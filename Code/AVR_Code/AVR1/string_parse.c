/*
 * string_parse.c
 *
 * Created: 5/30/2017 10:17:12 AM
 *  Author: Chirag
 */ 

#include <string.h>
#include "LCD.h"
#include <stdlib.h>

extern volatile char data_string[][40];  //to store received data from UDR

extern int id;
extern int id_var;
extern int x_current;
extern int y_current;
extern int theta_current;
extern int x_req;
extern int y_req;
extern int theta_req;
extern int trigger;
extern int trigger_angle;

/*
* Function Name display_data_string
* Input: None
* Output: Last valid string received from the microcontroller is displayed on the LCD
* Example Call: display_data_string()
*/
void display_data_string()
{
	char data_string1[40];
	strcpy((char*) data_string1, (const char*)data_string);
	lcd_string2(1,1,data_string1);
}

/*
* Function Name display_data
* Input: None
* Output: All the current and required states of the robot are displayed on the microcontroller
* Example Call: display_data()
*/
void display_data()
{
	lcd_print(1,1,id_var,3);
	lcd_print(1,5,x_current,3);
	lcd_print(1,9,y_current,3);
	lcd_print(1,13,theta_current,3);
	lcd_print(2,1,x_req,3);
	lcd_print(2,5,y_req,3);
	lcd_print(2,9,theta_req,3);
}

/*
* Function Name update_values
* Input: None
* Output: The received string is parsed to update the values
* Logic: The string is parsed to obtain the integer values.
		 The string is split into a 2D array using strchr function.
		 The strings are then converted to integer type using atoi function.
* Example Call: update_values()
*/
void update_values()
{
	char parts[10][5];
	char data_string1[40];
	strcpy((char*)data_string1, (const char*)data_string);
	
	char *p_start, *p_end;
	unsigned char i=0;
	p_start = data_string1;
	
	//Split the data_string1 into parts which are separated by a /
		while(1) 
		{
			p_end = strchr(p_start, '/');
			if (p_end)
			{
				strncpy(parts[i], p_start, p_end-p_start);
				parts[i][p_end-p_start] = 0;
				i++;
				p_start = p_end + 1;
			}
			else
			break;
		}
		
		//If you want a checksum at the end of the data string 
		int checksum = 0;
		for(int i = 1;i<=8; i++)	//does not add id
		{
			checksum = checksum + atoi(parts[i]);
		}
		
		//Convert the string to int using atoi function
		if (1)//(checksum == atoi(parts[9]))	//If you want a checksum at the end of the data string
		{
			//id_var = atoi(parts[0]);
			x_current = atoi(parts[1]);
			y_current = atoi(parts[2]);
			theta_current = abs(atoi(parts[3])-360+180-360); //(0)-(360)
			x_req = atoi(parts[4]);
			y_req = atoi(parts[5]);
			theta_req = abs(atoi(parts[6])-180-360); //(0)-(360)
			trigger = atoi(parts[7]);
			trigger_angle = atoi(parts[8]);
		}
}

/*
* Function Name check_id
* Input: The address of the index 0 of the data string of whose id you want to check
* Output: Returns 1 if id matches, returns 0 if id does not match with the actual id of the robot.
* Logic: The string is parsed to obtain the id string.
		 The string is split into a 2D array using strchr function.
		 The string is then converted to integer type using atoi function.
* Example Call: check_id(data_string)
*/
int check_id(char *p_start)
{
		char parts[2][5];
		char *p_end;
		unsigned char i=0;
		
		//while(1)
		//{
			p_end = strchr(p_start, '/');
			if (p_end)
			{
				strncpy(parts[i], p_start, p_end-p_start);
				parts[i][p_end-p_start] = 0;
				i++;
				p_start = p_end + 1;
			}
			//else
			//break;
		//}
		
		if (atoi(parts[0])==id)
		{
			return 1;
		}
	return 0;
}