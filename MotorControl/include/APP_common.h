/*
COMMON DATA between the modules

*/

#define TRUE            1
#define FALSE           0

// The appplication type is selected though pin 14/12 (D5/D6)
#define APP_SERVO_CTRL  0       // Servo when both D5/D6 are set to 0V
#define APP_UNDEF1      1       // Not Defined
#define APP_UNDEF2      2       // Not Defined
#define APP_MOTOR_CTRL  3       // Default motor control

#define MAX_SIZE_SSID   32
#define MAX_SIZE_PWD    24
#define MAX_SIZE_IP_ADR 24
#define MAX_SIZE_TST    128

#define MAX_STRING_SIZE 65  // 64 characters + 0

// ## constant between main and E2PROM_mgt
#define MAX_DUTY_CYCLE  200   // No more than 200 (max 255 ==> DC voltage)
#define MIN_DUTY_CYCLE  0     // Motor is not working below that value

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
int  EEPROM_WRITE_STR(int, int, const char *);
int  TCP_IP_check_string(char *, int );
void E2PROM_test();

// From Wifi.cpp
#define PORT_BASE (43150)
int  WiFiSetup(void);
int  WifiRead(char *);
void WifiPrint(const char *, int);
void WifiSendMsgToHost(char *);
int  WifiClientAvailable(void);
