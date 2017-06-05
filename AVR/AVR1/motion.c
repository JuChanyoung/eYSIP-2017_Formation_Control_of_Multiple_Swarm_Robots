/*
 * motion.c
 *
 * Created: 5/26/2017 5:29:15 PM
 *  Author: Chirag
 */ 

#include <avr/io.h>
#include "motion.h"

void motion_pin_config (void)
{
	DDRB = DDRB | 0x0F;   //set direction of the PORTB3 to PORTB0 pins as output
	PORTB = PORTB & 0xF0; // set initial value of the PORTB3 to PORTB0 pins to logic 0
	DDRD = DDRD | 0x30;   //Setting PD4 and PD5 pins as output for PWM generation
	PORTD = PORTD | 0x30; //PD4 and PD5 pins are for velocity control using PWM
}

//Function used for setting motor's direction
static void motion_set (unsigned char Direction)
{
	unsigned char PortBRestore = 0;

	Direction &= 0x0F; 			// removing upper nibbel as it is not needed
	PortBRestore = PORTB; 			// reading the PORTB's original status
	PortBRestore &= 0xF0; 			// setting lower direction nibbel to 0
	PortBRestore |= Direction; 	// adding lower nibbel for direction command and restoring the PORTB status
	PORTB = PortBRestore; 			// setting the command to the port
}

void forward (void)         //both wheels forward
{
	motion_set(0x06);
}

void back (void)            //both wheels backward
{
	motion_set(0x09);
}

void left (void)            //Left wheel backward, Right wheel forward
{
	motion_set(0x05);
}

void right (void)           //Left wheel forward, Right wheel backward
{
	motion_set(0x0A);
}

void soft_left (void)       //Left wheel stationary, Right wheel forward
{
	motion_set(0x04);
}

void soft_right (void)      //Left wheel forward, Right wheel is stationary
{
	motion_set(0x02);
}

void soft_left_2 (void)     //Left wheel backward, right wheel stationary
{
	motion_set(0x01);
}

void soft_right_2 (void)    //Left wheel stationary, Right wheel backward
{
	motion_set(0x08);
}

void hard_stop (void)       //hard stop(stop suddenly)
{
	motion_set(0x00);
}

void soft_stop (void)       //soft stop(stops slowly)
{
	motion_set(0x0F);
}
