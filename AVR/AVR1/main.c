# define F_CPU 7372800

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>

#include "motion.h"
#include "velocity.h"
#include "timer_init.h"
#include "LCD.h"
#include "XBee.h"
#include "string_parse.h"

extern volatile char data;  //to store received data from UDR0
extern volatile char flag_instruction;
extern volatile char data_string[100];  //to store received data from UDR
char data_string1[100];
extern char parts[4][10];

const int id = 1;
int id_var;
int x;
int y;
int theta;

//Function to initialize ports
void port_init()
{
	motion_pin_config();
	lcd_port_config();
}

void init_devices (void)
{
	cli(); //Clears the global interrupts
	port_init();
	lcd_init();
	timer1_init();
	uart0_init();
	sei(); //Enables the global interrupts
}

//Main Function
int main()
{
	init_devices();
		
	while(1)
	{		
		//Update the values on the LCD every
		_delay_ms(500);
		update_values();
		//display_data_string();
		//lcd_cursor()
		//lcd_string("1");
	}
}

