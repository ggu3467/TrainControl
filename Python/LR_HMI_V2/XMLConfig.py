#
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
#

#External Import
from xml.dom import minidom

# Local import
from   HfileConstant import Constante

# Get all the description of the server from an XML file
#
# At present there two kind of server/application:
#
#   - MotorControl : one per locomotive (start, stop, reverse, speed/power and ligth
#   - ServerControl: up to 3 for an ESP32 module, for each:
#                       - OPEN and CLOSE a track switch
#                       - adjust the position for on and off position (TRIM VALE)
#
#       ## TODO the trim value are saved in a different (==> create a backup and save new value to regular file)

# The ctrlPoint class contains all the attributes need for the HMI initialisation.
class CtrlPoint:
    def __init__(self,Nom, Type, IPAdr, instance, port, valRight, valLeft, tagLoco, tagSwitch):
        self.name           = Nom
        self.ip             = IPAdr
        self.type           = Type
        self.numCtrlPoint   = instance
        self.port           = port
        self.TrimRight      = valRight
        self.TrimLeft       = valLeft
        self.TrimSelected   = 0
        self.tagLoco        = tagLoco
        self.tagSwitch      = tagSwitch


# The parser is very "basic", the two mains key are "Locomotive" and "trackSwitch"
class XMLConfig:
    def __init__(self, filename, _TagLoco, _TagServo):
        self.TagLocomotive = _TagLoco
        self.TagServo      = _TagServo
        self.doc = minidom.parse(filename)
        self.CtrlPointLst   = []


    def OLD_ParseXML(self):
        self.CtrlPointLoco  = []
        self.CtrlPointServo = []

        self.CtrlPointLoco  = self.ParseLocomotive(self.CtrlPointLoco)
        self.CtrlPointServo = self.ParseTrackSwith(self.CtrlPointServo)

        index = 0
        for Loco in self.CtrlPointLoco:
            self.CtrlPointLst.append(Loco)
            self.CtrlPointLst[index].numCtrlPoint = index
            index = index + 1

        for Servo in self.CtrlPointServo:
            self.CtrlPointLst.append(Servo)
            self.CtrlPointLst[index].numCtrlPoint = index
            index = index + 1

        return self.CtrlPointLst

    def ParseXML(self):
        self.CtrlPointLst = []

        self.CtrlPointLst = self.ParseLocomotive(self.CtrlPointLst)
        self.CtrlPointLst = self.ParseTrackSwith(self.CtrlPointLst)

        index = 0
        for cp in self.CtrlPointLst:
            self.CtrlPointLst[index].numCtrlPoint = index
            index = index + 1

        return self.CtrlPointLst

    def getNodeText(self,node):
        nodelist = node.childNodes
        result = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                result.append(node.data)
        return ''.join(result)

    def GetTrimValue(self,xmlRead, ValueName):
        if (xmlRead.getElementsByTagName(ValueName).length > 0):
            str = self.getNodeText(xmlRead.getElementsByTagName(ValueName)[0])
            value = int(str)
        #        print("GetTrimValue(xmlRead", ValueName, str, value)
        else:
            value = 0
        return value

    def ParseLocomotive(self,CtrlPointMotrice):
        locomotive = self.doc.getElementsByTagName(self.TagLocomotive)
        index = 0
        for mot in locomotive:
            name = mot.getElementsByTagName("name")[0]
            type = mot.getElementsByTagName("type")[0]
            ip   = mot.getElementsByTagName("ip")[0]
            NAME = self.getNodeText(name)
            TYPE = self.getNodeText(type)
            IP   = self.getNodeText(ip)

            print("NAME, TYPE, IP",NAME, TYPE, IP)
            CP = CtrlPoint(NAME, TYPE, IP,index,0,0,0,"","")
            CtrlPointMotrice.append(CP)

        return CtrlPointMotrice

    def ParseTrackSwith(self, CtrlPointServo):
        TrackSwitch = self.doc.getElementsByTagName(self.TagServo)
        for key in TrackSwitch:
            TrimRight = []
            TrimLeft = []
            name      = key.getElementsByTagName("name")[0]
            type      = key.getElementsByTagName("type")[0]
            ip        = key.getElementsByTagName("ip")[0]

            value = key.getElementsByTagName("TrimMin1")[0]

            valueMin = self.GetTrimValue(key, "TrimMin1")
            TrimRight.append(valueMin)
            valueMax = self.GetTrimValue(key, "TrimMax1")
            TrimLeft.append(valueMax)

            valueMin = self.GetTrimValue(key, "TrimMin2")
            TrimRight.append(valueMin)
            valueMax = self.GetTrimValue(key, "TrimMax2")
            TrimLeft.append(valueMax)

            valueMin = self.GetTrimValue(key, "TrimMin3")
            TrimRight.append(valueMin)
            valueMax = self.GetTrimValue(key, "TrimMax3")
            TrimLeft.append(valueMax)

            NAME      = self.getNodeText(name)
            TYPE      = self.getNodeText(type)
            IP        = self.getNodeText(ip)

            CP = CtrlPoint(NAME, TYPE, IP,-1,0,TrimRight,TrimLeft,"","")
            print("NAME, TYPE, IP",NAME, TYPE, IP)
            CtrlPointServo.append(CP)
        return CtrlPointServo

    def UpdateTrackSwitch(self, xmlFilename, ip, NumSwitch, MinValue, MaxValue):
        self.doc = minidom.parse(xmlFilename)
        TrackSwitch = self.doc.getElementsByTagName(self.TagServo)

        for key in TrackSwitch:
            ipNode = key.getElementsByTagName("ip")[0]
            IP = self.getNodeText(ipNode)
            if (ip == IP):
                TagMin = "TrimMin" + str(NumSwitch+1)           # Create the appropropriate TAG
                TagMax = "TrimMax"  + str(NumSwitch+1)
# TODO il faut vérifier que le TAG existe !
                maxVal = key.getElementsByTagName(TagMax)[0]    # Read current value
                minVal = key.getElementsByTagName(TagMin)[0]

                oldMinValue = minVal.firstChild.nodeValue       # Get previous values
                oldMaxValue = maxVal.firstChild.nodeValue
                print("Replacing minValue:"+oldMinValue+" by new value:"+str(MinValue))
                print("Replacing maxValue:"+oldMaxValue+" by new value:"+str(MaxValue))

                minVal.firstChild.nodeValue=MinValue            # Assign new values
                maxVal.firstChild.nodeValue=MaxValue

                with open('ControlServer_test.xml', 'w') as f:
                    f.write(self.doc.toxml())
                    f.close()

                break

        return CtrlPoint

if __name__ == "__main__":
    CTE = Constante("common.h")  # From ParseCommonHeader.py
    CTE.ParseFile()
    CtrlServerLst = []  # ControlServers without the HMI aspect


    XML= XMLConfig(CTE.XML_cfgFile, "Locomotive","TrackSwitch")
    CtrlServerLst=XML.ParseXML()
    XML.UpdateTrackSwitch(CTE.XML_cfgFile, "192.168.1.108",0 ,11,111)






