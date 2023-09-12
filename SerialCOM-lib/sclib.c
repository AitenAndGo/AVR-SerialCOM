#include <avr/io.h>
#include "sclib.h"
#include <util/setbaud.h>

// setting the type of data
// SerialCOM receive 2 first bytes where 1 byte is a type of data 
// and 2 is size of data
#define set_type_int        send_byte('i')
#define set_type_byte       send_byte('b')
#define set_type_char       send_byte('c')
#define set_type_plot       send_byte('p')
#define set_type_float      send_byte('f')
#define set_type_uint8_t    send_byte('u')
#define set_type_uint16_t   send_byte('s')

#define send_one            send_byte(0x01);

void USART_Init()
{
    // Set baud rate 
    UBRR0H = UBRRH_VALUE;         
    UBRR0L = UBRRL_VALUE;
    #if USE_2X
    UCSR0A |= (1 << U2X0);
    #else
    UCSR0A &= ~(1 << U2X0);
    #endif
    
    /* Enable USART transmitter/receiver */
    UCSR0B = (1 << TXEN0) | (1 << RXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);   /* 8 data bits, 1 stop bit */
}

void send_byte(uint8_t data)
{
    loop_until_bit_is_set(UCSR0A, UDRE0);
    UDR0 = data; 
}

void print_uint8_t(uint8_t data)
{
    set_type_uint8_t;
    send_one;
    send_byte(data);
}

void print_uint16_t(uint16_t data)
{
    set_type_uint16_t;
    send_one;
    send_byte(data);
    send_byte(data >> 8);
}

void print_char(char data)
{
    set_type_char;
    send_one;
    send_byte(data);
}


void print_float(float data){
    set_type_float;
    send_one;
    // convert float
    uint8_t* bytes = (uint8_t*)&data;

    // send all 4 bytes
    for(int i = 0; i < 4; i++) {
        send_byte(bytes[i]);
    }
}

void print_int(int data){
    set_type_int;
    send_one;
    send_byte(data);
    send_byte(data >> 8);
}

void println_uint8_t(uint8_t data){
    print_uint8_t(data);
    print_char('\n');
}

void println_uint16_t(uint16_t data){
    print_uint16_t(data);
    print_char('\n');
}

void println_float(float data){
    print_float(data);
    print_char('\n');
}

void println_int(int data){
    print_int(data);
    print_char('\n');
}

void println_char(char data){
    print_char(data);
    print_char('\n');
}

void print(const char data[]){
    uint8_t size = 0;
    
    while (data[size])
    {
        print_char(data[size]);
        size++;
    }
    
}

void println(const char data[]){
    print(data);
    print_char('\n');
}

void plot_uint8_t(uint8_t data_x, uint8_t data_y){
    set_type_plot;
    set_type_uint8_t;
    send_byte(0x02);
    send_byte(data_x);
    send_byte(data_y);
}

void plot_uint16_t(uint16_t data_x, uint16_t data_y){
    set_type_plot;
    set_type_uint16_t;
    send_byte(0x02);
    send_byte(data_x);
    send_byte(data_x >> 8);
    send_byte(data_y);
    send_byte(data_y >> 8);
}

void plot_float(float data_x, float data_y){
    set_type_plot;
    set_type_float;
    send_byte(0x02);

    // convert float
    uint8_t* bytes = (uint8_t*)&data_x;

    // send all 4 bytes
    for(int i = 0; i < 4; i++) {
        send_byte(bytes[i]);
    }

    // convert float
    bytes = (uint8_t*)&data_y;

    // send all 4 bytes
    for(int i = 0; i < 4; i++) {
        send_byte(bytes[i]);
    }
}

void plot_int(int data_x, int data_y){
    set_type_plot;
    set_type_int;
    send_byte(0x02);
    send_byte(data_x);
    send_byte(data_x >> 8);
    send_byte(data_y);
    send_byte(data_y >> 8);
}

uint8_t receive_byte(){
    // Wait for incoming data
    loop_until_bit_is_set(UCSR0A, RXC0); 
    return UDR0;  
}

uint8_t receive_new_byte(uint8_t* byte)
{
    return 0;
}