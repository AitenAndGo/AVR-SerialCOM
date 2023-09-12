#include <stdint.h>

#ifndef BAUD
    #define BAUD  9600                 
#endif

void USART_Init();

void send_byte(uint8_t data);

void print_uint8_t(uint8_t data);
void print_uint16_t(uint16_t data);
void print_float(float data);
void print_int(int data);
void print_char(char data);

void println_uint8_t(uint8_t data);
void println_uint16_t(uint16_t data);
void println_float(float data);
void println_int(int data);
void println_char(char data);

void print(const char data[]);
void println(const char data[]);

void plot_uint8_t(uint8_t data_x, uint8_t data_y);
void plot_uint16_t(uint16_t data_x, uint16_t data_y);
void plot_float(float data_x, float data_y);
void plot_int(int data_x, int data_y);

// wait until new byte appears
uint8_t receive_byte();

// if there is new byte then upgrades value of byte and return 1 else return 0
uint8_t receive_new_byte(uint8_t* byte);