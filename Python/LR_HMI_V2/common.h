/*
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
*/

/*
COMMON DATA between C-CODE and Python code, "parsed" by HfileConstant.py.
*/

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

//
#define MAX_SIZE_SSID   32
#define MAX_SIZE_PWD    24
#define MAX_SIZE_IP_ADR 24
#define MAX_SIZE_TST    128

#define MAX_STRING_SIZE 65  // 64 characters + 0

// ######### The following value need to be identical in the HMI Application.
#define ORDER_SIZE      6     // Size of the message incomings from HOST application
#define ACK_MSG_LENGTH  80    // Size of the message returned to the HOST ("ACK")


