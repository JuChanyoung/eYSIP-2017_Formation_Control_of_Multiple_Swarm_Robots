/*
 * string_parse.c
 *
 * Created: 5/30/2017 10:17:12 AM
 * Author: Chirag
 */ 

#include <string.h>
#include "LCD.h"

extern volatile char data;  //to store received data from UDR0
extern volatile char flag_instruction;
extern volatile char data_string[100];  //to store received data from UDR
extern char data_string1[100];

extern int id_var;
extern int x;
extern int y;
extern int theta;

/*
Name: display_data_string
Input: None
Output: Displays the string last received from XBee
Example Call: display_data_string();
*/
void display_data_string()
{
	strcpy(data_string1, data_string);
	lcd_cursor(2,1);
	lcd_string(data_string1);
}

/*
Name: update_values
Input: None
Output: Updates the  id, x, y, theta valuesand displayes them on the LCD
Example Call: update_values();
*/
void update_values()
{
	char parts[4][10];
	strcpy(data_string1, data_string);
	
	char *p_start, *p_end;
	char i=0;
	p_start = data_string1;
	
	//display_data_string();
	
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
		
	id_var = atoi(parts[0]);
	x = atoi(parts[1]);
	y = atoi(parts[2]);
	theta = atoi(parts[3]);
	
	//lcd_clear();
	lcd_print(1,1,id_var,3);
	lcd_print(1,5,x,3);
	lcd_print(2,1,y,3);
	lcd_print(2,5,theta,3);
}

