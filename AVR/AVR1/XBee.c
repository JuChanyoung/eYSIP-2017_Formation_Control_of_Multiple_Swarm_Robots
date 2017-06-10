#define F_CPU 7372800
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>

#include "XBee.h"
#include "string_parse.h"

volatile char data;  //to store received data from UDR0
volatile char data_string[100];  //to store received data from UDR
volatile char data_string_var[100];  //to store all received data from UDR
volatile int i = 0, j = 0;
volatile char append_on = 0;
char my_string=0;

/*
UART0 initialization
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
		j=0;
		append_on = 1;
	}
	
	else if (append_on==1)
	{
		data_string_var[i]=data;
		i++;
	 
	 //count the number of /
	 if (data == 0x2F) // ascii of /
	 {
		 j++; 
	 }
	}
	
	//checks to see if id matches
	if (j==1)
	{
		append_on = check_id(data_string_var); 
	}
	
	//checks to see if entire string is received, if yes save it
	if (j==7 && append_on==1)
	{
		i=0;
		j=0;
		append_on=0;
		strcpy(data_string, data_string_var); //Entire string received!! Save it!!
	}
}