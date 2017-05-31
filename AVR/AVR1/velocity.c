/*
 * velocity.c
 *
 * Created: 5/26/2017 5:52:07 PM
 *  Author: Chirag
 */

#include <avr/io.h>

#include "velocity.h"

//Function for velocity control
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR1AH = 0x00;
	OCR1BH = 0x00;
	
	if(0<=left_motor && left_motor<=255)
	{
		OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
	}
	else
	{
		OCR1AL = 0xFF;	//255
	}

	if(0<=right_motor && right_motor<=255)
	{
		OCR1BL = left_motor;     // duty cycle 'ON' period of PWM out for Right motor
	}
	else
	{
		OCR1BL = 0xFF; //255
	}
}
 
