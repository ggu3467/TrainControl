import tkinter as tk

from   HfileConstant     import Constante           # Global constant values from 'common.h' file
import XMLConfig         as CFG                     # XML Read (not Write Yet)...

global root

class AnimatedIHM:
    def __init__(self, _root, _Line, _Column, _Width, _Height, _Name ):
        self.name    = _Name              # Server/ControlPoint Name
        self.allure  = 0                # Initially stopped

        self.master = _root
        self.tl = tk.Toplevel(root)   # Link with master window
        self.tl.withdraw()              # Dp Not display empty window

        self.Line   = _Line
        self.Column = _Column
        self.Width  = _Width
        self.Height = _Height

        self.create(root, self.master, "COCUCO")

    def create(self, master, ControlLst,  Nom):
        Locomotive = tk.Canvas(tk.Toplevel(master), bg='light blue', height=600, width=1200, borderwidth =5)
        Locomotive.grid(row=50, column=14, rowspan=1, sticky='NW', padx=4, pady=4)

        frameTitre = tk.Frame(self.master, width=700, borderwidth = 5, height=30,bg='dark blue', relief="sunken", highlightcolor="red", highlightthickness=2 )
        frameTitre.grid(row=0, column=14)
        LabelTitre = tk.Label(frameTitre, text="*** Network view ***", font="Arial 14", height=2, bg='light blue')
        LabelTitre.grid(row=0, column=14)

        x        = 2
        index    = 1
        cptServo = 0
        for _row in range (1,self.Line):
            for _column in range (1,self.Column):
                b1 = tk.Button(frameTitre, text=' ADJUST ',bg='light blue')
                b1.grid(row=_row,column=_column,sticky='NW')




if __name__ == "__main__":
    CTE = Constante("common.h")
    CTE.ParseFile()

    root=tk.Tk()
    hmi = AnimatedIHM(root,10,20,400,800, "NETWORK")
    root.mainloop()

#    img1 = tk.PhotoImage(file='Montagnarde2.png')
#    can1 = tk.Canvas(root, width = 200, height = 200, bg = 'white')
#    photo =can1.create_image(150,150,image=img1)
#    can1.pack()
