/*
 * string_parse.c
 *
 * Created: 5/30/2017 10:17:12 AM
 *  Author: Chirag
 */ 

#include <string.h>
#include "LCD.h"
#include <stdlib.h>

extern volatile char data_string[100];  //to store received data from UDR

extern int id;
extern int id_var;
extern int x_current;
extern int y_current;
extern int theta_current;
extern int x_req;
extern int y_req;
extern int theta_req;

extern volatile char data_string_var[100];

void display_data_string()
{
	char data_string1[100];
	strcpy(data_string1, data_string);
	lcd_cursor(2,1);
	lcd_string(data_string1);
}

void display_data()
{
	lcd_print(1,1,x_current,3);
	lcd_print(1,5,y_current,3);
	lcd_print(1,9,theta_current,3);
}

void update_values()
{
	char parts[7][10];
	char data_string1[100];
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
	if(id_var==id)	
	{
		x_current = atoi(parts[1]);
		y_current = atoi(parts[2]);
		theta_current = abs(atoi(parts[3])-360+180-360); //(0)-(360)
		x_req = atoi(parts[4]);
		y_req = atoi(parts[5]);
		theta_req = abs(atoi(parts[6])-180-360); //(0)-(360)
	}
	
	//lcd_clear();
	/*
	lcd_print(1,1,id_var,3);
	lcd_print(1,5,x_current,3);
	lcd_print(1,9,y_current,3);
	lcd_print(1,13,theta_current,3);
	lcd_print(2,5,x_req,3);
	lcd_print(2,9,y_req,3);
	lcd_print(2,13,theta_req,3);
	*/
}

int check_id(char *p_start)
{
		char parts[2][5];
		//char data_string1[10];
		//strcpy(data_string1, data_string_var);
		
		//char *p_start, *p_end;
		char *p_end;
		char i=0;
		//p_start = data_string1;
		
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
		
		if (atoi(parts[0])==id)
		{
			return 1;
		}
	return 0;
}