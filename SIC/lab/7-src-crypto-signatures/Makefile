CFLAGS := $(CFLAGS) -g

all: rsa_sign rsa_verify ec_sign

rsa_sign: rsa_sign.o load_private_key.o digest_file.o print_hex.o
	$(CC) -g -o $@ $^ -lcrypto

rsa_verify: rsa_verify.o digest_file.o
	$(CC) -g -o $@ $^ -lcrypto

ec_sign: ec_sign.o load_private_key.o digest_file.o print_hex.o
	$(CC) -g -o $@ $^ -lcrypto

rsa_sign.o: load_private_key.h digest_file.h print_hex.h
rsa_verify.o: digest_file.h
ec_sign.o: load_private_key.h digest_file.h print_hex.h
load_private_key.o: load_private_key.h
digest_file.o: digest_file.h
print_hex.o: print_hex.h

clean:
	-rm *.o
	rm rsa_sign rsa_verify ec_sign
