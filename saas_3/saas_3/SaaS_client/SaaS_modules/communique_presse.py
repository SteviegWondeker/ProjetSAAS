import urllib.parse

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font




class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.cadreapp=Frame(self.root)
        self.cadres={}
        self.cadreapp.pack()
        self.cadreactif=None
        self.creercadres()
        self.changercadre("Communiqué")
        self.InfoCompagnie()

class Cadre_Communique(Frame):
    def __init__(self, root):
        root.minsize(width=700, height=500)
        root.maxsize(width=700, height=600)
        Frame.__init__(self, root)
        Grid.config(self)
        self.InfoCompagnie()
        self.TextFrame()
        # self.OtherInfos()

    def InfoCompagnie(self):

        self.infoCompagnieMethode = StringVar()
        self.infoCompagnieMethode.set("infoCom")

        self.list_membre= None
        self.infoframe = LabelFrame(self,text="Info Communiqué",height= 120,width =600)
        self.infoframe.grid(row= 0, column=0)
        self.infoframe.grid_propagate(0)

        self.label_nom_projet = Label(self, text="Choisir une date:", font=("Arial", 10)).place(x=310,y=30 )
        
        
        
        self.list_nom_projet = ttk.Combobox(self, values=0).place(x=440,y=50)
        self.infoframe.infocom= Label(self.infoframe, text = "Compagnie :").place(x = 0,y = 20)  
        self.infoframe.infoCom= Entry(self.infoframe, width=15,font=("Arial",16)).place(x=75,y=20)

        self.label_choix_existant = Label(self, text="Choisir une adresse:", font=("Arial", 10)).place(x=310,y=50 )
       
        # self.list_nom_projet.grid        (row=0, column=2,sticky='w')
        self.browseButton = Button(self.infoframe, text="Ajoutrer Compagnie").place(x = 125,y = 65) 
        self.enregistrer = Button(self.infoframe, text="Enregistrer").place(x = 0,y = 65) 

       
        self.cancelButton = Button(self.infoframe, text="Annuler").place(x = 70,y = 65) 
        # self.btn_annuler.grid               (row=3, column=1)
        # self.btn_valider.grid                (row=3, column=2)


  

    def TextFrame(self):
        self.logframe = LabelFrame(self,text="Text",height= 450,width =390,padx=15)
        self.logframe.grid_propagate(0)
        
        text_area = scrolledtext.ScrolledText(root, 
                                      wrap =WORD, 
                                      width = 40, 
                                      height = 10, 
                                      font = ("Times New Roman",
                                              15))
  
        text_area.grid(column = 0,row=2, pady = 10, padx = 10)
       

        # self.btn_annuler = Button(self, text="Annuler", font=("Arial", 10)).place(x=30,y=120)
        # self.btn_valider = Button(self, text="Envoyer", font=("Arial", 10))

        
      


class Modele():
    def __init__(self,parent):
        self.parent=parent
    def printMessage():
        print("Wow this actually worked!")

class Controleur():
    def __init__(self):
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
if __name__ == '__main__':
 root = Tk()
 root.title("COMMUNIQUÉ DE PRESSE ")
 tif= Cadre_Communique(root)
 root.mainloop()

