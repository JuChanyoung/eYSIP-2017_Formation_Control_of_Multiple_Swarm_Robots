/*
 * velocity.c
 *
 * Created: 5/26/2017 5:52:07 PM
 *  Author: Chirag
 */

#include <avr/io.h>
#include <stdlib.h>
#include "motion.h"
#include "velocity.h"
#include "LCD.h"

//Function for velocity control
void velocity(int left_motor, int right_motor)
{
	if (left_motor>=0 && right_motor>=0)
	{
		forward();
		lcd_string2(2,1,"forward");
	}
	
	else if (left_motor<0 && right_motor>0)
	{
		left();
		left_motor=abs(left_motor)+40;
		lcd_string2(2,1,"left   ");
	}
	
	else if (left_motor>0 && right_motor<0)
	{
		right();
		right_motor=abs(right_motor)+40;
		lcd_string2(2,1,"right  ");
	}
	else 
	{
		back();
		left_motor=abs(left_motor);
		right_motor=abs(right_motor);
		lcd_string2(2,1,"back   ");
	}
		OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
		OCR1BL = right_motor;     // duty cycle 'ON' period of PWM out for Right motor
}

/*
//Function for velocity control
void velocity(int left_motor, int right_motor)
{
	if(0<=left_motor && left_motor<=255)
	{
		OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
	}
	else if(left_motor>255)
	{
		OCR1AL = 0xFF;
		// 		lcd_clear();
		// 		lcd_home();
		// 		lcd_string("Error 2");
	}
	else
	{
		OCR1AL = 0x00;
	}

	if(0<=right_motor && right_motor<=255)
	{
		OCR1BL = right_motor;     // duty cycle 'ON' period of PWM out for Right motor
	}
	else if(right_motor>255)
	{
		OCR1BL = 0xFF; //255
		// 		lcd_clear();
		// 		lcd_home();
		// 		lcd_string("Error 2");
	}
	else
	{
		OCR1BL = 0x00; //000
	}
	//right_power=OCR1BL;
	//left_power=OCR1AL;
}
*/