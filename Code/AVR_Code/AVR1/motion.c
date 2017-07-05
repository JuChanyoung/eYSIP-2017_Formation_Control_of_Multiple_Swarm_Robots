/*
 * motion.c
 *
 * Created: 5/26/2017 5:29:15 PM
 *  Author: Chirag
 */ 
#include <avr/interrupt.h>
#include <avr/io.h>
#include <stdlib.h>
#include "motion.h"
#include "velocity.h"

volatile unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
volatile unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
unsigned int Degrees; //to accept angle in degrees for turning

//ISR for right position encoder
ISR(INT1_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}

//ISR for left position encoder
ISR(INT0_vect)
{
	ShaftCountLeft++;  //increment left shaft position count
}

void motion_pin_config (void)
{
	DDRB = DDRB | 0x0F;   //set direction of the PORTB3 to PORTB0 pins as output
	PORTB = PORTB & 0xF0; // set initial value of the PORTB3 to PORTB0 pins to logic 0
	DDRD = DDRD | 0x30;   //Setting PD4 and PD5 pins as output for PWM generation
	PORTD = PORTD | 0x30; //PD4 and PD5 pins are for velocity control using PWM
}

/*
* Function Name motion_set
* Input: Direction -> 8-bit value corresponding to the direction of the motors
* Output: Motors spin in the specified direction
* Logic: Sets the lower nibble of PORTB to the lower nibble of Direction
		 Lower nibble of a Port a controls the direction of the motors since they ate connected to the direction pins of L293d
* Example Call: motion_set(0x06) -> for forward
*/
static void motion_set (unsigned char Direction)
{
	unsigned char PortBRestore = 0;

	Direction &= 0x0F; 			// removing upper nibbel as it is not needed
	PortBRestore = PORTB; 			// reading the PORTB's original status
	PortBRestore &= 0xF0; 			// setting lower direction nibbel to 0
	PortBRestore |= Direction; 	// adding lower nibbel for direction command and restoring the PORTB status
	PORTB = PortBRestore; 			// setting the command to the port
}

/*
* Function Name:forward
* Input: None
* Output: The bot moves forward
* Logic: Writes 0x06 to lower nibble of PORTA xxxx 0110
* Example Call: forward()
*/
void forward (void)         //both wheels forward
{
	motion_set(0x06);
}

/*
* Function Name:back
* Input: None
* Output: The bot moves backwards
* Logic: Writes 0x09 to lower nibble of PORTA xxxx 1001
* Example Call: back()
*/
void back (void)            //both wheels backward
{
	motion_set(0x09);
}

/*
* Function Name:left
* Input: None
* Output: The bot turns anticlockwise, ie Left wheel backward, Right wheel forward
* Logic: Writes 0x05 to lower nibble of PORTA xxxx 0101
* Example Call: left()
*/
void left (void)            //Left wheel backward, Right wheel forward
{
	motion_set(0x05);
}

/*
* Function Name:right
* Input: None
* Output: The bot turns clockwise, ie Left wheel forward, Right wheel backward
* Logic: Writes 0x0A to lower nibble of PORTA xxxx 1011
* Example Call: right()
*/
void right (void)           //Left wheel forward, Right wheel backward
{
	motion_set(0x0A);
}

/*
* Function Name:soft_left
* Input: None
* Output: The bot turns counter-clockwise, ie Left wheel stationary, Right wheel forward
* Logic: Writes 0x04 to lower nibble of PORTA xxxx 0100
* Example Call: soft_left()
*/

void soft_left (void)       //Left wheel stationary, Right wheel forward
{
	motion_set(0x04);
}
/*
* Function Name:soft_right
* Input: None
* Output: The bot turns clockwise, ie Left wheel forward, Right wheel is stationary
* Logic: Writes 0x02 to lower nibble of PORTA xxxx 0010
* Example Call: soft_right()
*/
void soft_right (void)      //Left wheel forward, Right wheel is stationary
{
	motion_set(0x02);
}

/*
* Function Name:soft_left_2
* Input: None
* Output: The bot turns counter-clockwise, ie Left wheel backward, right wheel stationary
* Logic: Writes 0x01 to lower nibble of PORTA xxxx 0001
* Example Call: soft_left_2()
*/
void soft_left_2 (void)     //Left wheel backward, right wheel stationary
{
	motion_set(0x01);
}

/*
* Function Name:soft_right_2
* Input: None
* Output: The bot turns clockwise, ie Left wheel stationary, Right wheel backward
* Logic: Writes 0x08 to lower nibble of PORTA xxxx 1000
* Example Call: soft_right_2()
*/
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

//###############

/*
* Function Name: left_encoder_pin_config
* Input: None
* Output: Pin connected to left position encoder is set as input
* Logic: PORTD 3 pin is set as input-xxxx0xxx
* Example Call: left_encoder_pin_config ()
*/
void left_encoder_pin_config (void)
{
	DDRD  = DDRD & 0xF7;  //Set the direction of the PORTD 3 pin as input
	PORTD = PORTD | 0x08; //Enable internal pull-up for PORTD 3 pin
}

/*
* Function Name: right_encoder_pin_config
* Input: None
* Output: Pin to connected right position encoder is set as input
* Logic: PORTD 2 pin is set as input-xxxxx0xx
* Example Call: right_encoder_pin_config ()
*/
void right_encoder_pin_config (void)
{
	DDRD  = DDRD & 0xFB;  //Set the direction of the PORTD 2 pin as input
	PORTD = PORTD | 0x04; //Enable internal pull-up for PORTD 2 pin
}

/*
* Function Name: left_position_encoder_interrupt_init
* Input: None
* Output: Enable interrupt 1 for the left side position encoder
* Logic: Given alongside the code
* Example Call: left_position_encoder_interrupt_init ()
*/
void left_position_encoder_interrupt_init (void)
{
	MCUCR = MCUCR | 0x04; // INT1 is set to trigger with a falling or rising edge
	GICR = GICR | 0x80;   // Enable Interrupt INT1 for left position encoder
}

/*
* Function Name: right_position_encoder_interrupt_init
* Input: None
* Output: Enable interrupt 0 for the left side position encoder
* Logic: Given alongside the code
* Example Call: right_position_encoder_interrupt_init ()
*/
void right_position_encoder_interrupt_init (void) //Interrupt 0 enable
{
	MCUCR = MCUCR | 0x01; // INT0 is set to trigger with a falling or rising edge
	GICR = GICR | 0x40;   // Enable Interrupt INT5 for right position encoder
}

/*
* Function Name: stop
* Input: None
* Output: Stops the bot
* Example Call: stop()
*/
void stop (void)
{
	motion_set(0x00);
}

/*
* Function Name:angle_rotate
* Input: Degrees -> No of degrees to turn
* Output: Stops the bot after it turns the specified number of degrees
* Logic: 1.Convert the degrees to rotate into a no of encoder pulses
		 2.Set ReqdShaftCountInt to 0
		 3.Wait for TurnCount to become equal to the required count
		 4.Stop the Bot
* Example Call: angle_rotate(90)
*/
void angle_rotate(unsigned int Degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) 2*Degrees/ 12.85; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	while (1)
	{
		if((ShaftCountRight+ShaftCountLeft)/2 >= ReqdShaftCountInt)
		break;
	}
	stop(); //Stop robot
}

/*
* Function Name:linear_distance_mm
* Input: DistanceInMM -> distance to move
* Output: Stops the bot after it moves the specified distance
* Logic: 1.Convert the distance to move into a no of encoder pulses
		 2.Set ReqdShaftCountInt to 0
		 3.Wait for ReqdShaftCountInt to become equal to the required count
		 4.Stop the Bot
* Example Call: linear_distance_mm(1000) -> Move one meter
*/
void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = 2*DistanceInMM / 12.92; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	while(1)
	{
		if((ShaftCountRight+ShaftCountLeft)/2 >= ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}

/*
* Function Name:forward_mm
* Input: DistanceInMM -> distance to move forward
* Output: Moves the bot forward by the specified distance
* Logic: 1.Move forward
		 2.Stop after specified distance is reached
* Example Call: forward_mm(1000) -> Move forward one meter
*/
void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}

/*
* Function Name:back_mm
* Input: DistanceInMM -> distance to move back
* Output: Moves the bot backwards by the specified distance
* Logic: 1.Move backwards
		 2.Stop after specified distance is reached
* Example Call: back_mm(1000) -> Move back one meter
*/
void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

/*
* Function Name: left_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot left by the specified degrees, ie Left wheel backward, Right wheel forward
* Logic: 1.Turn counter-clockwise
		 2.Stop after specified degrees is reached
* Example Call: left_degrees(90) -> Turn left by 90 degrees
*/
void left_degrees(unsigned int Degrees)
{
	// 28 pulses for 360 degrees rotation 12.92 degrees per count
	left(); //Turn left
	angle_rotate(Degrees);
}

/*
* Function Name: right_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot right by the specified degrees, ie right wheel backward, left wheel forward
* Logic: 1.Turn clockwise
		 2.Stop after specified degrees is reached
* Example Call: right_degrees(90) -> Turn right by 90 degrees
*/
void right_degrees(unsigned int Degrees)
{
	// 28 pulses for 360 degrees rotation 12.92 degrees per count
	right(); //Turn right
	angle_rotate(Degrees);
}

/*
* Function Name: soft_left_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot left by the specified degrees, ie Right wheel forward only
* Logic: 1.Turn
		 2.Stop after specified degrees is reached
* Example Call: soft_left_degrees(90) -> Turn left by 90 degrees
*/
void soft_left_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_left(); //Turn soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

/*
* Function Name: soft_right_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot right by the specified degrees, ie Left wheel forward only
* Logic: 1.Turn
		 2.Stop after specified degrees is reached
* Example Call: soft_right_degrees(90) -> Turn right by 90 degrees
*/
void soft_right_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_right();  //Turn soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

/*
* Function Name: soft_left_2_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot left by the specified degrees, ie Left wheel backwards only
* Logic: 1.Turn
		 2.Stop after specified degrees is reached
* Example Call: soft_left_2_degrees(90) -> Turn left by 90 degrees
*/
void soft_left_2_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_left_2(); //Turn reverse soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

/*
* Function Name: soft_right_2_degrees
* Input: Degrees -> Angle to rotate
* Output: Turns the bot right by the specified degrees, ie Right wheel backwards only
* Logic: 1.Turn
		 2.Stop after specified degrees is reached
* Example Call: soft_right_2_degrees(90) -> Turn left by 90 degrees
*/
void soft_right_2_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_right_2();  //Turn reverse soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

//###############