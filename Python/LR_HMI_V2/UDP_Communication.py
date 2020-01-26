#
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
#
import socket # Socket API
import time
from   HfileConstant import Constante

# The server class is only used as a sub-part of over class
# It contains:
#   - the name of the server (only useful for display purpose
#   - the ip address
#   - TCP/IP 'port' used (43510 + the fourth byte of the ip address)
#            Example ip = 192.168.1.10 then the port used will be 43520
class  server:
    def __init__(self, __name, __ip, __port, ):
        self.name = __name
        self.ip   = __ip;
        self.port = __port

class UDP_comm:

    CTE = Constante("common.h")     # The message codes are store in the common.h file (shared with server C Code)
    CTE.ParseFile()                 # Parse the file and initialize the CTR class.

    # Liste of message of for Power Control (the bytes set 0x00 might be changed by the HMI)
    MsgPowerOrder   = bytearray([CTE.PW_CHANGE,   0x00, 0x00, 0x00, 0x00, 0x00])
    MsgLightOn      = bytearray([CTE.LIGHT_ORDER, 0x00, 0x00, 0x00, 0x00, 0x00])
    MsgLightOff     = bytearray([CTE.LIGHT_ORDER, 0x01, 0x00, 0x00, 0x00, 0x00])
    MsgStopOrder    = bytearray([CTE.STOP_ORDER,  0x00, 0x00, 0x00, 0x00, 0x00])
    MsgStartOrder   = bytearray([CTE.FWD_ORDER,   0x00, 0x00, 0x00, 0x00, 0x00])
    MsgBackwardOrder= bytearray([CTE.BWD_ORDER,   0x00, 0x00, 0x00, 0x00, 0x00])

    #  Liste of message for Swith Control (the bytes set 0x00 might be changed by the HMI)
    MsgForkRight    = bytearray([CTE.FORK_RIGHT,  0x00, 0x00, 0x00, 0x00, 0x00])
    MsgForkLeft     = bytearray([CTE.FORK_LEFT,   0x00, 0x00, 0x00, 0x00, 0x00])
    MsgForkMiddle   = bytearray([CTE.FORK_MIDDLE, 0x00, 0x00, 0x00, 0x00, 0x00])
    MsgForkSetPos   = bytearray([CTE.FORK_SET_POS,0x00, 0x00, 0x00, 0x00, 0x00])

    def __init__(self, CtrlServerLst):
        i = 0
        # Get the constant from 'common.h' file active.
        CTE = Constante("common.h")
        CTE.ParseFile()

        # Get the host IP address.
        #        if your PC / Host have several Ethernet/IP port,
        #        you might not get the IP address you want !!!!!!!!
        self.ipLocal = socket.gethostbyname(socket.gethostname())

        # The list of Server from
        self.ServerLst  = []            # Array of server with IP, Port and name
        self.UDPClientSocket = []       # Array of the socket created: one per server.

        # Assigned the port for each server, then create the socket associated to each server
        for i in range(0, len(CtrlServerLst)):
            CtrlPt = CtrlServerLst[i]
            BYTES = CtrlPt.ip.split('.')  # Socket Port number  as port = 43150 + the fourth digit of the IP Address
            Byte4 = int(BYTES[3])  # ==> For 192.168.1.100 the port will be 43150 + 100 ==> 43250
            CtrlPt.port = CTE.PORT + Byte4

            self.server=server(CtrlPt.name,CtrlPt.ip,CtrlPt.port)
            self.ServerLst.append(self.server)

            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Use full trace
            print("Create socket for", CtrlPt.name, "IP:", CtrlPt.ip, "PORT:", CtrlPt.port)
            sock.bind((self.ipLocal, CtrlPt.port))
            sock.setblocking(0)
            self.UDPClientSocket.append(sock)

    def SendData(self, Msg, numLoco):
    #
    # The ESP32_SendData function is sending data to a given server using UDP
    # After sending the data, the procedure is looking for some acknowledgment message.
    # However there is no error or 'retry' procedure if such message is not received.
    #
    # The 'cpt, cpt1' variables are only there for debugging purpose
        cpt1=0
        cpt=0

        DestAdr =  self.ServerLst[numLoco].ip
        port    =  self.ServerLst[numLoco].port
        self.UDPClientSocket[numLoco].sendto(Msg, (DestAdr, port) )
        print("Dest Adr, Port:"+DestAdr+" - "+str(port)+ " Msg: "+str(Msg[0])+" - "+str(Msg[1])+" - "+str(Msg[2]))
        time.sleep(0.100)
        try:
            msg,addr = self.UDPClientSocket[numLoco].recvfrom(self.CTE.SIZE_MESSAGE)
            print("<===", msg,cpt)
        except BlockingIOError:
    #        print("IO error")
            cpt1=cpt1+1
        time.sleep(0.100)
        try:
            msg,addr = self.UDPClientSocket[numLoco].recvfrom(self.CTE.SIZE_MESSAGE)
            print("<===", msg,cpt)
        except BlockingIOError:
            #        print("IO error")
            cpt1=cpt1+1



