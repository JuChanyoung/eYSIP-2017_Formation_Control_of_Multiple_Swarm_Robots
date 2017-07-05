#define F_CPU 7372800
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>

#include "XBee.h"
#include "string_parse.h"

volatile char data;  //to store received data from UDR0
volatile char previous_data;
volatile char data_string[40];  //to store received data from UDR
volatile char data_string_var[40];  //to store all received data from UDR
volatile int i = 0, j = 0;
volatile char append_on = 0;
char my_string=0;

/*
UART0 initialization
desired baud rate: 115200
actual: baud rate:115200 (0.0%)
char size: 8 bit
parity: Disabled
*/
void uart0_init(void)
{
 UCSRB = 0x00; //disable while setting baud rate
 UCSRA = 0x00;
 UCSRC = 0x86;
 //UBRRL = 0x2F; //set baud rate lo  //67 is for 16MHz 9600 baudrate
 UBRRL = 0x03; //set baud rate lo  //115200 baudrate
 UBRRH = 0x00; //set baud rate hi
 UCSRB = 0x98; 
}

/*
The data is received character by character over UART. When a character is received it is very briefly stored in a buffer and USART_RXC_vect is incremented. This is done internally by the microcontroller.
USART_RXC_vect then triggers an interrupt.
This interrupt then decides what to do with this character of data. 
If it is a valid byte of data it will be stored in the array "data_string_var". After a complete packet of data is received it is copied to the array "data_string".
<#.........#> is a proper string which then saved to "data_string" by the ISR.
*/
ISR(USART_RXC_vect)
{		
	previous_data = data;
	data = UDR;
	
	strcpy((char*) data_string, (const char*)data_string_var); //Entire string received!! Save it!!

	if (previous_data==0x3C && data == 0x23)//< and #
	{
		append_on = 1;
		i=0;
	}
	
	else if (previous_data==0x23 && data==0x3E)//# and >
	{
		append_on=0;
		strcpy((char*)data_string, (const char*) data_string_var); //Entire string received!! Save it!!
	}
	
	else if (append_on==1 && data != 0x23)
	{
		data_string_var[i]=data;
		i++;
	}
}
