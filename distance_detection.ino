
const int trigPin = 8;
const int echoPin =10 ;


long duration;

float distance;

void setup() {

  Serial.begin(9600);
  
  
  pinMode(trigPin, OUTPUT);
  
  
  pinMode(echoPin, INPUT);
}

void loop() {
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  

  distance = (duration / 2.0) * 0.0344;
 
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
 
  delay(500);
}