//read pin assignments
const int startPin = A2;
const int v1Pin = A3;
const int v2Pin = A4;
const int v3Pin = A5;


//setup var
int start, var, v1, v2, v3;

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



void setup() {
  Serial.begin(9600);
  pinMode(startPin, INPUT);
  pinMode(v1Pin, INPUT);
  pinMode(v2Pin, INPUT);
  pinMode(v3Pin, INPUT);
  
  
  Serial.println("Setup Complete");

}

void loop() {


  var = readVar();
  Serial.println("-----------------");
  Serial.print("start:  ");
  Serial.println(digitalRead(startPin));  
  
  Serial.print("var:   ");
  Serial.println(var);

  
  v1 = digitalRead(v1Pin);
  Serial.print("v1: ");
  Serial.println(v1);

  
  v2 = digitalRead(v2Pin);
  Serial.print("v2: ");
  Serial.println(v2);

  
  v3 = digitalRead(v3Pin);
  Serial.print("v3: ");
  Serial.println(v3);
  
  Serial.println("-----------------");
  
  delay(1000);
  
}
