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

/*
* Function Name: velocity
* Input: left_motor_speed, left_motor_speed -> values can range from -255 to +255
* Output: Speed of the motors is changed, direction of rotation will also be set according to the sign of the argument.
		  Negative velocity will make the wheel rotate in the opposite direction.
* Logic: Change the values of the OCRs of the PWM generating timer to change the duty cycle.
		 If input speed>255 or if speed<(-255) the speed is set to 255.
* Example Call: velocity(200,-50) -> turn right
*/
void velocity(int left_motor, int right_motor)
{
	if (left_motor>=0 && right_motor>=0)
	{
		forward();
		//lcd_string2(2,1,"forward");
	}
	
	else if (left_motor<0 && right_motor>0)
	{
		left();
		left_motor=abs(left_motor)+40;//some offset is added so that the wheel still turns at lower -ve values
		//lcd_string2(2,1,"left   ");
	}
	
	else if (left_motor>0 && right_motor<0)
	{
		right();
		right_motor=abs(right_motor)+40;//some offset is added so that the wheel still turns at lower -ve values
		//lcd_string2(2,1,"right  ");
	}
	else 
	{
		back();
		left_motor=abs(left_motor);
		right_motor=abs(right_motor);
		//lcd_string2(2,1,"back   ");
	}
		OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
		OCR1BL = right_motor;     // duty cycle 'ON' period of PWM out for Right motor
}

/*
* Function Name: velocity2
* Input: left_motor_speed, left_motor_speed -> values between 0-255
* Output: Speed of the motors is changed 
* Logic: Change the values of the OCRs of the PWM generating timer to change the duty cycle
* Example Call: velocity2(200,150)
*/
void velocity2(unsigned char left_motor, unsigned char right_motor)
{
	OCR1AL = left_motor;     // duty cycle 'ON' period of PWM out for Left motor
	OCR1BL = right_motor;    // duty cycle 'ON' period of PWM out for Right motor
}