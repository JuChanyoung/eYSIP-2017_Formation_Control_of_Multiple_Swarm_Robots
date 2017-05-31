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

extern volatile char flag_instruction;
extern volatile char data_string[100];  //to store received data from UDR
char data_string1[100];

const int id = 1;

int id_var;
int x_current;
int y_current;
int theta_current;
int x_req;
int y_req;
int theta_req;

//Function to initialize ports
void port_init()
{
	motion_pin_config();
	lcd_port_config();
	motion_pin_config();          //robot motion pins config
	left_encoder_pin_config();    //left encoder pin config
	right_encoder_pin_config();   //right encoder pin config
}

void init_devices (void)
{
	cli(); //Clears the global interrupts
	port_init();
	lcd_init();
	timer1_init();
	uart0_init();
	left_position_encoder_interrupt_init();
	right_position_encoder_interrupt_init();	
	sei(); //Enables the global interrupts
}

//Main Function
int main()
{
	init_devices();
		
	int theta_error;
	
	int vel = 255;
	velocity(vel,vel);	
		
	while(1)
	{		
		update_values();
		theta_error = theta_req - theta_current;
		
		if(theta_error>0) //clockwise
		{
			left_degrees(theta_error);
		}

		if (theta_error<0) //counter-clockwise
		{
			right_degrees(-theta_error);
		}
		
		_delay_ms(1000);
	}
}

