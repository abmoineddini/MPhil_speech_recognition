/* Arduino Mega Data Collection
 * by: Amirbahador Moineddini
 * date: November 10th, 2021
 * V1 Data collection

/* Pin Setup
 * A5  Channel 1
 * A8  Channel 2
 * A12 Channel 3
 * A14 Channel 4
*/

void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  pinMode(A5, INPUT);  // Channel 1
  pinMode(A8, INPUT);  // Channel 2
  pinMode(A12, INPUT); // Channel 3
  pinMode(A14, INPUT); // Channel 4

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(analogRead(A5));
  Serial.print(",");
  Serial.print(analogRead(A8));
  Serial.print(",");
  Serial.print(analogRead(A12));
  Serial.print(",");
  Serial.println(analogRead(A12));

}

