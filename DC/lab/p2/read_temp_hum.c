#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void task1()
{
    while (true)
    {
        printf("reading temperature \n");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
void task2()
{
    while (true)
    {
        printf("reading humidity \n");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
void app_main(void)
{
    task1();
    task2();
}