/*
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
*/

/*
COMMON DATA between C-CODE and Python code, "parsed" by HfileConstant.py.
*/

#define TRUE            1
#define FALSE           0

// The appplication type is selected though pin 14/12 (D5/D6)
#define SIZE_MESSAGE    64

#define XML_cfgFile     "ControlServer.xml"

#define APP_SERVO_CTRL  0       // Servo when both D5/D6 are set to 0V
#define APP_UNDEF1      1       // Not Defined
#define APP_UNDEF2      2       // Not Defined
#define APP_MOTOR_CTRL  3       // Default motor control

#define PORT            43150

// Communication code for Motor Control
#define PW_CHANGE       0x01
#define LIGHT_ORDER     0x02
#define STOP_ORDER      0x03
#define FWD_ORDER       0x04
#define BWD_ORDER       0x05

// Communication code for Servo Control
#define MSG_SERVO_BASE  0x80
#define FORK_RIGHT      0x81
#define FORK_LEFT       0x82
#define FORK_MIDDLE     0x83
#define FORK_SET_POS    0x84

// ## constant between main and E2PROM_mgt
#define MAX_DUTY_CYCLE  200   // No more than 200 (max 255 ==> DC voltage)
#define MIN_DUTY_CYCLE  0     // Motor is not working below that value
//
#define MAX_SIZE_SSID   32
#define MAX_SIZE_PWD    24
#define MAX_SIZE_IP_ADR 24
#define MAX_SIZE_TST    128

#define MAX_STRING_SIZE 65  // 64 characters + 0

// ######### The following value need to be identical in the HMI Application.
#define ORDER_SIZE      6     // Size of the message incomings from HOST application
#define ACK_MSG_LENGTH  80    // Size of the message returned to the HOST ("ACK")

// E2PROM ADDRESS
#define E2P_ADR_TAG1    0     // E2PROM address for Tag1
#define E2P_ADR_TAG2    4     // E2PROM address for Tag2
#define E2P_ADR_DutCycle  8   // E2PROM address to store latest Power value

#define E2P_ADR_SSID      12  // First String.
#define E2P_ADR_PWD       (E2P_ADR_SSID   + (MAX_SIZE_SSID+4)  ) // Max 32 chr for SSID
#define E2P_ADR_IP_ADR    (E2P_ADR_PWD    + (MAX_SIZE_PWD+4)   ) // Max 16 chr for PWD
#define E2P_ADR_TST       (E2P_ADR_IP_ADR + (MAX_SIZE_IP_ADR+4))
#define E2P_ADR_END       (E2P_ADR_TST    + (MAX_SIZE_TST+4)   )

// EEPROM services
void E2PROM_reinitialise(void);
bool EEPROM_init_value(void);
int  EEPROM_read_value(int);
void EEPROM_write_value(int, int);
int  EEPROM_READ_STR(int, int, char*);
int  EEPROM_WRITE_STR(int, int, char *);
int  TCP_IP_check_string(char *, int );
void E2PROM_test();

// From Wifi.cpp
#define PORT_BASE (43150)
int  WiFiSetup(void);
int  WifiRead(char *);
void WifiPrint(const char *, int);
void WifiSendMsgToHost(char *);
int  WifiClientAvailable(void);
