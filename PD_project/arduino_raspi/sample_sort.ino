#include <SoftwareSerial.h>

// Stepper motor control pins
const int motor_step = 11;
const int motor_dir = 12;
const int motor_ena = 13;

// Color sensor pins
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8

// Serial communication with Raspberry Pi
SoftwareSerial mySerial(10, 11);

int redFreq, greenFreq, blueFreq;
int targetVariety = 0;

void setup() {
    Serial.begin(9600);
    mySerial.begin(9600);

    pinMode(motor_step, OUTPUT);
    pinMode(motor_dir, OUTPUT);
    pinMode(motor_ena, OUTPUT);

    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(sensorOut, INPUT);
    
    // Set color sensor scaling to 20% output frequency
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);

    // Disable stepper motor at startup
    digitalWrite(motor_ena, HIGH);
}

void loop() {
    if (mySerial.available()) {
        String receivedData = mySerial.readStringUntil('\n');  // Read signal from Raspberry Pi
        receivedData.trim();
        targetVariety = receivedData.toInt();

        Serial.print("Received variety: ");
        Serial.println(targetVariety);

        if (targetVariety == 0) {
            stopStepper();  // Stop motor if no signal
        } else {
            runStepper();  // Move motor if signal is received
        }
    }
}

void runStepper() {
    digitalWrite(motor_ena, LOW);  // Enable stepper motor

    Serial.println("Stepper running");

    digitalWrite(motor_dir, HIGH);
    for (int i = 0; i < 200; i++) {  // Rotate stepper motor
        digitalWrite(motor_step, HIGH);
        delayMicroseconds(1000);
        digitalWrite(motor_step, LOW);
        delayMicroseconds(1000);
    }

    int detectedColor = readColorSensor();  // Read color sensor
    Serial.print("Detected color variety: ");
    Serial.println(detectedColor);

    if (detectedColor == targetVariety) {
        stopStepper();  // Stop motor if color matches variety
    }
}

void stopStepper() {
    Serial.println("Stepper stopped");
    digitalWrite(motor_ena, HIGH);  // Disable stepper motor
}

int readColorSensor() {
    // Read Red Component
    digitalWrite(S2, LOW);
    digitalWrite(S3, LOW);
    redFreq = pulseIn(sensorOut, LOW);

    // Read Green Component
    digitalWrite(S2, HIGH);
    digitalWrite(S3, HIGH);
    greenFreq = pulseIn(sensorOut, LOW);

    // Read Blue Component
    digitalWrite(S2, LOW);
    digitalWrite(S3, HIGH);
    blueFreq = pulseIn(sensorOut, LOW);

    Serial.print("R: "); Serial.print(redFreq);
    Serial.print(" G: "); Serial.print(greenFreq);
    Serial.print(" B: "); Serial.println(blueFreq);

    if (redFreq < greenFreq && redFreq < blueFreq) {
        return 1;  // Red
    } 
    else if (greenFreq < redFreq && greenFreq < blueFreq) {
        return 2;  // Green
    } 
    else if (blueFreq < redFreq && blueFreq < greenFreq) {
        return 3;  // Blue
    } 
    else if (redFreq > 300 && greenFreq > 300 && blueFreq > 300) {  
        return 5;  // Black
    } 
    else if (redFreq < 150 && greenFreq < 150 && blueFreq < 150) {  
        return 4;  // White
    } 
    else {
        return 0;  // Unknown
    }
}
