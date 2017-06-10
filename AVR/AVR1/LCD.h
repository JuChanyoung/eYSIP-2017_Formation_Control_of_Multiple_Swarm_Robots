/*
 * LCD.h
 *
 * Created: 5/27/2017 6:05:58 PM
 *  Author: Chirag
 */ 


#ifndef LCD_H_
#define LCD_H_

void lcd_port_config();
void lcd_init();
void init_ports();
void lcd_init();
void lcd_wr_char(char);
void lcd_line1();
void lcd_line2();
void lcd_print (char, char, unsigned int, int);
void lcd_string(char*);
void lcd_home();
void lcd_clear(void);
void lcd_cursor (char, char);

void lcd_print_neg(char , char , int , int);


#endif /* LCD_H_ */