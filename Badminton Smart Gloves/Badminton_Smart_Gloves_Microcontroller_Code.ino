#include <MPU9250.h>
#include <Wire.h>  
#define FORCE_SENSOR_PIN A0 // the FSR and 10K pulldown are connected to A2

const float VCC = 5;   
const float R_DIV = 63000.0; // resistor used to create a voltage divider
const float flatResistance = 25000.0; // resistance when flat
const float bendResistance = 125000.0; // resistance at 90 deg
MPU9250 IMU (Wire , 0x68);


void setup() {
  Serial.begin(9600);
  pinMode(A2, INPUT);
  pinMode(A1  , INPUT);
  IMU.begin();
  Serial.println("CLEARDATA");
  Serial.println("LABEL, ,aX,aY,aZ,Temp,gX,gY,gZ,mX,mY,mZ,Flex1 R,Flex1 D, Flex2 R, Flex2 D,Force Value ,Force State");
  Serial.println("RESETTIMER");

  
  
}
void loop() {

  IMU.readSensor();
  //Accelerometer data code

  Serial.print("DATA, ");
  Serial.print(" , ");
  Serial.print(IMU.getAccelX_mss(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getAccelY_mss(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getAccelZ_mss(), 3);
  Serial.print(" , ");

  //Temp
  
  Serial.print(IMU.getTemperature_C(), 2);

  //Gyroscope data code
  
  Serial.print(" , ");
  Serial.print(IMU.getGyroX_rads(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getGyroY_rads(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getGyroZ_rads(), 3);
  Serial.print(" , ");
  
  //Magnetometer data code

  Serial.print(IMU.getMagX_uT(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getMagY_uT(), 3);
  Serial.print(" , ");
  Serial.print(IMU.getMagZ_uT(), 3);
  Serial.print(" , ");



     // Read the ADC, and calculate voltage and resistance from it (1)
 int ADCflex = analogRead(A2);
 float Vflex = ADCflex * VCC / 1023.0;
 float Rflex = R_DIV * (VCC / Vflex - 1.0);
 Serial.print(Rflex);
 Serial.print(" , ");


 // Use the calculated resistance to estimate the sensor's bend angle: (1)
 float angle = map(Rflex, flatResistance, bendResistance, 0, 90.0);
 Serial.print(angle);
 Serial.print(" , ");

     // Read the ADC, and calculate voltage and resistance from it (2)

 int ADCflex2 = analogRead(A1);
 float Vflex2 = ADCflex2 * VCC / 1023.0;
 float Rflex2 = R_DIV * (VCC / Vflex2 - 1.0);
 Serial.print(Rflex2);
 Serial.print(" , ");

 // Use the calculated resistance to estimate the sensor's bend angle: (2)
 float angle2 = map(Rflex2, flatResistance, bendResistance, 0, 90.0);
 Serial.print(angle2);
 Serial.print(" , ");
 
  int analogReading = analogRead(FORCE_SENSOR_PIN);

  Serial.print(analogReading); // print the raw analog reading
  Serial.print(" , ");
  if ((analogReading) < (10))       // from 0 to 9
    Serial.print("no pressure");
  else if ((analogReading) < 200) // from 10 to 199
    Serial.print("light touch");
  else if ((analogReading) < 500) // from 200 to 499
    Serial.print("light squeeze");
  else if ((analogReading) < 800) // from 500 to 799
    Serial.print("medium squeeze");
  else // from 800 to 1023
    Serial.print("big squeeze");

 
 Serial.println(" , "); 
  // delay
  delay(1000);
}
