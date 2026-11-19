#!/usr/bin/env python3
import sys

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

BLUEZ_SERVICE_NAME = "org.bluez"
DBUS_OM_IFACE = "org.freedesktop.DBus.ObjectManager"
DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"
ADAPTER_IFACE = "org.bluez.Adapter1"
DEVICE_IFACE = "org.bluez.Device1"
GATT_SERVICE_IFACE = "org.bluez.GattService1"
GATT_CHARACTERISTIC_IFACE = "org.bluez.GattCharacteristic1"

CHAT_SERVICE_UUID = "0000110a-0000-1000-8000-00805f9b34fb"
CHAT_MSG_UUID = "0000110b-0000-1000-8000-00805f9b34fb"


def find_chat_characteristic(objects, device_path):
    service_paths = {
        path
        for path, interfaces in objects.items()
        if GATT_SERVICE_IFACE in interfaces
        and str(interfaces[GATT_SERVICE_IFACE].get("UUID", "")).lower()
        == CHAT_SERVICE_UUID
        and interfaces[GATT_SERVICE_IFACE].get("Device") == device_path
    }

    for path, interfaces in objects.items():
        characteristic = interfaces.get(GATT_CHARACTERISTIC_IFACE)
        if (
            characteristic
            and characteristic.get("Service") in service_paths
            and str(characteristic.get("UUID", "")).lower() == CHAT_MSG_UUID
        ):
            return path
    return None


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <hci_interface> <device_address>")
        return 2

    adapter_name, target_address = argv[1], argv[2].upper()
    adapter_path = f"/org/bluez/{adapter_name}"
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    object_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, "/"), DBUS_OM_IFACE
    )
    adapter = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter_path), ADAPTER_IFACE
    )
    main_loop = GLib.MainLoop()
    state = {
        "characteristic": None,
        "device_path": None,
        "discovering": False,
        "connected_by_client": False,
        "notifying": False,
        "signal_match": None,
        "exit_code": 0,
        "device_waits": 0,
        "service_waits": 0,
    }

    def fail(message):
        print(message, file=sys.stderr)
        state["exit_code"] = 1
        main_loop.quit()

    def get_objects():
        return object_manager.GetManagedObjects()

    def stop_discovery():
        if state["discovering"]:
            adapter.StopDiscovery()
            state["discovering"] = False

    def on_message(interface, changed, invalidated):
        if interface != GATT_CHARACTERISTIC_IFACE or "Value" not in changed:
            return
        message = bytes(changed["Value"]).decode("utf-8", errors="replace")
        print(f"\n{message}\n> ", end="", flush=True)

    def send_message(message):
        characteristic = state["characteristic"]
        if characteristic is None:
            return
        value = dbus.Array(message.encode("utf-8"), signature="y")
        options = dbus.Dictionary({}, signature="sv")
        try:
            characteristic.WriteValue(value, options)
        except dbus.DBusException as error:
            print(f"Could not send message: {error}", file=sys.stderr)

    def on_stdin(_fd, condition):
        if condition & GLib.IO_ERR:
            fail("Error reading chat input.")
            return False
        line = sys.stdin.readline()
        if not line:
            main_loop.quit()
            return False
        message = line.rstrip("\r\n")
        if message.casefold() == "/quit":
            main_loop.quit()
            return False
        if message:
            send_message(message)
        print("> ", end="", flush=True)
        return True

    def start_chat(characteristic_path):
        characteristic = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, characteristic_path),
            GATT_CHARACTERISTIC_IFACE,
        )
        state["characteristic"] = characteristic
        state["signal_match"] = bus.add_signal_receiver(
            on_message,
            signal_name="PropertiesChanged",
            dbus_interface=DBUS_PROP_IFACE,
            path=characteristic_path,
            arg0=GATT_CHARACTERISTIC_IFACE,
        )
        try:
            characteristic.StartNotify()
        except dbus.DBusException as error:
            fail(f"Could not subscribe to chat messages: {error}")
            return False
        state["notifying"] = True
        print("Connected to the chat service. Type a message or /quit to exit.")
        print("> ", end="", flush=True)
        GLib.io_add_watch(
            sys.stdin.fileno(), GLib.IO_IN | GLib.IO_HUP, on_stdin
        )
        return False

    def wait_for_services():
        try:
            objects = get_objects()
            device = objects.get(state["device_path"], {}).get(DEVICE_IFACE, {})
            if device.get("ServicesResolved", False):
                characteristic_path = find_chat_characteristic(
                    objects, state["device_path"]
                )
                if characteristic_path is None:
                    fail("The connected device does not expose the chat GATT service.")
                    return False
                return start_chat(characteristic_path)
        except dbus.DBusException as error:
            fail(f"Could not inspect GATT services: {error}")
            return False

        state["service_waits"] += 1
        if state["service_waits"] >= 60:
            fail("Timed out waiting for the device's GATT services to resolve.")
            return False
        return True

    def connect_to_device(device_path):
        try:
            stop_discovery()
            state["device_path"] = device_path
            device = dbus.Interface(
                bus.get_object(BLUEZ_SERVICE_NAME, device_path), DEVICE_IFACE
            )
            device_properties = get_objects()[device_path][DEVICE_IFACE]
            if not device_properties.get("Connected", False):
                print(f"Connecting to {target_address} ...")
                device.Connect()
                state["connected_by_client"] = True
            GLib.timeout_add(500, wait_for_services)
        except dbus.DBusException as error:
            fail(f"Could not connect to {target_address}: {error}")
        return False

    def find_device():
        try:
            for path, interfaces in get_objects().items():
                device = interfaces.get(DEVICE_IFACE)
                if (
                    device
                    and str(device.get("Address", "")).upper() == target_address
                    and device.get("Adapter") == adapter_path
                ):
                    return connect_to_device(path)
        except dbus.DBusException as error:
            fail(f"Could not discover Bluetooth devices: {error}")
            return False

        state["device_waits"] += 1
        if state["device_waits"] >= 60:
            fail(f"Timed out waiting to discover {target_address}.")
            return False
        return True

    try:
        objects = get_objects()
        known_device = next(
            (
                path
                for path, interfaces in objects.items()
                if DEVICE_IFACE in interfaces
                and str(interfaces[DEVICE_IFACE].get("Address", "")).upper()
                == target_address
                and interfaces[DEVICE_IFACE].get("Adapter") == adapter_path
            ),
            None,
        )
        if known_device is not None:
            connect_to_device(known_device)
        else:
            print(f"Scanning for {target_address} ...")
            adapter.StartDiscovery()
            state["discovering"] = True
            GLib.timeout_add(500, find_device)

        if state["exit_code"] == 0:
            main_loop.run()
    except dbus.DBusException as error:
        print(f"Bluetooth D-Bus error: {error}", file=sys.stderr)
        state["exit_code"] = 1
    except KeyboardInterrupt:
        print("\nDisconnecting...")
    finally:
        try:
            stop_discovery()
        except dbus.DBusException as error:
            print(f"Could not stop Bluetooth discovery: {error}", file=sys.stderr)
            state["exit_code"] = 1
        if state["notifying"]:
            try:
                state["characteristic"].StopNotify()
            except dbus.DBusException as error:
                print(f"Could not stop chat notifications: {error}", file=sys.stderr)
                state["exit_code"] = 1
        if state["signal_match"] is not None:
            state["signal_match"].remove()
        if state["connected_by_client"]:
            try:
                device = dbus.Interface(
                    bus.get_object(BLUEZ_SERVICE_NAME, state["device_path"]),
                    DEVICE_IFACE,
                )
                device.Disconnect()
            except dbus.DBusException as error:
                print(f"Could not disconnect from the chat device: {error}", file=sys.stderr)
                state["exit_code"] = 1

    return state["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
