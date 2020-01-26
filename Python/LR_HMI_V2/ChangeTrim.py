#
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
#

#External Import
from tkinter import *

# Local import
#from HMI_LR_V2 import CtrlServer
import XMLConfig     as CFG
from   HfileConstant import Constante
from   UDP_Communication import UDP_comm as ESP     # Communication aspect of the projet

class ChangeTrim:
    def __init__(self, master, _ControlPoint, NumTrimmer, _commESP): #########################################
        self.allure = 0  # Initially stopped
        self.CTE=Constante("common.h")       # From ParseCommonHeader.py
        self.CTE.ParseFile()
        self.commESP = _commESP  # get the liste of Server, contain only communicationa artefacts
        self.ControlPoint =  _ControlPoint
        self.NumTrimmer   =  NumTrimmer

        self.top = Toplevel(master)  # Link with master window
        self.top.withdraw()  # Dp Not display empty window
        self.top.grab_set()

        self.CreateTrimScale(self.top)

    def SetTrimValueLeft(self, value):
        print("==> LEFT", value)
        self.ControlPoint.TrimLeft[self.NumTrimmer] = value
        self.commESP.MsgForkLeft[1] = self.NumTrimmer+1
        self.commESP.MsgForkLeft[2] = int(value)
        self.commESP.SendData(self.commESP.MsgForkLeft, self.ControlPoint.numCtrlPoint)
        return

    def SetTrimValueRight(self, value):
        print("==> RIGHT", value)
        self.ControlPoint.TrimRight[self.NumTrimmer] = value
        self.commESP.MsgForkRight[1] = self.NumTrimmer+1
        self.commESP.MsgForkRight[2] = int(value)
        self.commESP.SendData(self.commESP.MsgForkRight, self.ControlPoint.numCtrlPoint)
        return

    def ValidateRight(self):
        print("ValidateRight")
        return

    def ValidateLeft(self):
        print("ValidateRight")
        return

    def CreateTrimScale(self, master):

        Head = Canvas(Toplevel(master), bg='light blue', height=600, width=800, borderwidth=5)
        Head.grid(row=1, column=3, sticky='NW', padx=4, pady=4)

        frameTitre = Frame(Head, width=1200, borderwidth = 3, height=30,bg='dark blue', relief="sunken", highlightcolor="red", highlightthickness=2 )
        frameTitre.grid(row=0, column=3)
        LabelTitre = Label(frameTitre, text="*** Set the minimum and maximum values ​​of the servo motors ***", font="Arial 12", height=2, bg='light blue')
        LabelTitre.grid(row=0, column=3)

        Trim = Frame(Head, width=1200, borderwidth=5, height=30, bg='dark blue', relief="sunken",
                             highlightcolor="red", highlightthickness=2)
        Trim.grid(row=4, column=3, rowspan=1, sticky='NW', padx=4, pady=4)

        SetTrim = Frame(Trim, width=1200, height=50, borderwidth=6, bg='light blue', relief="ridge")
        SetTrim.grid(row=3, column=5, sticky='NW')
        Label1 = Label(SetTrim, text=self.ControlPoint.name + '\n' + self.ControlPoint.ip, font="Arial 12", height=3, width=15,
                          bg='light blue')
        Label1.grid(row=1, column=0, rowspan=3, padx=3)

        TrimmerRight = Scale(SetTrim, variable=self.ControlPoint.TrimRight[self.NumTrimmer], resolution=1, orient=HORIZONTAL, length=600,bg='light blue',
                                    showvalue=1, from_=0, to_= 90, tickinterval=5,
                                    command=self.SetTrimValueRight)
        TrimmerRight.set(self.ControlPoint.TrimRight[self.NumTrimmer])
        TrimmerRight.grid(row=1, column=1, columnspan=3)
        TrimmerRight.config(state='active')
        TrimmerRight.lower()
        TxtButton2 = 'RIGHT: '+str(self.ControlPoint.TrimRight[self.NumTrimmer])
        LeftButton = Button(SetTrim, text=TxtButton2,  bg='light blue', command=self.ValidateLeft)
        LeftButton.grid(row=1, column=4)

        QuitButton = Button(SetTrim, text="QUIT-SAVE", command=self.QuitSave)
        QuitButton.grid(row=2, column=4)

        TrimmerLeft = Scale(SetTrim, variable=self.ControlPoint.TrimLeft[self.NumTrimmer], orient=HORIZONTAL, length=600,bg='light blue',
                                      showvalue=25, from_=90, to_=180, tickinterval=5,
                                      command=self.SetTrimValueLeft)
        TrimmerLeft.set(self.ControlPoint.TrimLeft[self.NumTrimmer])
        TrimmerLeft.grid(row=3, column=1, columnspan=3)
        TrimmerLeft.config(state='active')
        TrimmerLeft.lower()


        TxtButton1 = 'LEFT:'+str(self.ControlPoint.TrimLeft[self.NumTrimmer])
        RightButton = Button(SetTrim, text=TxtButton1, bg='light blue', command=self.ValidateRight)
        RightButton.grid(row=3, column=4)

        print("Fin CreateTrimScale")

    def QuitSave(self):
        print("QUIT SAVE")
        minValue=self.ControlPoint.TrimLeft[self.NumTrimmer]
        maxValue=self.ControlPoint.TrimRight[self.NumTrimmer]
        print("ControlPoint:"+self.ControlPoint.name+" NumTrim:",self.NumTrimmer)
        print("TrimLeft, min value: " , minValue)
        print("TrimRight, maxValue: " , maxValue)
        XML = CFG.XMLConfig(self.CTE.XML_cfgFile, " ", "TrackSwitch")

#        def UpdateTrackSwitch(self, xmlFilename, ip, NumSwitch, MinValue, MaxValue):
        XML.UpdateTrackSwitch(self.CTE.XML_cfgFile, self.ControlPoint.ip, self.NumTrimmer, minValue, maxValue)

        self.top.destroy()

if __name__ == "__main__":
    CTE = Constante("common.h")  # From ParseCommonHeader.py
    CTE.ParseFile()
    CtrlServerLst = []  # ControlServers without the HMI aspect
    CFG = CFG.XMLConfig(CTE.XML_cfgFile, "Locomotive", "TrackSwitch")
    CtrlServerLst = CFG.ParseXML()

    root = Tk()  # This variable is require for the initialisation of the control points.
    root.winfo_toplevel().title("Changing the min and max values for piloting the servo")
    root.withdraw()  # Do not display root window

### 3 numéro du premier Servo
    CtrlPoint = CtrlServerLst[3]  # Get the Control Server aspect
    ESP = ESP(CtrlServerLst)  # get the liste of Server, contain only communicationa artefacts
    app1 = ChangeTrim(root, CtrlPoint, 1, ESP)  # Start the HMI
    root.mainloop()


