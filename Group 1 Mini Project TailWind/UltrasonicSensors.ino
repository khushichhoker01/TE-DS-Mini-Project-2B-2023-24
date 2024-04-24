#include <NewPing.h>

#define TRIGGER_PIN_FRONT  2
#define ECHO_PIN_FRONT     3
#define TRIGGER_PIN_REAR   4
#define ECHO_PIN_REAR      5
#define MAX_DISTANCE       200

NewPing sonarFront(TRIGGER_PIN_FRONT, ECHO_PIN_FRONT, MAX_DISTANCE);
NewPing sonarRear(TRIGGER_PIN_REAR, ECHO_PIN_REAR, MAX_DISTANCE);

void setup() {
  Serial.begin(9600);
}
// print("working1");
void loop() {
  unsigned int distanceFront = sonarFront.ping_cm();
  unsigned int distanceRear = sonarRear.ping_cm();
  // print("working2")

  Serial.print(distanceFront);
  Serial.print(",");
  Serial.println(distanceRear);

  delay(100);
}
