/*
 * motion.h
 *
 * Created: 5/26/2017 5:28:57 PM
 *  Author: Chirag
 */ 


#ifndef MOTION_H_
#define MOTION_H_

void motion_pin_config (void);
//void motion_set (unsigned char); //Function used for setting motor's direction
void forward (void);         //both wheels forward
void back (void);            //both wheels backward
void left (void);            //Left wheel backward, Right wheel forward
void right (void);           //Left wheel forward, Right wheel backward
void soft_left (void);       //Left wheel stationary, Right wheel forward
void soft_right (void);      //Left wheel forward, Right wheel is stationary
void soft_left_2 (void);     //Left wheel backward, right wheel stationary
void soft_right_2 (void);    //Left wheel stationary, Right wheel backward
void hard_stop (void);		 //hard stop(stop suddenly)
void soft_stop (void);       //soft stop(stops solowly)



#endif /* MOTION_H_ */