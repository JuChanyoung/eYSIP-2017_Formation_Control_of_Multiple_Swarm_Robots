/*
 * timer_init.c
 *
 * Created: 5/26/2017 5:50:06 PM
 *  Author: Chirag
 */ 

#include <avr/io.h>

//Timer1 is configured for constant frequency and variable duty cyclr
//TIMER1 initialize - prescale:64
// WGM: 5) PWM 8bit fast, TOP=0x00FF
// desired value: 450Hz
// actual value: 450.000Hz (0.0%)
void timer1_init(void)
{
	TCCR1B = 0x00; //stop
	TCNT1H = 0xFF; //higher byte constant frequency value of PWM cycle
	TCNT1L = 0x01; //lower byte constant frequency value of PWM cycle
	OCR1AH = 0x00;
	OCR1AL = 0xFF;
	OCR1BH = 0x00;
	OCR1BL = 0xFF;
	// ICR1H  = 0x00;
	// ICR1L  = 0xFF;
	TCCR1A = 0xA1;
	TCCR1B = 0x0D; //start Timer
}

