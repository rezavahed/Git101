void setup() {
  // Initialize serial communication at 9600 baud
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}

void loop() {
  // Check if at least 6 bytes are available to read
  if (Serial.available() >= 6) {
    char incomingBytes[6]; // Array to store the incoming bytes

    // Read the 6 bytes into the array
    for (int i = 0; i < 6; i++) {
      incomingBytes[i] = Serial.read();
    }



    //Serial.write(incomingBytes[0]);

    // Process the incoming bytes
    switch (incomingBytes[0]) {
      case 0x04: // CMD_RANDOM = 0x04
        digitalWrite(2, HIGH);
        Serial.write(incomingBytes[0] + 0x80);
        for (int i = 1; i < 6; i++) {
          Serial.write(incomingBytes[i]);
        }
        break;
      case 0x02: // CMD_ADC = 0x02
        digitalWrite(2, LOW);
        break;
      case 0x03: // CMD_GET_FWVERSION = 0x03
        
        break;
      case 0x09: // CMD_HELLO = 0x09
        
        break;
      case 0x05: // CMD_GET_TARGET_TYPE = 0x05
        
        break;
      case 0x12: // CMD_READ_HR = 0x12
        // Handle case 0x12
        break;
      case 0x13: // CMD_WRITE_HR = 0x13
        
        break;
      default:
        
        break;
    }
  }
}
