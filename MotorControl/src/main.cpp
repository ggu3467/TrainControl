/*
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code

DISCLAIMER:
  *** The communication between the client application and the server (ESP32 module) ***
  *** is completely 'open', hence UNSAGE.                                            ***

*/

/* ESP32 headers */
#include <Arduino.h>
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <EEPROM.h>
#include <WiFiUdp.h>    /* UDP Communication */
#include <Servo.h>

/* Local Application headers */
#include "APP_common.h"   
#include "../../Python/LR_HMI_V2/common.h"  // Shared with Python client application

// Local service function
void printDec(byte *, byte);

const int   TIMER_INIT      = 375;
const int   PWM_PIN         = 4;    // D2 Power With Modulation PIN 
const int   SERVO1_PIN      = 13;   // D7 Use to control servo 1
const int   SERVO2_PIN      = 16;   // D0 Use to control servo 2
const int   SERVO3_PIN      = 20;   // D1 Use to control servo 3

const int   LIVE_LED        = 15;   // D8 / 16LED used to indicate POWER level for motor control

const int   TYPE_APPLI1     = 14;   // D5 Pin used to select the application
const int   TYPE_APPLI2     = 12;   // D6

char AckMsgMotor1[ACK_MSG_LENGTH]="Power Order received";
char AckMsgMotor2[ACK_MSG_LENGTH]="Light Order received";
char AckMsgMotor3[ACK_MSG_LENGTH]="Stop  Order received";
char AckMsgMotor4[ACK_MSG_LENGTH]="Forward  Order received";
char AckMsgMotor5[ACK_MSG_LENGTH]="Backward Order received";

char AckMsgForkRight [ACK_MSG_LENGTH]="Fork set to the right";
char AckMsgForkLeft  [ACK_MSG_LENGTH]="Fork set to the left";
char AckMsgForkMiddle[ACK_MSG_LENGTH]="Fork moving middle";
char AckMsgForkSetPos[ACK_MSG_LENGTH]="Fork set to position";

char UnknownCode [ACK_MSG_LENGTH]="Received an Unkown code message";

int  dutyCycle              = MIN_DUTY_CYCLE;
int  startDutyCycle         = MIN_DUTY_CYCLE;
int  cycleCpt               = 0;
int  cptLiveLed             = 0;
int  cptLed                 = 0;
int  ApplicationMode        = 0;
Servo servo1;
Servo servo2;
Servo servo3;
WiFiUDP Udp;

// Send to server using created UDP socket
int  localUdpPort = PORT_BASE;
char incomingPacket[256];


void UdpPrint(IPAddress destIP,char *Msg){

    Udp.begin(localUdpPort);
    Udp.beginPacket(destIP, localUdpPort); // ####################
    Udp.write(Msg);
    Udp.endPacket();

//    Serial.print("Port:");
//    Serial.println(localUdpPort);
}

void UdpPrintValue(IPAddress destIP, const char *string, int value) {
char buf[ACK_MSG_LENGTH+1];   // +1, for null terminination

  memset(buf,'-',ACK_MSG_LENGTH);
  sprintf(buf, "%s: %u", string, value);
  UdpPrint(destIP, buf);
}

void UdpPrint2Value(IPAddress destIP, const char *string1, int value1, const char *string2, int value2) {
char buf[ACK_MSG_LENGTH+1];   // +1, for null terminination

  memset(buf,'-',ACK_MSG_LENGTH);
  sprintf(buf, "** %s: %u  %s: %u **", string1, value1, string2, value2);
  UdpPrint(destIP, buf);
}

/*
  Timer interrupt routine, use to pilot the DarlingTon transistor, hence changing
   the dutyCyle.

   This is an issue with the D1 Mini lite, could not use PWM_PIN (?!)
*/
int cycleLed=0;
void ICACHE_RAM_ATTR onTimerISR(){
    if (dutyCycle==0) {
      digitalWrite(PWM_PIN, LOW);
    }

// Rapport cyclique pour PWM
    cycleCpt++;

    if ((dutyCycle !=0) and (cycleCpt>255)) {
        cycleCpt  =0;
        digitalWrite(PWM_PIN,HIGH);
    }
    if (cycleCpt>dutyCycle) {
         digitalWrite(PWM_PIN,LOW);
    }

    cycleLed++;
    if (cycleLed>MAX_DUTY_CYCLE*5) {
        cycleLed=0;
       digitalWrite(LIVE_LED, HIGH);
    }
    if (cycleLed>dutyCycle*5) {
        digitalWrite(LIVE_LED, LOW);
    }

  timer1_write(TIMER_INIT);
}

// We are looking for a interrupt every
void SetTimerMotorCtrl() {
  Serial.println("SetTimer: IN");
  
  timer1_isr_init();
  timer1_attachInterrupt(onTimerISR);
  timer1_enable(TIM_DIV16, TIM_EDGE, TIM_LOOP);
  timer1_write(TIMER_INIT); // every 250uS

  Serial.println("SetTimer: OUT ...");
}


void ServoControlSetup(void) {  
    servo1.attach(SERVO1_PIN); 
    servo2.attach(SERVO2_PIN); 
    servo3.attach(SERVO3_PIN);
}
/*

  General setup() procedure for SerialPort, PinMode, Timer, BlueTooth, and E2PROM

*/


void setup() {
int pinMode1,pinMode2;            // Read pin used to select application

    pinMode(LIVE_LED,OUTPUT);     // Set-up PIN for LED
    pinMode(PWM_PIN, OUTPUT);     // Set-up PIN for PowerControl

  // 00 ==> Motor Control
  // 11 ==> Servo Control

    pinMode(TYPE_APPLI1, INPUT);  // D5 - 14
    pinMode(TYPE_APPLI2, INPUT);  // D6 - 12 Select application Motor or Servo Control

    pinMode1= digitalRead(TYPE_APPLI1);
    pinMode2= digitalRead(TYPE_APPLI2);

    digitalWrite(PWM_PIN, LOW);

    Serial.begin(230400);         // Serial port for traces
    Serial.println("setup");

    Serial.print("PinMode1=");
    Serial.println(pinMode1);
    Serial.print("PinMode2=");
    Serial.println(pinMode2);

    if ( (pinMode1==1) && (pinMode2==1)) {
         ApplicationMode= APP_MOTOR_CTRL;
         Serial.println("Application is Motor Control");
    }
    else if ((pinMode1==0) && (pinMode2==0)) {
         ApplicationMode= APP_SERVO_CTRL;
         Serial.println("Application is Servo Control");
    }
    else {
      do{
         Serial.println("Application is not defined");
         delay(1000);
      } while (1);
    /* code */
    }

    WiFi.begin("LouisRoussy","Monastier");

    pinMode(LIVE_LED,OUTPUT);     // Set-up PIN for LED
    pinMode(PWM_PIN, OUTPUT);     // Set-up PIN for PowerControl
    digitalWrite(PWM_PIN, LOW);
    EEPROM.begin(512);

    if (EEPROM_init_value()==TRUE)      // Initialize E2PROM
        startDutyCycle=EEPROM_read_value(E2P_ADR_DutCycle);
    else  {
        EEPROM_write_value(E2P_ADR_DutCycle,MIN_DUTY_CYCLE);
        startDutyCycle=MIN_DUTY_CYCLE;
    }
    
    if (ApplicationMode==APP_MOTOR_CTRL) {
        SetTimerMotorCtrl();                   // Set-up used for power control (PWM)
    }
    if (ApplicationMode==APP_SERVO_CTRL){
       ServoControlSetup();
    }
    localUdpPort = WiFiSetup();                  // Wifi initialisation */
    Serial.print("Port:");
    Serial.println(localUdpPort);
      //This initializes udp and transfer buffer
}

void ServoSendAngle(IPAddress destIP, int numServo, int angle ) {

    UdpPrint2Value(destIP, " NumServo:", numServo, " angle:",angle);
    
    switch (numServo) {
        case 1: servo1.write(angle);
                break;
        case 2: servo2.write(angle);
                break;
        case 3 :servo3.write(angle);
                break;
    }                   
}
/*

   Main loop of the application:
      - Update Power
      -

*/
void loop() {
byte  Msg[SIZE_MESSAGE+1];
IPAddress AckIP;
char  MsgCode;
int   MsgLength;
int   MaxLength=SIZE_MESSAGE;
int   result;
int   numServo;  // Servo number from 0 to 2
int   angle;     // Rotation angle

  dutyCycle= startDutyCycle; // startDutyCycle is set in the general setup.
  result = Udp.begin(localUdpPort);
  Serial.print("Port:");
  Serial.println(localUdpPort);
  
  Serial.print("UdpBegin");
  Serial.println(result);
  // sanity check..

  if ( (startDutyCycle<MIN_DUTY_CYCLE) || (startDutyCycle>MAX_DUTY_CYCLE)) {
         dutyCycle = MIN_DUTY_CYCLE;
  }

// forever loop
  while (1) {
    delay(100);

    MaxLength = Udp.parsePacket();
    MsgLength = Udp.read(Msg,MaxLength);

    if ( MsgLength > 0){
        int UsableScale; 
        int PowerOrder;          // For power/speed setting

        AckIP = Udp.remoteIP();  // In order to send ACK msg to the sender

        Serial.println(Udp.remoteIP());
        Serial.print("RCV: ");
        Serial.print(MsgLength);
        MsgCode=Msg[0];
        if (MsgCode<MSG_SERVO_BASE) {

            switch (MsgCode) {
                case 0: break;
                case PW_CHANGE: 
                        Serial.print(" Power:"); //
                        PowerOrder = (int)Msg[1];
                        printDec((byte *)&Msg[1],1);
                        WifiSendMsgToHost(AckMsgMotor1);
                        // The power order is from 0 to 100
                        // It is then scaled from MIN_DUTY_CYCLE to MAX_DUTY_CYCLE
                        UsableScale  = MAX_DUTY_CYCLE-MIN_DUTY_CYCLE; // Actual possible scale
                        dutyCycle = ((UsableScale*PowerOrder)/MAX_DUTY_CYCLE)+MIN_DUTY_CYCLE;
                        Serial.print(", PWM: ");
                        Serial.println(dutyCycle);
                        UdpPrintValue(AckIP," PWMxx:",dutyCycle);
                        break;
                case LIGHT_ORDER: 
                        Serial.println(" TODO LIGHT ORDER");
                        UdpPrint(AckIP,AckMsgMotor2);
                        break;
                case STOP_ORDER: Serial.println(" Stop");
                        dutyCycle=0;
                        UdpPrint(AckIP,AckMsgMotor3);
                        break;
                case FWD_ORDER: 
                        Serial.println(" Forward");
                        UdpPrint(AckIP,AckMsgMotor4);
                        break;
                case BWD_ORDER:
                        Serial.println(" Backward");
                        UdpPrint(AckIP,AckMsgMotor5);
                        break;
                default:
                        Serial.println(" Unkown Message Received");
                        UdpPrintValue(AckIP,UnknownCode,MsgCode);
                        break;
              } // switch case
        } // if Msg is related to MotorControl

        if (MsgCode>=MSG_SERVO_BASE) {
            switch (MsgCode) {
                case 0x80: break;
                case FORK_RIGHT: 
                          numServo = Msg[1];
                          angle    = Msg[2];
                          ServoSendAngle(AckIP, numServo, angle);
                          break;
                case FORK_LEFT: 
                          numServo = Msg[1];
                          angle    = Msg[2];
                          ServoSendAngle(AckIP, numServo, angle);
                          break;

                case FORK_MIDDLE: 
                          numServo = Msg[1];
                          angle    = Msg[2];
                          ServoSendAngle(AckIP, numServo,angle);
//                          UdpPrint(AckIP,AckMsgForkMiddle);
                          break;

                case FORK_SET_POS: 
                          numServo = Msg[1];
                          angle    = Msg[2];
                          ServoSendAngle(AckIP, numServo,angle);
                          break;
            }
        } // if (MsgCode>=MSG_SERVO_BASE) 
      } // if MsgLength>0)
      EEPROM_write_value(E2P_ADR_DutCycle,dutyCycle);
    } // while (1)
}

/**
   Helper routine to dump a byte array as hex values to Serial.
*/
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

/**
   Helper routine to dump a byte array as dec values to Serial.
*/
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}

