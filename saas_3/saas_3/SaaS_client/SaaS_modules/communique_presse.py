from tkinter import *
from tkinter import font
class Cadre_Communique(Frame):
    def __init__(self, root):
        root.minsize(width=700, height=500)
        root.maxsize(width=700, height=500)
        Frame.__init__(self, root)
        Grid.config(self)
        self.InfoCompagnie()
        self.TextFrame()
        # self.OtherInfos()

    def InfoCompagnie(self):

        self.infoCompagnieMethode = StringVar()
        self.infoCompagnieMethode.set("infoCom")
        
        self.infoframe = LabelFrame(self,text="Info Compagnie",height= 120,width =300)
        self.infoframe.grid(row= 0, column=0)
        self.infoframe.grid_propagate(0)

        self.infoframe.infocom= Label(self.infoframe, text = "Compagnie :").place(x = 0,y = 30)  
        self.infoframe.infoCom= Entry(self.infoframe, width=15,font=("Arial",16)).place(x=75,y=30)

        self.traceButton = Button(self.infoframe, text="Enregistrer").place(x = 0,y = 65) 

        self.cancelButton = Button(self.infoframe, text="Annuler").place(x = 70,y = 65) 
        
        self.browseButton = Button(self.infoframe, text="Ajoutrer Compagnie").place(x = 125,y = 65) 

    
    def TextFrame(self):
        self.logframe = LabelFrame(self,text="Text",height= 450,width =390,padx=15)
        self.logframe.grid_propagate(0)

        self.logframe.grid_rowconfigure(0,weight =1)
        self.logframe.grid_columnconfigure(0,weight=1)

        xscrollbar = Scrollbar(self.logframe,orient = HORIZONTAL)
        xscrollbar.grid(row=1, column=1, sticky=E+W,columnspan=2)

        yscrollbar = Scrollbar(self.logframe)
        yscrollbar.grid(row=0, column=3, sticky=N+S)

        text = Text(self.logframe,width=50,height=60, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        text.grid(row=0, column=1, columnspan=2)
        # attach listbox to scrollbar
        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)

        button_1 = Button(self.logframe, text="Visualiser", command=printMessage)
        button_1.grid(row=2,column= 1)

        button_2 = Button(self.logframe, text="Envoyer", command=printMessage)
        button_2.grid(row=2,column= 2)

        self.logframe.grid(row=0,column =1,rowspan=5)

    # def OtherInfos(self):
    #     self.otherFrame = LabelFrame(self,text="Other Function",height= 400,width =300)
    #     self.otherFrame.grid(row=4, column=0)
    #     self.otherFrame.grid_propagate(0)

    #     OpenPreviousCaseFile = Button(self.otherFrame, text="Open previous Case File", command=printMessage,height = 4, width =25)
    #     OpenPreviousCaseFile.grid(row=5,column= 0,pady=5)

    #     OpenPreviousTracingResult = Button(self.otherFrame, text="Open previous Tracing Result ", command=printMessage,height = 4, width =25)
    #     OpenPreviousTracingResult.grid(row=6,column= 0,pady=5)

    #     OpenMenualbtn = Button(self.otherFrame, text="User Manual", command=printMessage,height =4, width =25)
    #     OpenMenualbtn.grid(row=7,column= 0,pady=5)

    #     AboutBtn = Button(self.otherFrame, text="About", command=printMessage,height = 4, width =25)
    #     AboutBtn.grid(row=8,column= 0,pady=5)

def printMessage():
    print("Wow this actually worked!")
root = Tk()
root.title("COMMUNIQUÉ DE PRESSE ")
tif= Cadre_Communique(root)
root.mainloop()

