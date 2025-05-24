//ir
const int ir = A0;

// conveyor pin assignments
const int motor_step = 11;
const int motor_dir = 12;
const int motor_ena = 13;

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

int steps = 2;
int start = 0;
int taken = 0;
bool extra;
void setup() {
  pinMode(motor_ena, OUTPUT);
  pinMode(motor_step, OUTPUT);
  pinMode(motor_dir, OUTPUT);
  pinMode(ir, INPUT);
  digitalWrite(motor_ena, LOW);
  
  if (steps>0){
    digitalWrite(motor_dir, LOW);
    steps = steps * 2;
    extra = false;
  }
  else{
    digitalWrite(motor_dir, HIGH);
    steps = abs(steps);
    steps = (steps * 2)+1;
    extra = true;
    }
}

void loop() {
  while (taken < steps){
    if (digitalRead(ir)!= start){
      start = !start;
      taken = taken +1;
      }  
    run();}
if (extra){
    digitalWrite(motor_dir, LOW);
    while (digitalRead(ir) == 1) run();
    extra = false;  
  }
}    
