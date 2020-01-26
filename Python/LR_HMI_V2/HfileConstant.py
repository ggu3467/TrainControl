#
# This piece of software is under the GPL licence https://www.gnu.org/licenses/gpl-3.0.fr.html
# Thanks for considering letting this licence as part the source code
#
import re       # 're' stands for Regular Expression

class Constante:
    def __init__(self, filename):
        self.file = filename

    def ParseLine(self, str1):
    # ----------------------------------------------------------------------------------------------#
    # The client application is in Python and the server application in C code...
    # But these two applications need to share some technical value, and in particular the communication constants.
    #
    # Each of these constants matches a function to be performed by the server module.
    # In order to ease the developpemeent and to avoid some mistakes, the value of these constants
    # are shared between client and server code.
    #
    # The technique is to have a simple '.h' file which can easily be parsed to extract the value.
    #
    # The python variable will be created  using the exec funcion...
    #
    # '#define CODE1 12345' will become 'exec('CODE1','=','12345).
    #
    # WARNING: this code is only able to parse very basic '.h' file.
    #
    # The "parser" only recognise lines such as;
    # '#define  VAR_NAME1   12345
    # '#define  VAR_NAME2     0x90
    #
    # '#define  FileName    "constant.h"
    # '#define  XMLFileName "ControlServer.xml"
    #
    # Something like this will not be accepted:
    #
    # '# define VAR_NAME    10
    # '# define VAR_NAME1   (VAR_NAME+10)
    # '# define VAR_NAME1   /* bla bla */  12345
    #

    #
    # Reading the constant values from 'common.h with a (very) simplifed parser.
    #
    # This shall be executed at the top level
        VarName = ""
        VarValue = 0

        str2 = str1.split(' ')
        keyword = str2[0].lower()

        cpt = 0
        if (keyword == "#define"):
            for keyword in str2:
                # Skip all empty string
                if keyword == '':
                    continue
                # First state: the first keyword shall '#define'
                if (keyword.lower() == "#define") and (cpt == 0):
                    cpt = cpt + 1
                    define = 1
                    continue
                # Secund state: an identifier is expected, only in capital letter
                pName = re.compile('[A-Z]+')
                s1 = pName.match(keyword)
                if cpt == 1 and s1:
                    cpt = cpt + 1
                    #                print("S1: Match found",keyword, s1.string)
                    VarName = s1.string
                    continue

                # Third state: a value is expected as integer in decimale or in hexadecimal.
                pValue = re.compile('[0-9x]+')
                s1 = pValue.match(keyword)
                if cpt < 3 and s1:
                    cpt = cpt + 1
                    if len(s1.string) > 2:
                        hex = s1.string[0] + s1.string[1]
                        if (hex == '0x'):
                            #                        print("Found hexa value",pValue)
                            VarValue = int(s1.string[2:], 16)
                            #                        print("Found hexa value", VarValue)
                            break
                        else:
                            VarValue = int(s1.string)
                            break
                    else:
                        #                    print("S2: Match found",keyword, s1.string)
                        VarValue = int(s1.string)
                        break
                    break

                pValue = re.compile('\"[A-Za-z_.]+\"')
                s1 =  pValue.match(keyword)
                if cpt < 3 and s1:
                    cpt = cpt + 1
                    if len(s1.string) > 2:
                        VarValue = s1.string
                        break
                    break

                # Only 3 states
                if cpt >= 3:
                    break
        return VarName, VarValue

    def ParseFile(self):
        cnt = 1
        fp = open(self.file, 'r')
        line = fp.readline()

        while line:
#            print("Line {}: {}".format(cnt, line.strip()))
            VarName, VarValue = self.ParseLine(line)
            if VarName != "":
#                print("Name:", VarName, "Value:", VarValue)
# TRY numerical value first
                try:
                    VarValuex = int(VarValue)
                    exec("self.%s = %d" % (VarName, VarValue))  # DYNAMICALLY CREATE VARIABLE AND ASSIGN VALUE

#Exception imply a string was provided
                except ValueError:
                    exec("self.%s = %s" % (VarName, VarValue))  # DYNAMICALLY CREATE VARIABLE AND ASSIGN VALUE
                    pass  # it was a string, not an int.

            line = fp.readline()
            cnt += 1

if __name__ == "__main__":
    CTE=Constante("common.h")
    CTE.ParseFile()

    print(CTE.PORT)
    print(CTE.FWD_ORDER)