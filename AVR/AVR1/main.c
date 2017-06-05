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

extern volatile char data;  //to store received data from UDR0
extern volatile char flag_instruction;
extern volatile char data_string[100];  //to store received data from UDR
char data_string1[100];
extern char parts[4][10];

//const int id = 1;
int id_var;
int x_current;
int y_current;
int theta_current;
int x_req;
int y_req;
int theta_req;
int er,v_left,v_right,L,R,V;
float w;
float kp;
int distance;



//Function to initialize ports
void port_init()
{
	motion_pin_config();
	lcd_port_config();
}

void init_devices (void)
{
	cli(); //Clears the global interrupts
	port_init();
	lcd_init();
	timer1_init();
	uart0_init();
	sei(); //Enables the global interrupts
}

//Main Function
int main()
{ 
	init_devices();

	kp=0.1;
	V=100;
	R=3.5;
	L=11.5;	
	
	while(1)
	{	
	cli();	
	update_values();
	sei();
	
	distance=sqrt(square(y_req-y_current)+square(x_req-x_current));
	lcd_print(1,1,distance,3);

	int theta1;
	theta1 = abs(theta_current-theta_req); //0 to (360)
	int er2=0;
	
	if(180>=theta1 && theta1>=0)
	{
		er2 = theta1; //0 to (180)
	}
	else if (theta1<=360 && theta1>180)
	{
		er2 = 360-theta1;	//0 to (180)
	}
	else
	{
		er2=0;
		lcd_clear();
		lcd_home();
		lcd_string("Error 1");
	}
	w=kp*er2;
			
		if(distance>50)
		{		
			er=theta_current-theta_req;
			if (er<0)
			{
				er+=360;
			}
		
			if (er<=360 && er>=180)
			{
				//lcd_home();
				//lcd_string("left   ");
				v_left=((2*V-w*L)/(2*R));
				v_right=((2*V+w*L)/(2*R));
				velocity(v_left,v_right);
				forward();
			}
			else if (er<180 && er>=0)
			{
				//lcd_home();
				//lcd_string("right  ");		
				v_left=((2*V+w*L)/(2*R));
				v_right=((2*V-w*L)/(2*R));
				velocity(v_left,v_right);
				forward();
			}
			else
			{
				lcd_clear();
				lcd_home();
				lcd_string("Error 3");
			}
		}
		
		else
		{
			hard_stop();
			lcd_clear();
			lcd_home();
			lcd_string("Stopped");
		}
	}
}

