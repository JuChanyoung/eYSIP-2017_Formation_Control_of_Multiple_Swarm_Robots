#define F_CPU 7372800
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "XBee.h"

volatile char flag_instruction = 0;
volatile char data;  //to store received data from UDR0
volatile char data_string[100];  //to store received data from UDR
volatile int i = 0;

/*
UART0 initialisation
desired baud rate: 9600
actual: baud rate:9600 (0.0%)
char size: 8 bit
parity: Disabled
*/
void uart0_init(void)
{
 UCSRB = 0x00; //disable while setting baud rate
 UCSRA = 0x00;
 UCSRC = 0x86;
 UBRRL = 0x2F; //set baud rate lo  //67 is for 16MHz 9600 baudrate
 UBRRH = 0x00; //set baud rate hi
 UCSRB = 0x98; 
}



//ISR(SIG_UART_RECV)  		// ISR for receive complete interrupt //, ISR_NOBLOCK
ISR(USART_RXC_vect)
{
	data = UDR; 				//making copy of data from UDR0 in 'data' variable
	
	if (data == 0x2E) // ascii of .
	{
		i=0;
	}
	else
	{
	 data_string[i]=data;
	 i++;
	 UDR = data;
	 flag_instruction++;			//One instruction received	
	}
}