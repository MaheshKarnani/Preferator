unsigned long interval=1000;
unsigned long duration=300;

#include <CapacitiveSensor.h>
CapacitiveSensor cs_1 = CapacitiveSensor(7,2);
CapacitiveSensor cs_2 = CapacitiveSensor(7,11);
long c1_thresh;
long c1;
int licks1;
int drinks1;
bool drink1_primed=true;
bool drink1_finished=true;
unsigned long t_drink1;
unsigned long now;
long c2_thresh;
long c2;
int licks2;
int drinks2;
bool drink2_primed=true;
bool drink2_finished=true;
unsigned long t_drink2;
const int threshold_increment=1000;
const int drink1=A0;
const int drink2=A1;
const int led=13;

char receivedChar;

void setup() {
  Serial.begin(115200);//setup serial
  pinMode(led,OUTPUT);
  digitalWrite(led,HIGH);
  pinMode(drink1,OUTPUT);
  digitalWrite(drink1,LOW);
  digitalWrite(drink1,HIGH);
  t_drink1=millis()-interval;
  pinMode(drink2,OUTPUT);
  digitalWrite(drink2,LOW);
  digitalWrite(drink2,HIGH);
  delay(500);
  long c1 = cs_1.capacitiveSensor(100);
  c1_thresh=c1+threshold_increment;
  licks1=0;
  drinks1=0;
  long c2 = cs_2.capacitiveSensor(100);
  c2_thresh=c2+threshold_increment;
  licks2=0;
  drinks2=0;
  digitalWrite(led,LOW);
//  Serial.print("cs_threshold   ");//show value for trouble shooting if serial monitor is on
//  Serial.println(c1_thresh); 
//  Serial.println(c2_thresh);
}

void loop() 
{
  Comms();
  Exp();
}

void Comms() {
  if (Serial.available()>0)
  {
    receivedChar = Serial.read();
    if (receivedChar=='a')
    {
      Serial.print(licks1);Serial.print(",");Serial.print(drinks1);Serial.print(",");
      Serial.print(licks2);Serial.print(",");Serial.print(drinks2);Serial.println(",");
      licks1=0;drinks1=0;licks2=0;drinks2=0;
    }
    if (receivedChar=='b')
    {
      Serial.println(licks2);
      Serial.println(drinks2);
      licks2=0;
      drinks2=0;
    }
  }
}

void Exp() {
  now=millis();
  c1 = cs_1.capacitiveSensor(100);
//  Serial.println(c1);
  if (c1>c1_thresh)
  {
    licks1++;digitalWrite(led,HIGH);
    if (drink1_primed){digitalWrite(drink1,LOW);t_drink1=millis();drinks1++;drink1_primed=false;drink1_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink1_primed) && (!drink1_finished) && (t_drink1+duration<now)) {digitalWrite(drink1,HIGH);drink1_finished=true;}
  if((!drink1_primed) && (drink1_finished) && (t_drink1+interval<now)) {drink1_primed=true;}
  
  c2 = cs_2.capacitiveSensor(100);
//  Serial.println(c2);
  if (c2>c2_thresh)
  {
    licks2++;digitalWrite(led,HIGH);
    if (drink2_primed){digitalWrite(drink2,LOW);t_drink2=millis();drinks2++;drink2_primed=false;drink2_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink2_primed) && (!drink2_finished) && (t_drink2+duration<now)) {digitalWrite(drink2,HIGH);drink2_finished=true;}
  if((!drink2_primed) && (drink2_finished) && (t_drink2+interval<now)) {drink2_primed=true;}
}
