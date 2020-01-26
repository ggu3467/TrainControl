/*
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code

DISCLAIMER:
  *** The communication between the client application and the server (ESP32 module) ***
  *** is completely 'open', hence UNSAGE.                                            ***

*/



/* ESP32 headers */
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <EEPROM.h>

/* Local Application headers */
#include "APP_common.h"

#define TAG1  0x55AA   // Tag to Indicate that EZ2PROM is setup
#define TAG2  0xCC33   // Tag to Indicate that EZ2PROM is setup

extern const char*  ssid1;
extern const char*  password1;
extern       int    startDutyCycle;

void E2PROM_reinitialise () {
char  buf[MAX_STRING_SIZE];
int   strLength=0;

    EEPROM.put(E2P_ADR_TAG1,TAG1);
    EEPROM.put(E2P_ADR_TAG2,TAG2);

    strLength = EEPROM_WRITE_STR(E2P_ADR_SSID, MAX_SIZE_SSID, ssid1);
    Serial.print("E2PROM_test: Lenght of SSID:");
    Serial.println(strLength);

    strLength = EEPROM_WRITE_STR(E2P_ADR_PWD, MAX_SIZE_PWD, password1);
    Serial.print("E2PROM_test: Lenght of PWD:");
    Serial.println(strLength);

    EEPROM.put(E2P_ADR_DutCycle,MIN_DUTY_CYCLE);

    EEPROM.commit();
    delay(500);

    EEPROM_READ_STR(E2P_ADR_SSID, MAX_SIZE_SSID, buf);
    Serial.print("E2PROM_test: SSID:   ");
    Serial.println(buf);

    EEPROM_READ_STR(E2P_ADR_PWD, MAX_SIZE_PWD, buf);
    Serial.print("E2PROM_test: PWD:   ");
    Serial.println(buf);

    EEPROM_READ_STR(E2P_ADR_IP_ADR, MAX_SIZE_IP_ADR, buf);
    Serial.print("E2PROM_test: IPADR: ");
    Serial.println(buf);
}
/* ==================== TEST CODE */


bool EEPROM_init_value( void ){
int tag1,tag2;
char ssid[MAX_SIZE_SSID];
char pwd[MAX_SIZE_PWD];
char ip_adr[MAX_SIZE_IP_ADR];

//  EEPROM.begin(1024);  // ==> done in the main setup.
  EEPROM.get(E2P_ADR_TAG1,tag1);
  Serial.println(tag1);
  EEPROM.get(E2P_ADR_TAG2,tag2);
  Serial.println(tag2);
  EEPROM.get(E2P_ADR_SSID  , ssid);
  Serial.println(ssid);
  EEPROM.get(E2P_ADR_PWD   , pwd);
  Serial.println(pwd);
  EEPROM.get(E2P_ADR_IP_ADR, ip_adr);
  Serial.println(ip_adr);

  if (  (tag1==TAG1) &&
        (tag2==TAG2) &&
        (TCP_IP_check_string(ssid  , MAX_SIZE_SSID)) &&
        (TCP_IP_check_string(pwd   , MAX_SIZE_PWD )) &&
        (TCP_IP_check_string(ip_adr, MAX_SIZE_IP_ADR ))) {

        Serial.println("=== E2PROM OK ===");
        EEPROM.get(E2P_ADR_DutCycle,startDutyCycle);
        return (TRUE);
    } else {
      Serial.println("########### Tag E2PROM NOT OK");
      E2PROM_reinitialise();
      return(TRUE);
  }
}

// ############################################################################
// PUBLIC FUNCTION:  Read a string from E2PROM to a buffer, one character per 32 bits word
//    EEPROM_write_string(int E2P_ADR, int maxChar, const char *pStr)
//    - int  E2P_ADR: EEPROM start address where to read a string (null termianted).
//    - int  maxChar: Maximum number of character allowed
//    * const char* StringBuf: pointeur to the buffer used to store the string
// ###########################################################################



int EEPROM_READ_STR(int E2P_ADR, int maxChar, char *pStr) {
int p;
int value;        // convert char to int.
char *pBuf;
int  i=0;
bool end;
unsigned char c1,c2,c3,c4;

p    = E2P_ADR;
pBuf = pStr;
end  = false;

  do {
      EEPROM.get(p, value);
//      sprintf(buf2,"Value: 0x%08x",value);
//      Serial.println(buf2);
      c1 = (unsigned char) (value  & 0x000000FF);
      c2 = (unsigned char) ((value & 0x0000FF00)>> 8);
      c3 = (unsigned char) ((value & 0x00FF0000)>> 16);
      c4 = (unsigned char) ((value & 0xFF000000)>> 24);

      *pBuf=c1;
      pBuf++;
      i++;
      end=true;
      if (c1) {
          *pBuf++=c2;
          i++;
          if (c2)  {
              *pBuf++=c3;
              i++;
              if (c3) {
                  *pBuf++=c4;
                  i++;
                  if (c4) {
                        end=false;
                      } // if c4
                  }  // if c3
              } // if c2
          } // c1

      p=p+4; // Next int 32 bits

      // Boundary checking
      if (i>maxChar) {
        Serial.println("EEPROM_READ_STR: EEPROM_READ_STR: String too long E2PROM_write_string");
        return 0;
      }
  } while (end==false);
//  Serial.print("EEPROM_READ_STR: length of String");
//  Serial.println(i);
  return (i);
}
// ############################################################################
// PUBLIC FUNCTION:  Write a string to E2PROM one character per 32 bits word
//    EEPROM_write_string(int E2P_ADR, int maxChar, const char *pStr)
//    - int  E2P_ADR: EEPROM start address where to write to.
//    - int  maxChar: Maximum number of character allowed
//    * const char* pStr: pointeur to the string to write (null termianted)
// ###########################################################################

int EEPROM_WRITE_STR(int E2P_ADR, int maxChar, const char *StringBuf) {
    int idx = 0;
    int i=0;
    int value;        // convert 4 char to a 32bits int.
    unsigned char c1,c2,c3,c4;
    char *pStr = (char *)StringBuf;
    bool ended=false;
    char buf[256]; // sprintf..

    do {
        c1 = (unsigned char)*pStr++;
        c2 = (unsigned char)*pStr++;
        c3 = (unsigned char)*pStr++;
        c4 = (unsigned char)*pStr++;

        if (c1==0) {
              i++;
              value = 0;
              ended=true;
           } else
                if (c2==0) {
                    i+=2;
                    value = (int) c1;
                    ended=true;
              } else
                  if (c3==0) {
                          i+=3;
                          value = (int) ((c1) | (c2<<8));
                          ended=true;
                      } else
                          if (c4==0) {
                                  i+=4;
                                  value = (int) ((c1) | (c2<<8) | (c3<<16));
                                  ended=true;
                              } else {
                                  i+=4;
                                  value = (int) ((c1) | (c2<<8) | (c3<<16) | (c4 << 24));
                                }

      sprintf(buf, "0x%04x", value);
      Serial.println(buf);
        EEPROM_write_value(E2P_ADR + idx, value);

        // Boundary checking
        if (i>(maxChar)) {
          Serial.print("EEPROM_WRITE_STR: String too long E2PROM_write_string");
          return 0;
        }
        idx = idx + 4;
    } while (ended==false);

   Serial.print("EEPROM_WRITE_STR: String length:");
   Serial.println(i);

    return(i);  // Length of the string
}

int TCP_IP_check_string(char *str, int maxLength){
int i;
char *p=(char *)str;
char c=' ';

  for(i=0;i<=maxLength;i++) {
    c=*p;
    Serial.print(c);
    if (c==0)
       break;
    if ((c<32)|| (c>128)) {         // More restrective test ?
       Serial.print("TCP_IP_check_string: invalid caracter: ");
       Serial.println(c);
       return FALSE;
    }
    p++;
  }

  if (i<maxLength) {
    return TRUE;
  }

Serial.print("TCP_IP_check_string: Invalid String: ");
Serial.println(str);
return FALSE;
}

void EEPROM_write_value(int address, int value) {
    EEPROM.put(address, value);
    EEPROM.commit();
}

int EEPROM_read_value(int address) {
int value;
    EEPROM.get(address, value);
    return(value);
}
