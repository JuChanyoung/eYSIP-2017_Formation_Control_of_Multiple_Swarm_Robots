/*
 * motion.c
 *
 * Created: 5/26/2017 5:29:15 PM
 *  Author: Chirag
 */ 

#include <avr/interrupt.h>
#include <avr/io.h>
#include "motion.h"

unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
unsigned int Degrees; //to accept angle in degrees for turning

//ISR for right position encoder
ISR(INT0_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}

//ISR for left position encoder
ISR(INT1_vect)
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

//###############

//Function to configure INT1 (PORTD 3) pin as input for the left position encoder
void left_encoder_pin_config (void)
{
	DDRD  = DDRD & 0xF7;  //Set the direction of the PORTD 3 pin as input
	PORTD = PORTD | 0x08; //Enable internal pull-up for PORTD 3 pin
}

//Function to configure INT0 (PORTD 2) pin as input for the right position encoder
void right_encoder_pin_config (void)
{
	DDRD  = DDRD & 0xFB;  //Set the direction of the PORTD 2 pin as input
	PORTD = PORTD | 0x04; //Enable internal pull-up for PORTD 2 pin
}

void left_position_encoder_interrupt_init (void) //Interrupt 1 enable
{
	MCUCR = MCUCR | 0x08; // INT1 is set to trigger with falling edge
	GICR = GICR | 0x80;   // Enable Interrupt INT1 for left position encoder
}

void right_position_encoder_interrupt_init (void) //Interrupt 0 enable
{
	MCUCR = MCUCR | 0x02; // INT0 is set to trigger with falling edge
	GICR = GICR | 0x40;   // Enable Interrupt INT5 for right position encoder
}

void stop (void)
{
	motion_set(0x00);
}

//Function used for turning robot by specified degrees
void angle_rotate(unsigned int Degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) Degrees/ 12.85; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	while (1)
	{
		if((ShaftCountRight >= ReqdShaftCountInt) | (ShaftCountLeft >= ReqdShaftCountInt))
		break;
	}
	stop(); //Stop robot
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = DistanceInMM / 12.92; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	while(1)
	{
		if(ShaftCountRight > ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}

void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}

void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

void left_degrees(unsigned int Degrees)
{
	// 28 pulses for 360 degrees rotation 12.92 degrees per count
	left(); //Turn left
	angle_rotate(Degrees);
}

void right_degrees(unsigned int Degrees)
{
	// 28 pulses for 360 degrees rotation 12.92 degrees per count
	right(); //Turn right
	angle_rotate(Degrees);
}

void soft_left_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_left(); //Turn soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_right();  //Turn soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_left_2_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_left_2(); //Turn reverse soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_2_degrees(unsigned int Degrees)
{
	// 56 pulses for 360 degrees rotation 12.85 degrees per count
	soft_right_2();  //Turn reverse soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

//###############