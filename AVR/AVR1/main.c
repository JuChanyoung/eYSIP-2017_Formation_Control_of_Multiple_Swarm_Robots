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
int er,v_left,v_right,L,R,V;
float w;
float kp;
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

	kp=0.1;
	V=100;
	R=3.5;
	L=11.5;
		
	while(1)
	{
		_delay_ms(100);
 		cli();
 		update_values();
 		sei();
						  		
		distance=sqrt(square(y_req-y_current)+square(x_req-x_current));
		float er2=theta_current-theta_req; //-360 to 360
		
		er2 = atan2(sin(er2*3.14/180), cos(er2*3.14/180))*(180/3.14); //-180 to 180
		w=kp*er2;
		
		if(distance>50)
		{
			//lcd_home();
			//lcd_string("left   ");
			v_left=((2*V+w*L)/(2*R));
			v_right=((2*V-w*L)/(2*R));
			velocity(v_left,v_right);
			forward();
		}
		
		else
		{
			hard_stop();
			//lcd_clear();
			//lcd_home();
			//lcd_string("Stopped");
		}
	}
}

