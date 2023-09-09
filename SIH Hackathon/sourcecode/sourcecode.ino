#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(2,3,4,5,6,7);
int tempPin = A0; // the output pin of LM35
int fan = 11; // the pin where fan is
int led = 8; // led pin
int temp;
int tempMin = 30; // the temperature to start the fan 0%
int tempMax = 60; // the maximum temperature when fan is at 100%
int fanSpeed;
int fanLCD;
Servo servohori; //horizontal servo(BOTTOM SERVO)
int servoh = 0; //assign servo at 0 degree
int servohLimitHigh = 180; //maximum range of servo is 180 degree(it is variable you can also change)
int servohLimitLow = 10;   //minimum range of servo is 10 degree(it is variable you can also change)

Servo servoverti; //vertical servo(TOP SERVO) 
int servov = 0; 
int servovLimitHigh = 180;
int servovLimitLow = 10;

int ldrtopr = 1; //top right LDR A1 pin
int ldrtopl = 2; //top left LDR A2 pin

int ldrbotr = 0; // bottom right LDR A0 pin
int ldrbotl = 3; // bottom left LDR A3 pin


void setup () 
 {
  servohori.attach(10); //horizontal servo connected to arduino pin 10
  servohori.write(0);
  
  servoverti.attach(9); //vertical servo connected to arduino pin 9
  servoverti.write(0);
  delay(500); //delay
  pinMode(fan, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(tempPin, INPUT);
   lcd.begin(16,2);
  Serial.begin(9600);
 }

void loop()
{
  servoh = servohori.read();
  servov = servoverti.read();
  
  
  int topl = analogRead(ldrtopl); //read analog values from top left LDR
  int topr = analogRead(ldrtopr); //read analog values from top right LDR
  int botl = analogRead(ldrbotl); //read analog values from bottom left LDR
  int botr = analogRead(ldrbotr); //read analog values from bottom right LDR
  
  
  int avgtop = (topl + topr) / 2; //average of top LDRs
  int avgbot = (botl + botr) / 2; //average of bottom LDRs
  int avgleft = (topl + botl) / 2; //average of left LDRs
  int avgright = (topr + botr) / 2; //average of right LDRs

  if (avgtop < avgbot)
  {
    servoverti.write(servov -1);
    if (servov > servovLimitHigh) 
     { 
      servov = servovLimitHigh;
     }
    delay(8);
  }
  else if (avgbot < avgtop)
  {
    servoverti.write(servov +1);
    if (servov < servovLimitLow)
  {
    servov = servovLimitLow;
  }
    delay(8);
  }
  else 
  {
    servoverti.write(servov);
  }
  
  if (avgleft > avgright)
  {
    servohori.write(servoh -1);
    if (servoh > servohLimitHigh)
    {
    servoh = servohLimitHigh;
    }
    delay(8);
  }
  else if (avgright > avgleft)
  {
    servohori.write(servoh +1);
    if (servoh < servohLimitLow)
     {
     servoh = servohLimitLow;
     }
    delay(8);
  }
  else 
  {
    servohori.write(servoh); // write means run servo
  }
  delay(50);
  temp = readTemp(); // get the temperature
  Serial.print( temp );
  if(temp < tempMin) // if temp is lower than minimum temp
  {
    fanSpeed = 0; // fan is not spinning
    analogWrite(fan, fanSpeed);
    fanLCD=0;
    digitalWrite(fan, LOW);
  }
  if((temp >= tempMin) && (temp <= tempMax)) // if temperature is higher than minimum temp
  {
  fanSpeed = temp;//map(temp, tempMin, tempMax, 0, 100); // the actual speed of fan//map(temp, tempMin, tempMax, 32, 255);
  fanSpeed=1.5*fanSpeed;
  fanLCD = map(temp, tempMin, tempMax, 0, 100); // speed of fan to display on LCD100
  analogWrite(fan, fanSpeed); // spin the fan at the fanSpeed speed
  }
   
  if(temp > tempMax) // if temp is higher than tempMax
  {
  digitalWrite(led, HIGH); // turn on led
  }
  else // else turn of led
  {
  digitalWrite(led, LOW);
  }
   
  lcd.print("TEMP: ");
  lcd.print(temp); // display the temperature
  lcd.print("C ");
  lcd.setCursor(0,1); // move cursor to next line
  lcd.print("FANS: ");
  lcd.print(fanLCD); // display the fan speed
  lcd.print("%");
  delay(200);
  lcd.clear();
  }
   
  int readTemp() { // get the temperature and convert it to celsius
  temp = analogRead(tempPin);
  return temp * 0.48828125;
}








 

 
