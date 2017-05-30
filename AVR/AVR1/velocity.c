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
	OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
	OCR1BH = 0x00;
	OCR1BL = right_motor;    // duty cycle 'ON' period of PWM out for Right motor
}
 
