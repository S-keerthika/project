#include<LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,6);
float value=0;
float rev=0;
int rpm;
int oldtime=0;
int time;
 
void isr() //interrupt service routine
{
rev++;
}
 
void setup()
{
  Serial.begin(9600);
  Serial.print(" \n please start the motor at least 3 seconds prior.\n");
  
  lcd.begin(16,2); //initialize LCD
  attachInterrupt(0,isr,RISING); //attaching the interrupt

}

void loop()
{
  delay(1000);
  detachInterrupt(0); //detaches the interrupt
  time=millis()-oldtime; //finds the time
  //Serial.println(time);
  rpm=((rev/3)/time)*60000; //calculates rpm for blades
  oldtime=millis();
  rev=0;
   
  Serial.print("\n The rpm is : "); 
  Serial.println( rpm );
  
  
  lcd.clear();
  lcd.setCursor(3,0);
  lcd.print("TACHOMETER");
  lcd.setCursor(4,1);
  lcd.print( rpm);
  lcd.print(" RPM");
  lcd.print(" ");
  
  
   //saves the current time
  attachInterrupt(0,isr,RISING);
}
