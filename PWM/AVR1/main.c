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

const int id = 3;
int id_var;
int x_current;
int y_current;
int theta_current;
int x_req;
int y_req;
int theta_req;
int v_left,v_right,R=3.5,L=11.5,V;
float er, previous_er=0, integral = 0, derivative = 0;
float w;
float kp, ki, kd;
int distance;

extern volatile int i;

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

int main()
{
	init_devices();

	kp=.8;
	ki=0;
	kd=50;
	V=420;
	const int dt = 50;	
		
	while(1)
	{
		_delay_ms(dt);
 		cli();
 		update_values();
 		sei();
		 
		//display_data();
						  		
		distance=sqrt(square(y_req-y_current)+square(x_req-x_current));
		
		V=(distance<100)?230:420;
		kp=(distance<100)?.4:.8;
		
		if(distance>15)
		{			
			er=theta_current-theta_req; //-360 to 360
			er = atan2(sin(er*3.14/180), cos(er*3.14/180))*(180/3.14); //-180 to 180
			
			integral= integral+er*dt;
			derivative = (er-previous_er)/dt;
			previous_er = er;
			
			w=kp*er + ki*integral + kd*derivative;
			v_left=((2*V+w*L)/(2*R));
			v_right=((2*V-w*L)/(2*R));
			
			lcd_print_neg(1,1,v_left,4);
			lcd_print_neg(1,9,v_right,4);
			velocity(v_left,v_right);
			//forward();
		}
		
		else
		{
			hard_stop();
		}
	}
}

