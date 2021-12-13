import urllib.parse

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font




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
        # root.minsize(width=700, height=500)
        # root.maxsize(width=700, height=600)
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

        self.label_choix_existant = Label(self, text="Choisir votre courriel:", font=("Arial", 10)).place(x=310,y=50 )
       
        # self.list_nom_projet.grid        (row=0, column=2,sticky='w')
        self.browseButton = Button(self.infoframe, text="Ajoutrer Compagnie").place(x = 125,y = 65) 
        self.enregistrer = Button(self.infoframe, text="Enregistrer").place(x = 0,y = 65) 

       
        self.cancelButton = Button(self.infoframe, text="Annuler").place(x = 70,y = 65) 
        # self.btn_annuler.grid               (row=3, column=1)
        # self.btn_valider.grid                (row=3, column=2)


  

    def TextFrame(self):
        
        self.TextMethode = StringVar()
        self.TextMethode.set("textcommunique")

        self.infoframe = LabelFrame(self,text="Communiqué de presse ",height=60,width =600)
        self.infoframe.grid(row= 2, column=0)
        self.infoframe.grid_propagate(0)
        self.btn_annuler = Button(self, text="Annuler", font=("Arial", 10)).place(x=250,y=140)
        self.btn_valider = Button(self, text="Envoyer", font=("Arial", 10)).place(x=350,y=140)
        self.btn_visualiser = Button(self, text="Visualiser", font=("Arial", 10)).place(x=150,y=140)
        self.btn_background = Button(self, text="Background", font=("Arial", 10)).place(x=450,y=140)


        self.text_area = scrolledtext.ScrolledText(root, 
                                      wrap =WORD, 
                                      width = 40, 
                                      height = 10, 
                                      font = ("Times New Roman",
                                              15))
  
        self.text_area.grid(column = 0,row=2, pady = 10, padx = 10)       

    # def VisualisationFrame(self):
        # UNE FOIS LE BTN VISUALISÉ CLIQUE LE WIDGET S'OUVRE
        # PERMET D'AVOIR UN LABEL POUR VISUALISER LE COMMUNIQUE
        # BTN ENREGISTRER POUR L,ENV DNS LA BD
        # BTN CORRIGER POUR RETOURNER VERS LE TEXTE 
        
    # def ChoixBackground(self):
        #BTN BACKGROUND
        # OUVRE UNE FENETRE POUR CHOISIR LE BACKGROUND DEP DE LA COMPAGNIE
        # BTN SAUVEGARDER ENV L'IMAGE A LA BD
        # METTRE L'IMAGE COMME BACKGROUND
        # BTN RETOUR POUR RETOURNER À LA PAGE DU COMMUNIQUÉ

    # def get_infoCompagnie(self):    
        # get le nom de la compagnie 
        # get le courriel de la compagnie
        # get le responsable de la compagnie(ajouter en haut nom responsable)

    # def date(self):
        # checker si ne pas ajouter a la bd 
        # avoir un format date     
    
      


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

