
#include "DHT.h"  //DHT sensor Library

#define DHTPIN 12  //Define sensor pin(pin 12)
#define DHTTYPE DHT22  //What sensor use

DHT dht(DHTPIN, DHTTYPE);//Create sensor object

//boolean a=LOW,b=HIGH;
float h=0,t=0;
int fan = 3; //LED pins for temperature control 
int pump = 2;
long previousMillis = 0;
long interval = 2000; //Read sensor each 2 seconds

void setup() {

  pinMode(fan, OUTPUT);//Change to output my pins
  pinMode(pump, OUTPUT);
  dht.begin();//Start DHT22 sensor
  digitalWrite(pump,LOW);//Turn off pump
  digitalWrite(fan,LOW);//Turn off fan

}

void loop()
{
  unsigned long currentMillis = millis();//time elapsed
  if(currentMillis - previousMillis > interval) //Comparison between the elapsed time and the time in which the action is to be executed
  {
    previousMillis = currentMillis; //"Last time is now"

     h = dht.readHumidity();//humidity value
     t = dht.readTemperature();//temperature value centigrades if you want farenheit change to
     //t = dht.readTemperature(true);
     //Below is for print data sensors in lcd 
     
    if(t>=25 && a==LOW)//if temperature above of 25 degrees
    {
      digitalWrite(fan,HIGH);//Active air conditioner
      digitalWrite(pump,LOW);
      a=HIGH;
      b=LOW;
     
    }
    else if(t<=23&&b==LOW)//if temperature is under 23 degrees
    {
      digitalWrite(pump,HIGH);
      digitalWrite(fan,LOW);//Turn off air conditioner
      a=LOW;
      b=HIGH;
    }
    
  }
}
