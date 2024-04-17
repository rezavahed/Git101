
#include <CRC8.h>

#define CMD_RANDOM         0x04
#define CMD_ADC            0x02
#define CMD_GET_FWVERSION  0x03
#define CMD_HELLO          0x09
#define CMD_GET_TARGET_TYPE 0x05
#define CMD_READ_HR         0x12
#define CMD_WRITE_HR      0X13
const char* FW_VERSION = "1.2.6";
void setup() {
  // Initialize serial communication at 9600 baud
  Serial.begin(9600);
  pinMode(7, OUTPUT);


 
}

uint16_t getRandomValue() {
  // Return a dummy random value
  return random(0, 1000);
}

uint32_t getFirmwareVersion() {
    // Assuming the version is in format Major.Minor.Patch
    uint8_t major = FW_VERSION[0] - '0';
    uint8_t minor = FW_VERSION[2] - '0';
    uint8_t patch = FW_VERSION[4] - '0';

    // Pack version into 32 bits: major, minor, and patch each in their own byte
    uint32_t version = ((uint32_t)patch << 24) | ((uint32_t)minor << 16) | ((uint32_t)major << 8);
    return version;
}
uint8_t calculateCRC(const uint8_t* data, int len) {
    CRC8 crc;
    crc.reset();

    // Assuming 'data' points to an array of 5 bytes
    for (int i = 0; i < len; ++i) {
        crc.add(data[i]);
    }

    return crc.calc();
}

void sendResponse(uint8_t res_id, uint32_t value) {

  uint8_t response_packet[6]; 

  response_packet[0] = res_id;
  response_packet[1] = value & 0xFF;          // Least significant byte
  response_packet[2] = (value >> 8) & 0xFF;
  response_packet[3] = (value >> 16) & 0xFF;
  response_packet[4] = (value >> 24) & 0xFF;  // Most significant byte
  
  response_packet[5] = calculateCRC(response_packet,5);
  Serial.write(response_packet, 6);
  


}

void loop() {
    
  // Check if at least 6 bytes are available to read
  if (Serial.available() >= 6) {
    char incomingBytes[6];

    // Read the 6 bytes into the array
    for (int i = 0; i < 6; i++) {
      incomingBytes[i] = Serial.read();  
    }

    
    uint8_t cmd_id = incomingBytes[0];

    // Process the incoming bytes
    switch (cmd_id) {
      case CMD_GET_FWVERSION: //
        digitalWrite(7, HIGH);

        //first byte incomingBytes[0] + 0x80 is id
        sendResponse(CMD_GET_FWVERSION + 0x80,getFirmwareVersion());
        
        break;
      case CMD_ADC: // CMD_ADC = 0x02
        digitalWrite(7, LOW);
        break;
      case 0x15: 
        
        break;
      case CMD_RANDOM: // CMD_HELLO = 0x09
        sendResponse(CMD_RANDOM + 0x80,getRandomValue());
        
        break;
      case CMD_GET_TARGET_TYPE: // CMD_GET_TARGET_TYPE = 0x05
        
        break;
      case CMD_READ_HR: // CMD_READ_HR = 0x12
        // Handle case 0x12
        break;
      case CMD_WRITE_HR: // CMD_WRITE_HR = 0x13
        
        break;
      default:
        
        break;
    }
    

  }



}
