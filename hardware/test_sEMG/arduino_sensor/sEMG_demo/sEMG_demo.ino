#define semgPin A0

const float freq = 200.0;
const unsigned long period = 1000000 / freq;

unsigned long last_time = 0;
int emgValue = 0;

bool running = false;

void setup() {
  Serial.begin(115200);
  pinMode(semgPin, INPUT);
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

      emgValue = analogRead(semgPin);
      Serial.println(emgValue);
    }
  }
}