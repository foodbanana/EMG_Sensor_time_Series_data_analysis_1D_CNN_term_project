const int sensorPins[4] = {A0, A1, A2, A3};

const float freq = 200.0;
const unsigned long period = 1000000 / freq;

unsigned long last_time = 0;
bool running = false;

void setup() {
  Serial.begin(115200);
  
  for(int i=0; i<4; i++){
    pinMode(sensorPins[i], INPUT);
  }
}

void loop() {
  if(Serial.available() > 0){
    char command = Serial.read();

    if(command == 's'){
      running = true;
      last_time = micros();
    }
    else if (command == 'e'){
      running = false;
    }

    while(Serial.available() > 0){
      Serial.read();
    }
  }

  if(running){
    unsigned long current_time = micros();
    
    if(current_time - last_time >= period){
      last_time += period;

      int val0 = analogRead(sensorPins[0]);
      int val1 = analogRead(sensorPins[1]);
      int val2 = analogRead(sensorPins[2]);
      int val3 = analogRead(sensorPins[3]);

      Serial.print(val0);
      Serial.print(",");
      Serial.print(val1);
      Serial.print(",");
      Serial.print(val2);
      Serial.print(",");
      Serial.println(val3);
    }
  }
}
