#include <AccelStepper.h>
#define DRIVER 1

// conveyor pin assignments
const int enaPinC = 13;
const int dirPin1 = 12;
const int stepPin1 = 11;

// sorter pin assignments
const int enaPinS = 4;  
const int dirPin2 = 3;  
const int stepPin2 = 2; 

//read pin assignments
const int startPin = A0;
const int enaPin = A1;
const int v1pin = A2;
const int v2pin = A3;
const int v3pin = A4;

//relay pins
const int r1
const int r2
const int r3
const int r4

//ultrasonic
const int trigPin;  
const int echoPin;
int distance;

//
bool currentFull = false;

//setup motor
AccelStepper conveyor(DRIVER, stepPin1, dirPin1);
AccelStepper sorter(DRIVER, stepPin2, dirPin2);
int cSpeed = 500;
int sSpeed = 500;

//setup var
int start, ena, v1, v2, v3, var;
int position = 1;

//counters
int caneCount = 0, var1Count = 0, var2Count = 0, var3Count = 0, var4Count = 0, var5Count = 0;

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);
  
  
  // Enable both motors
  pinMode(enaPinC, OUTPUT);
  pinMode(enaPinS, OUTPUT);
  digitalWrite(enaPinC, LOW);  // LOW to enable motor 1
  digitalWrite(enaPinS, LOW);  // LOW to enable motor 2

  conveyor.setMaxSpeed(cSpeed);    // Max speed (steps per second)
  sorter.setMaxSpeed(sSpeed);    // Max speed (steps per second)
  

  // Set initial target positions
  conveyor.moveTo(200); // Move Motor 1 forward 200 steps
}

void loop() {
  
  start = analogRead(startPin);
  if (start > 0){

    //run conveyor
    conveyor.run();

    while (true){
      //keep conveyor running
      if (conveyor.distanceToGo() == 0 ) conveyor.moveTo(200); 

      releaseCane();

      start = analogRead(startPin);
      ena = analogRead(enaPin);

      while ( start>0 && !(enaPin>0){
        start = analogRead(startPin);
        ena = analogRead(enaPin);
        }
      if (!(start>0)){digitalWrite(enaPinC, HIGH); break;}
     
      else if (enaPin > 0){
        var = readVar();
        positionSorter(var);
        sorter.run();
        position = var;
        caneCount++;
        updateVarCount(var);

        
        if (conveyor.distanceToGo() == 0 ) conveyor.moveTo(200); 


        distance=readUltrasonic();
        while (distance>10){
          distance=readUltrasonic();}

        if (currentFull){
          sorter.setMaxSpeed(s2Speed); sorter.moveTo(40);
          emptyContainer()
          sorter.setMaxSpeed(-s2Speed); sorter.moveTo(40);}
      }
    }
  }
}



int readVar(){
  int variety = 0;
  float v1 = analogRead(v1pin)
  float v2 = analogRead(v2pin)
  float v3 = analogRead(v3pin)

  if (v1 > 0){
    if (v3 > 0){variety = 5;}
    else {variety = 4;}
  }
  else{
    if (v2 > 0){
      if(v3>0){variety = 3;}
      else{variety = 2;}

    }
    else {variety = 1;}
      }

  return variety;
}

void releaseCane(){

  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW);
  delay(5000);
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH);
  delay(5000);
}
  
void emptyContainer(){

  digitalWrite(r3,HIGH);
  digitalWrite(r4,LOW);
  delay(5000);
  digitalWrite(r3,LOW);
  digitalWrite(r4,HIGH);
  delay(5000);
}

void positionSorter(int var){
  
    int toGo = position - var;

    if (toGo = 1 || toGo == -4) {sorter.setMaxSpeed(s2Speed); sorter.moveTo(40);}
    else if (toGo = 2 || toGo == -3) {sorter.setMaxSpeed(s2Speed); sorter.moveTo(80);}
    else if (toGo = -1 || toGo == 4) {sorter.setMaxSpeed(-s2Speed);  sorter.moveTo(40);}
    else if (toGo = -2 || toGo == 3) {sorter.setMaxSpeed(-sSpeed);  sorter.moveTo(80);}

  }

void updateVarCount(int var){
  switch (var){
    case 1:
      var1Count++;
      if (var1Count == 50) currentFull = true;
      break;
        
    case 2:
      var2Count++;
      if (var2Count == 50) currentFull = true;
      break;

    case 3:
      var3Count++;
      if (var3Count == 50) currentFull = true;    
      break;
      
    case 4:
      var4Count++;
      if (var4Count == 50) currentFull = true;      
      break;
      
    case 5:
      var5Count++;
      if (var5Count == 50) currentFull = true;
      break;
    }
  
}

float readUltrasonic(){

  long duration;  // Variable to store the duration of the sound wave travel
  int distance;   // Variable to store the calculated distance

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

   duration = pulseIn(echoPin, HIGH);

  // Calculate the distance (in cm)
  distance = duration * 0.034 / 2;

  return distance;
  }
