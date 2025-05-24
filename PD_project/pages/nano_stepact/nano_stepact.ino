int r1 = 10;
int r2 = 9;

const int pul = 8;
const int dir = 7;
const int ena = 6;

const int start = 4;

int i=0;
int speed = 2.5;


void setup() {
  pinMode(r1,OUTPUT);
  pinMode(r2,OUTPUT);

  pinMode(ena,OUTPUT);
  pinMode(dir,OUTPUT);
  pinMode(pul,OUTPUT);

  pinMode(start,OUTPUT);

  //enable stepper
  digitalWrite(ena, 0);


  //relay|actuator init
  digitalWrite(r1, 1);
  digitalWrite(r2, 0);
}

void loop() {
  if (digitalRead(start)==1){
    digitalWrite(pul,0);
    delay(speed);
    i=i+speed;
    if (i>4500){
      int temp = r1;
      r1 = r2; r2 = temp;
      i=0;
      digitalWrite(r1,1);
      digitalWrite(r2,0);
      }
    digitalWrite(pul,1);
    delay(speed);
    i=i+speed;
    if (i>4500){
      int temp = r1;
      r1 = r2; r2 = temp;
      i=0;
      digitalWrite(r1,1);
      digitalWrite(r2,0);
      }    
    }
}
