//read pin assignments
const int startPin = A2;
const int enaPin = A1;
const int v1Pin = A3;
const int v2Pin = A4;
const int v3Pin = A5;

//ir
const int ir = A0;

// conveyor pin assignments
const int motor_step = 11;
const int motor_dir = 12;
const int motor_ena = 13;

int readVar(){
  int variety = 0;
  float v1 = digitalRead(v1Pin);
  float v2 = digitalRead(v2Pin);
  float v3 = digitalRead(v3Pin);
  
  if (v1==1) variety += 1;
  if (v2==1) variety += 2;
  if (v3==1) variety += 4;
  
  return variety;
}

  


int det_step(int var, int position){
    int step;
    int dist = var - position; 
    
    if      ((dist == 1) ||(dist == -4)) step =1;
    else if ((dist == 2) ||(dist == -3)) step =2;
    else if ((dist == 3) ||(dist == -2)) step =-2;
    else if ((dist == 4) ||(dist == -1)) step =-1;
    else step = 0;
    
    return step;
  }

void run(){
int vel = 700;
int cal = 100;
  for (int x = 0; x< cal; x++){
    digitalWrite(motor_step,HIGH);
    delayMicroseconds(vel);
    digitalWrite(motor_step,LOW);
    delayMicroseconds(vel);
  }   
}

//setup var
int start, ena, v1, v2, v3, var, steps, irval;

int position = 1;
int taken = 0;
bool extra;

void setup() {
  Serial.begin(9600);
  
//sensor
  pinMode(ir, INPUT);
  
//motors
  pinMode(motor_ena, OUTPUT);
  pinMode(motor_step, OUTPUT);
  pinMode(motor_dir, OUTPUT);

  pinMode(startPin, INPUT);
  pinMode(v1Pin, INPUT);
  pinMode(v2Pin, INPUT);
  pinMode(v3Pin, INPUT);

  digitalWrite(motor_ena, LOW);

  Serial.println("Setup Complete");
}

void loop() {
  
  start = digitalRead(startPin);
  var = readVar();

  if (start == 1 && var!= 0){


    steps = det_step(var,position);

    Serial.println("-------------");
    Serial.print("To sort:");
    Serial.println(var);
    Serial.print("Position:");
    Serial.println(position);
    Serial.print("Steps:");
    Serial.println(steps);

    if (steps>0){
      digitalWrite(motor_dir, LOW);
      steps = steps * 2;
      extra = false;
    }
    else if(steps <0){
      digitalWrite(motor_dir, HIGH);
      steps = abs(steps);
      steps = (steps * 2)+1;
      extra = true;
      }
      
  
    irval = 0; 
    while (taken < steps){
      if (digitalRead(ir) != irval){
        irval = !irval;
        taken = taken+1;
        }
      run();
    }  
    if (extra){
      digitalWrite(motor_dir, LOW);
      while (digitalRead(ir) == 1) run();
      extra = false;  
    }

    position = var;
    taken = 0;
    Serial.println("Done");
    Serial.println();

  }
  else
  {
    Serial.println("Down");
  }
}
      
