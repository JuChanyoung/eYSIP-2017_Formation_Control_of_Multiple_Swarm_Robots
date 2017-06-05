/*
 * velocity.c
 *
 * Created: 5/26/2017 5:52:07 PM
 *  Author: Chirag
 */

#include <avr/io.h>
#include "velocity.h"
#include "LCD.h"

//Function for velocity control
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	//lcd_print(1,8,left_motor,3);
	//lcd_print(1,12,right_motor,3);
	
	OCR1AH = 0x00;
	OCR1BH = 0x00;
	
	if(0<=left_motor && left_motor<=255)
	{
		OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
	}
	else
	{
		OCR1AL = 0x00;	//000
		lcd_clear();
		lcd_home();
		lcd_string("Error 2");
	}

	if(0<=right_motor && right_motor<=255)
	{
		OCR1BL = right_motor;     // duty cycle 'ON' period of PWM out for Right motor
	}
	else
	{
		OCR1BL = 0x00; //000
		lcd_clear();
		lcd_home();
		lcd_string("Error 2");
	}
}
 
