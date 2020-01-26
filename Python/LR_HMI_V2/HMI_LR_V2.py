#
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
#

# This the main HMI ...

#External Import
import tkinter    as tk
import time


# Local import
import ChangeTrim as AdjustTrim
from   HfileConstant     import Constante           # Global constant values from 'common.h' file
from   UDP_Communication import UDP_comm as ESP     # Communication aspect of the projet
import XMLConfig         as CFG                     # XML Read (not Write Yet)...

# IHM AND COMMUNICATION WITH THE SERVERs
global CurrentControlPoint
global root

class CtrlServer:
    def __init__(self, __CtrlPoint, UDP_comm): #### Nom, Type, IPAdr, instance, port, valRight, valLeft):
        self.CP = __CtrlPoint

        self.TrimValue   = tk.Scale          # USe by Scale
        self.angle1      = tk.IntVar()
        self.angle2      = tk.IntVar()
        self.angle3      = tk.IntVar()
        self.ServoTrim   = tk.Scale

        self.TrimButton1 = tk.Button
        self.Txt1        = tk.StringVar()
        self.TrimButton2 = tk.Button
        self.Txt2        = tk.StringVar()
        self.TrimButton3 = tk.Button
        self.Txt3        = tk.StringVar()

        self.allure      = 0
        self.light      = tk.IntVar()  # Variable attached to widgets
        self.marche     = tk.IntVar()
        self.speed      = tk.IntVar()

        self.x          = 0
        self.PwrWidget  = tk.Scale

        self.light.set(0)
        self.marche.set(1)      # initially the motor are not active. #TODO use constant
        self.speed.set(0)

    def selected(self):
        return self.TrimSelected

# Controls for locomotive
    def SetStart(self):
        x = self.marche.get()
        print("==>Start", self.CP.name, "-", x)
        self.PwrWidget.config(state='active')
        self.PwrWidget.config(bg='light blue')
        ESP.SendData(ESP.MsgStartOrder, self.CP.numCtrlPoint)
    def SetStop(self):
        x = self.marche.get()
        print("==>Stop", self.CP.name, "-", x)
        self.speed.set(0)
        self.PwrWidget.config(state='disabled')
        self.PwrWidget.config(bg='gray')
        ESP.SendData(ESP.MsgStopOrder, self.CP.numCtrlPoint)
    def SetBack(self):
        x = self.marche.get()
        print("==>Back", self.CP.name, "-", x)
#        self.powerScale = 'Enabled'
        self.PwrWidget.config(state='active')
        self.PwrWidget.config(bg='light blue')
        ESP.SendData(ESP.MsgBackwardOrder, self.CP.numCtrlPoint)
    def SetPower(self, PowerValue):
        print("valeur de PowerValue",PowerValue)
        print("==>Set Power:", self.CP.name,':', PowerValue)
        ESP.MsgPowerOrder[1]=int(PowerValue)
        ESP.SendData(ESP.MsgPowerOrder, self.CP.numCtrlPoint)
    def LightOn(self):
        print("==>LightOn", self.CP.name,'-', self.light.get())
        ESP.SendData(ESP.MsgLightOn, self.CP.numCtrlPoint)
    def LightOff(self):
        print("==>LightOff", self.CP.name, '-', self.light.get())
        ESP.SendData(ESP.MsgLightOff,self.CP.numCtrlPoint)

# Control for up to 3 servos (used to control track switches)
# First SET

    def SetForkLeft1(self):
        print("==>Fork1 SET LEFT: ", self.CP.name, self.CP.TrimLeft[0], self.CP.TrimRight[0], "-")
        ESP.MsgForkLeft[1]=1
        ESP.MsgForkLeft[2]=int(self.CP.TrimLeft[0])
        ESP.SendData(ESP.MsgForkLeft,self.CP.numCtrlPoint)
    def SetForkRight1(self):
        print("==>Fork1 SET RIGHT: ", self.CP.name, self.CP.TrimLeft[0], self.CP.TrimRight[0], "-")
        ESP.MsgForkRight[1]=1
        ESP.MsgForkRight[2]=int(self.CP.TrimRight[0])
        ESP.SendData(ESP.MsgForkRight,self.CP.numCtrlPoint)

    def SetForkLeft2(self):
        print("==>Fork2 SET LEFT: ", self.CP.name, self.CP.TrimLeft[1], self.CP.TrimRight[1], "-")
        ESP.MsgForkLeft[1]=2
        ESP.MsgForkLeft[2]=int(self.CP.TrimLeft[1])
        ESP.SendData(ESP.MsgForkLeft,self.CP.numCtrlPoint)
    def SetForkRight2(self):
        print("==>Fork2 SET RIGHT: ", self.CP.name, self.CP.TrimLeft[1], self.CP.TrimRight[1], "-")
        ESP.MsgForkRight[1]=2
        ESP.MsgForkRight[2]=int(self.CP.TrimLeft[1])
        ESP.SendData(ESP.MsgForkRight,self.CP.numCtrlPoint)

    def SetForkLeft3(self):
        print("==>Fork3 SET LEFT: ", self.CP.name, self.CP.TrimLeft[2], self.CP.TrimRight[2], "-")
        ESP.MsgForkLeft[1]=3
        ESP.MsgForkLeft[2]=int(self.CP.TrimLeft[2])
        ESP.SendData(ESP.MsgForkLeft,self.CP.numCtrlPoint)
    def SetForkRight3(self):
        print("==>Fork3 SET RIGHT: ", self.CP.name, self.CP.TrimLeft[2], self.CP.TrimRight[2], "-")
        ESP.MsgForkRight[1]=3
        ESP.MsgForkLeft[2] =int(self.CP.TrimLeft[2])
        ESP.SendData(ESP.MsgForkRight,self.CP.numCtrlPoint)

# Secund SET
    def SetTrim1(self):
        print("==>Select Trim 1")
        self.TrimButton1.config(bg='orange')
        App1 = AdjustTrim.ChangeTrim(root, self.CP, 0, ESP)

    def SetTrim2(self):
        print("==>Select Trim 2")
        self.TrimButton2.config(bg='orange')
        App1= AdjustTrim.ChangeTrim(root, self.CP, 1, ESP)

    def SetTrim3(self):
        print("==>Select Trim 3")
        self.TrimButton3.config(bg='orange')
        App1 = AdjustTrim.ChangeTrim(root, self.CP, 2, ESP)

#
    def setServo(self):
        print("==>SetServo", self.name, '-', self.light.get())
        ESP.SendData(ESP.MsgLightOff,self.CP.numCtrlPoint)

    #
    # HMI ASPECT
    #

class ControlPointIHM(CtrlServer):
    def __init__(self, root,  ControlLst, Nom):
        self.name    = Nom              # Server/ControlPoint Name
        self.allure  = 0                # Initially stopped

        self.master = root
        self.tl = tk.Toplevel(root)   # Link with master window
        self.tl.withdraw()              # Dp Not display empty window
        self.create(root, ControlLst, Nom)


    def create(self, master, ControlLst,  Nom):
        Locomotive = tk.Canvas(tk.Toplevel(master), bg='light blue', height=600, width=1200, borderwidth =5)
        Locomotive.grid(row=50, column=14, rowspan=1, sticky='NW', padx=4, pady=4)

        frameTitre = tk.Frame(Locomotive, width=700, borderwidth = 5, height=30,bg='dark blue', relief="sunken", highlightcolor="red", highlightthickness=2 )
        frameTitre.grid(row=0, column=14)
        LabelTitre = tk.Label(frameTitre, text="*** Control Center ***", font="Arial 14", height=2, bg='light blue')
        LabelTitre.grid(row=0, column=14)

        x        = 2
        index    = 1
        cptServo = 0
        for CtrlPt in ControlLst:

            frame = tk.Frame(Locomotive, width=850, height=50, borderwidth = 6, bg='light blue', relief="ridge")
            frame.grid(row=x,column=14,sticky='NW')
            Label1 = tk.Label(frame, text=CtrlPt.CP.name+'\n'+CtrlPt.CP.ip, font ="Arial 12", height=3, width=15, bg='light blue')
            Label1.grid(row=x+1, column=0, rowspan=2, padx=3,sticky='NW')

            print('Locomotive:', CtrlPt.CP.name)
            if CtrlPt.CP.type=='Loco':
                b1 = tk.Radiobutton(frame,variable=CtrlPt.marche, value=0, text=' FWD ',bg='light blue', command=CtrlPt.SetStart)
                b1.grid(row=x,column=2,sticky='NW')
                b1.deselect()

                b2 = tk.Radiobutton(frame,variable=CtrlPt.marche, value=1, text=' STOP ',bg='light blue', command=CtrlPt.SetStop)
                b2.grid(row=x,column=4,sticky='NW')
                b2.select()

                b3 = tk.Radiobutton(frame,variable=CtrlPt.marche, value=2, text=' BACK ', bg='light blue', command=CtrlPt.SetBack)
                b3.grid(row=x,column=6,sticky='NW')
                b3.deselect()
                Puissance = tk.Scale(frame, variable=CtrlPt.speed, orient=tk.HORIZONTAL, length=274,bg='light blue',
                                 showvalue=0, from_=0, to=200, tickinterval=20, label="POWER",
                                 command=CtrlPt.SetPower)

                Puissance.grid(row=x+2, column=2, columnspan=10)
                Puissance.set(0)
                Puissance.config(state='disabled')
                Puissance.config(bg='gray')
                CtrlPt.PwrWidget = Puissance

                Label4 = tk.Label(frame, text="LIGHT", bg='light blue')
                Label4.grid(row=x, column=13, columnspan=2)

                b4 = tk.Radiobutton(frame, variable=CtrlPt.light, value=1, text='ON', bg='light blue',
                                    command=CtrlPt.LightOn)
                b4.grid(row=x + 2, column=13, sticky='N')
                b4.deselect()

                b5 = tk.Radiobutton(frame, variable=CtrlPt.light, value=0, text='OFF', bg='light blue',
                                    command=CtrlPt.LightOff)
                b5.grid(row=x + 2, column=14, sticky='N')
                b5.select()

            elif CtrlPt.CP.type=='Servo':
                print('Servo:', CtrlPt.CP.name)
                frameS1 = tk.Frame(frame, width=80, height=50, borderwidth = 6, bg='light blue', relief="ridge")
                frameS1.grid(row=x,column=2, columnspan=2, rowspan=2)

                b1 = tk.Radiobutton(frameS1,variable=CtrlPt.angle1, value=0, text='LEFT/RIGHT',bg='light blue', command=CtrlPt.SetForkLeft1)
                b1.grid(row=x,column=2,sticky='W')
                b1.select()

                b2 = tk.Radiobutton(frameS1,variable=CtrlPt.angle1, value=1, text='', bg='light blue', command=CtrlPt.SetForkRight1)
                b2.grid(row=x,column=3,sticky='W')
                b2.deselect()

                T1 = tk.Button(frameS1, text=' ADJUST ',bg='light blue', command=CtrlPt.SetTrim1)
                T1.grid(row=x+1,column=2,columnspan=2)
                T1.config(bg='light blue')
                CtrlPt.TrimButton1 = T1

                frameS2 = tk.Frame(frame, width=80, height=50, borderwidth = 6, bg='light blue', relief="ridge")
                frameS2.grid(row=x,column=4, columnspan=2, rowspan=2)
                b3 = tk.Radiobutton(frameS2,variable=CtrlPt.angle2, value=2, text='LEFT',bg='light blue', command=CtrlPt.SetForkLeft2)
                b3.grid(row=x,column=4,sticky='NW')
                b3.select()
                b4 = tk.Radiobutton(frameS2,variable=CtrlPt.angle2, value=3, text='RIGHT', bg='light blue', command=CtrlPt.SetForkRight2)
                b4.grid(row=x,column=5,sticky='NW')
                b4.deselect()

                T2 = tk.Button(frameS2, text='  ADJUST ',bg='light blue', command=CtrlPt.SetTrim2)
                T2.grid(row=x+1,column=4,columnspan=2)
                T2.config(bg='light blue')
                CtrlPt.TrimButton2 = T2

                frameS3 = tk.Frame(frame, width=80, height=50, borderwidth = 6, bg='light blue', relief="ridge")
                frameS3.grid(row=x,column=6, columnspan=2, rowspan=2)
                b5 = tk.Radiobutton(frameS3,variable=CtrlPt.angle3, value=4, text='LEFT',bg='light blue', command=CtrlPt.SetForkLeft3)
                b5.grid(row=x,column=6,sticky='NW')
                b5.select()

                b6 = tk.Radiobutton(frameS3,variable=CtrlPt.angle3, value=5, text='RIGHT', bg='light blue', command=CtrlPt.SetForkRight3)
                b6.grid(row=x,column=7,sticky='NW')
                b6.deselect()

                T3 = tk.Button(frameS3, text=' ADJUST  ',bg='light blue',command=CtrlPt.SetTrim3)
                T3.grid(row=x+1,column=6,columnspan=2)
                T3.config(bg='light blue')
                CtrlPt.TrimButton3 = T3

                cptServo = cptServo + 1

            x=x+5
            index = index + 1
    def clear_tl(self):
        self.tl.destroy()
#
# Reading the constant values from 'common.h with a (very) simplifed parser.
#
CTE=Constante("common.h")       # From ParseCommonHeader.py
CTE.ParseFile()

CtrlServerLst = []       # ControlServers without the HMI aspect
CFG = CFG.XMLConfig(CTE.XML_cfgFile, "Locomotive", "TrackSwitch")       # TODO create constant for 'tag' like Locomotive and TrackSwith
CtrlServerLst =CFG.ParseXML()

CtrPointFull = []

ESP = ESP(CtrlServerLst) # get the liste of Server, contain only communicationa artefacts

# Connecting to ESP32 module from the application, for sending Power Orders / Lightg
root=tk.Tk()            # This variable is required for the initialisation of the control points.
root.withdraw()         # Do not display root window

for i in range (0,len(CtrlServerLst)):
    CtrlPoint = CtrlServerLst[i]                # Get the Control Server aspect
    ControlServer = CtrlServer(CtrlPoint,ESP)   # Initialize HMI with both Server and HMI control aspect
    CtrPointFull.append(ControlServer)

app1 = ControlPointIHM(root,CtrPointFull,"Control Center")  # Start the HMI
while 1:
    root.update_idletasks()
    root.update()
    time.sleep(0.01)





