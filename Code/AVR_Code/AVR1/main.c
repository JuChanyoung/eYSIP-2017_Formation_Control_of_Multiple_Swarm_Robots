# define F_CPU 7372800

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include "motion.h"
#include "velocity.h"
#include "timer_init.h"
#include "LCD.h"
#include "XBee.h"
#include "string_parse.h"
#include "buzzer.h"

const int id = 3;	//Unique id of the robot, not used if robots are used in API mode with unique addresses

//All the data received over UART
int id_var;
int x_current;
int y_current;
int theta_current;
int x_req;
int y_req;
int theta_req;
int trigger;
int trigger_angle;

//Values for PID
float er, previous_er=0, integral = 0, derivative = 0;

extern unsigned volatile int stopwatch; //Used for timing purposes

unsigned int previous_PID_time = 0;
unsigned int previous_obs_time = 0;

int destination = 0;	//1 if robot is near the goal point and vice-versa

/*
* Function Name:port_init
* Input: None
* Output: None
* Logic: Calls the functions which will initializes the data direction registers
		 of the ports for various peripherals
		 ie: 1)Direction pins of motor-driver ic
		     2)Encoders
			 3)LCD
			 4)Buzzer
* Example Call: port_init()
*/
void port_init()
{
	motion_pin_config();
	lcd_port_config();
	left_encoder_pin_config();    //left encoder pin config
	right_encoder_pin_config();   //right encoder pin config
	buzzer_pin_config ();
}

/*
* Function Name:init_devices
* Input: None
* Output: None
* Logic: Calls the functions which will initialize the various components of the robot
		 ie: 1)All the ports
		     2)Left and right encoders
			 3)Timers for motor speed control (PWM)
			 4)LCD
			 5)UART initialization
* Example Call: init_devices()
*/
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

/*
* Function Name:avoid_obstacle
* Input: None
* Output: Avoids Obstacle if trigger is set
* Logic: Turns left or right based on the trigger and by the specified number of degrees
* Example Call: avoid_obstacle()
*/
void avoid_obstacle()
{
	if (trigger==1)	//turn left
	{
		hard_stop();
		_delay_ms(100);
		velocity2(90, 90);
		if (trigger_angle > 50) back_mm(50);
		left_degrees(trigger_angle);
		forward_mm(50);
		hard_stop();
	}
	else if (trigger==2) //turn left
	{
		hard_stop();
		_delay_ms(100);
		velocity2(90, 90);
		if (trigger_angle > 50)	back_mm(50);
		right_degrees(trigger_angle);
		forward_mm(50);
		hard_stop();
	}
}

/*
* Function Name:PID
* Input: The time since the last time this function was called in milliseconds
* Output: Velocities of the wheels are set such that the robot reaches closer to the goal
* Logic: Depending on the current and the required angle of the robot the angular velocity of the wheels will be set so as to minimize that error
		 'destination' is set to one as the robot reaches closer to the goal to turn off the obstacle avoidance behavior.
		  'V' and kp are reduced as the robot nears its goal point to avoid overshoot and to avoid oscillations.
* Example Call: PID(50)
*/
void PID(const int dt)
{		
		int v_left,v_right,R=3.5,L=11.5,V;
		float kp, ki, kd;
		float w;
		
		kp=.7;
		ki=0;
		kd=70;
		V=400;
	
		int distance=sqrt(square(y_req-y_current)+square(x_req-x_current));
		destination=(distance<100)?1:0;
			
		if (!x_req || !y_req)
		{
			hard_stop();
			destination = 1;
			return;
		}
		
		V=(distance<100)?200:400;
		kp=(distance<100)?.4:.7;
						
		if(distance>20)
		{
			er=theta_current-theta_req; //-360 to 360
			er = atan2(sin(er*3.14/180), cos(er*3.14/180))*(180/3.14); //-180 to 180
			
			integral= integral+er*dt;
			derivative = (er-previous_er)/dt;
			previous_er = er;
			
			w=kp*er + ki*integral + kd*derivative;
			v_left=((2*V+w*L)/(2*R));
			v_right=((2*V-w*L)/(2*R));
			
			velocity(v_left,v_right);
			destination=(distance<100)?1:0;
		}		
		else
		{
			hard_stop();
		}
}

/*
* Function Name:convert_ms_to_ticks
* Input: Number of milliseconds which you want converted to ticks based on a 450 hertz counter
* Output: Number of ticks of a 450 hertz which will be equal to the number of milliseconds
* Example Call: convert_ms_to_ticks(50)
*/
int convert_ms_to_ticks(unsigned int ms)
{
	return ms*450/1000;
}

/*
* Function Name:main
* Output: Go-to-goal behavior and avoid obstacle behavior is exhibited by the robot
* Logic: Both PID and avoid obstacle functions are called periodically without using a delay. 
		 This makes the loop non-blocking and allows us to call functions at different intervals of time if desired.
*/
int main()
{
	init_devices();
	const int dt = 50;
	
	buzzer_on();
	_delay_ms(100);
	buzzer_off();
					
	while(1)
	{
		if((stopwatch-previous_PID_time)>convert_ms_to_ticks(dt))
		{
			previous_PID_time=stopwatch;
			update_values();
			
			if (trigger==0)
				PID(dt);
		}
		
		if ((stopwatch-previous_obs_time)>convert_ms_to_ticks(50))
		{
			previous_obs_time=stopwatch;
			if (trigger && !destination)
			{
				avoid_obstacle();
			}
		}
	}
}

