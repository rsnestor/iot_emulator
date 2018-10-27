const int sensorPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.print("Sensor: "); Serial.print(sensorValue);

  float voltage = (sensorValue*5.0)/1024.0;
  Serial.print(" ["); Serial.print(voltage);

  float temperature = (voltage - 0.879)*100.0;
  Serial.print("]\ttemp (C): "); Serial.print(temperature);
  
  float temperatureF = (temperature * 9.0 / 5.0) + 32.0;
  Serial.print("\ttemp (F): "); Serial.println(temperatureF);
  
  delay(5000);
}

