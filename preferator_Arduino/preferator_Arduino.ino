unsigned long interval=1000;
unsigned long duration1=300; //durations must be less than interval
unsigned long duration2=300;
unsigned long duration3=300;
unsigned long duration4=300;

#include <CapacitiveSensor.h>
CapacitiveSensor cs_1 = CapacitiveSensor(7,8);
CapacitiveSensor cs_2 = CapacitiveSensor(7,6);
CapacitiveSensor cs_3 = CapacitiveSensor(7,2);
CapacitiveSensor cs_4 = CapacitiveSensor(7,11);

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

long c3_thresh;
long c3;
int licks3;
int drinks3;
bool drink3_primed=true;
bool drink3_finished=true;
unsigned long t_drink3;

long c4_thresh;
long c4;
int licks4;
int drinks4;
bool drink4_primed=true;
bool drink4_finished=true;
unsigned long t_drink4;

const int threshold_increment=3000;
const int drink1=A0;
const int drink2=A1;
const int drink3=A2;
const int drink4=A3;
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
  pinMode(drink3,OUTPUT);
  digitalWrite(drink3,LOW);
  digitalWrite(drink3,HIGH);
  
  pinMode(drink4,OUTPUT);
  digitalWrite(drink4,LOW);
  digitalWrite(drink4,HIGH);
  delay(500);
  long c1 = cs_1.capacitiveSensor(100);
  c1_thresh=c1+threshold_increment;
  licks1=0;
  drinks1=0;
  long c2 = cs_2.capacitiveSensor(100);
  c2_thresh=c2+threshold_increment;
  licks2=0;
  drinks2=0;
  
  long c3 = cs_3.capacitiveSensor(100);
  c3_thresh=c3+threshold_increment;
  licks3=0;
  drinks3=0;
  long c4 = cs_4.capacitiveSensor(100);
  c4_thresh=c4+threshold_increment;
  licks4=0;
  drinks4=0;
  
  digitalWrite(led,LOW);
//  Serial.print("cs_threshold   ");//show value for trouble shooting if serial monitor is on
//  Serial.println(c1_thresh); 
//  Serial.println(c2_thresh);
//  Serial.println(c3_thresh); 
//  Serial.println(c4_thresh);

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
      Serial.print(licks3);Serial.print(",");Serial.print(drinks3);Serial.print(",");
      Serial.print(licks4);Serial.print(",");Serial.print(drinks4);Serial.println(",");
      licks3=0;drinks3=0;licks4=0;drinks4=0;
    }
    if (receivedChar=='e')
    {
      digitalWrite(drink3,LOW);
      digitalWrite(drink4,HIGH);
      digitalWrite(drink1,HIGH);
      digitalWrite(drink2,HIGH);
     
    }
    if (receivedChar=='f')
    {
      digitalWrite(drink3,HIGH);
      digitalWrite(drink4,LOW);
      digitalWrite(drink1,HIGH);
      digitalWrite(drink2,HIGH);
     
    }
    if (receivedChar=='g')
    {
      digitalWrite(drink3,HIGH);
      digitalWrite(drink4,HIGH);
      digitalWrite(drink1,LOW);
      digitalWrite(drink2,HIGH);
     
    }
    if (receivedChar=='h')
    {
      digitalWrite(drink3,HIGH);
      digitalWrite(drink4,HIGH);
      digitalWrite(drink1,HIGH);
      digitalWrite(drink2,LOW);
     
    }
    if (receivedChar=='i')
    {
      digitalWrite(drink3,HIGH);
      digitalWrite(drink4,HIGH);
      digitalWrite(drink1,HIGH);
      digitalWrite(drink2,HIGH);
     
    }
  }
}

void Exp() {
  now=millis();
  c1 = cs_1.capacitiveSensor(3);
//  Serial.println(c1);
  if (c1>c1_thresh)
  {
    licks1++;digitalWrite(led,HIGH);
    if (drink1_primed){digitalWrite(drink1,LOW);t_drink1=millis();drinks1++;drink1_primed=false;drink1_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink1_primed) && (!drink1_finished) && (t_drink1+duration1<now)) {digitalWrite(drink1,HIGH);drink1_finished=true;}
  if((!drink1_primed) && (drink1_finished) && (t_drink1+interval<now)) {drink1_primed=true;}
  
  c2 = cs_2.capacitiveSensor(3);
//  Serial.println(c2);
  if (c2>c2_thresh)
  {
    licks2++;digitalWrite(led,HIGH);
    if (drink2_primed){digitalWrite(drink2,LOW);t_drink2=millis();drinks2++;drink2_primed=false;drink2_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink2_primed) && (!drink2_finished) && (t_drink2+duration2<now)) {digitalWrite(drink2,HIGH);drink2_finished=true;}
  if((!drink2_primed) && (drink2_finished) && (t_drink2+interval<now)) {drink2_primed=true;}

  c3 = cs_3.capacitiveSensor(3);
//  Serial.println(c3);
  if (c3>c3_thresh)
  {
    licks3++;digitalWrite(led,HIGH);
    if (drink3_primed){digitalWrite(drink3,LOW);t_drink3=millis();drinks3++;drink3_primed=false;drink3_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink3_primed) && (!drink3_finished) && (t_drink3+duration3<now)) {digitalWrite(drink3,HIGH);drink3_finished=true;}
  if((!drink3_primed) && (drink3_finished) && (t_drink3+interval<now)) {drink3_primed=true;}
  
  c4 = cs_4.capacitiveSensor(3);
//  Serial.println(c4);
  if (c4>c4_thresh)
  {
    licks4++;digitalWrite(led,HIGH);
    if (drink4_primed){digitalWrite(drink4,LOW);t_drink4=millis();drinks4++;drink4_primed=false;drink4_finished=false;}
  }
  else{digitalWrite(led,LOW);}
  if((!drink4_primed) && (!drink4_finished) && (t_drink4+duration4<now)) {digitalWrite(drink4,HIGH);drink4_finished=true;}
  if((!drink4_primed) && (drink4_finished) && (t_drink4+interval<now)) {drink4_primed=true;}
}
