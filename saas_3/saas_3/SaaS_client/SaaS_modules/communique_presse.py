# -*- Encoding: UTF-8 -*-
import urllib.request
import urllib.parse
import json

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk

import sys
from subprocess import Popen


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


    def creercadres(self):
        self.cadres["Communiqué"]=self.creer_cadre_communique()

    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()

    def creer_cadre_communique(self):
        self.root.title("Communique")
        self.cadre_gestion = Frame(self.cadreapp)
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

        self.list_membre= None
        self.infoframe = LabelFrame(self,text="Info Compagnie",height= 120,width =300)
        self.infoframe.grid(row= 0, column=0)
        self.infoframe.grid_propagate(0)

        self.label_nom_projet = Label(self.cadre_gestion, text="Nom du projet", font=("Arial", 12))
        self.list_nom_projet = ttk.Combobox(self.cadre_gestion, values=0)
        self.infoframe.infocom= Label(self.infoframe, text = "Compagnie :").place(x = 0,y = 30)  
        self.infoframe.infoCom= Entry(self.infoframe, width=15,font=("Arial",16)).place(x=75,y=30)

        self.label_choix_existant = Label(self.cadre_gestion, text="choisir un role existant : ", font=("Arial", 12))
        self.traceButton = Button(self.infoframe, text="Enregistrer").place(x = 0,y = 65) 

        self.comboBox_choix_du_role = ttk.Combobox(self.cadre_gestion)
        self.tableau = ttk.Treeview(self.cadre_gestion, columns=('modules'))
        self.btn_inscrire_modules = Button(self.cadre_gestion, text="Rafrachir", font=("Arial", 12), padx=10, pady=10, command=self.refresh)
        self.cancelButton = Button(self.infoframe, text="Annuler").place(x = 70,y = 65) 

        self.btn_annuler = Button(self.cadre_gestion, text="Annuler", font=("Arial", 12), padx=10, pady=10)
        self.btn_retour = Button(self.cadre_gestion, text="Valider", font=("Arial", 12), padx=10, pady=10)

        self.listbox = Listbox(self.cadre_gestion, font=("Arial", 16), selectmode="multiple")



        self.label_nom_projet.grid        (row=1, column=1, sticky='w')
        self.list_nom_projet.grid        (row=1, column=2, sticky='w')
        self.browseButton = Button(self.infoframe, text="Ajoutrer Compagnie").place(x = 125,y = 65) 

        self.label_choix_existant.grid      (row=2, column=1)
        self.comboBox_choix_du_role.grid    (row=2, column=2)
        self.btn_inscrire_modules.grid      (row=2, column=3)
        self.listbox.grid (row=3, column=1, columnspan='10')

        self.btn_annuler.grid               (row=5, column=1)
        self.btn_retour.grid                (row=5, column=2, sticky='w')

        return self.cadre_gestion

    def refresh(self):
        self.list_membre= self.list_nom_projet.get()
        self.listbox = Listbox(self.cadre_gestion, font=("Arial", 16), selectmode="multiple")

        self.listbox.grid (row=3, column=1, columnspan='10')

    def TextFrame(self):
        self.logframe = LabelFrame(self,text="Text",height= 450,width =390,padx=15)
        self.logframe.grid_propagate(0)

        self.listemodules=self.parent.trouvermembres("Cineclub")
        self.logframe.grid_rowconfigure(0,weight =1)
        self.logframe.grid_columnconfigure(0,weight=1)

        entete="modules disponibles"
        for items in self.listemodules:
            self.listbox.insert(END, items)
        xscrollbar = Scrollbar(self.logframe,orient = HORIZONTAL)
        xscrollbar.grid(row=1, column=1, sticky=E+W,columnspan=2)

        yscrollbar = Scrollbar(self.logframe)
        yscrollbar.grid(row=0, column=3, sticky=N+S)

class Modele():
    def __init__(self,parent):
        self.parent=parent
        print(sys.argv)
        self.usager=sys.argv[2].split()
        self.inscrireusager(self.usager)
        text = Text(self.logframe,width=50,height=60, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        text.grid(row=0, column=1, columnspan=2)
        # attach listbox to scrollbar
        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)

    def inscrireusager(self,dictinfo):
        self.nom=dictinfo[0]
        self.compagnie={"nom":dictinfo[2],
                        "id":dictinfo[4]}
        button_1 = Button(self.logframe, text="Visualiser", command=printMessage)
        button_1.grid(row=2,column= 1)

class Controleur:
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"
        #self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()
        button_2 = Button(self.logframe, text="Envoyer", command=printMessage)
        button_2.grid(row=2,column= 2)

        self.logframe.grid(row=0,column =1,rowspan=5)

    def trouver_projets_par_compagnie(self):
        url = self.urlserveur+"/trouver_projet_par_compagnie"
        params ={"id": self.modele.compagnie["id"]}
        #params = {self.modele.usager[1]}
        reptext=self.appelserveur(url,params)
    # def OtherInfos(self):
    #     self.otherFrame = LabelFrame(self,text="Other Function",height= 400,width =300)
    #     self.otherFrame.grid(row=4, column=0)
    #     self.otherFrame.grid_propagate(0)

        mondict=json.loads(reptext)
        return mondict
    #     OpenPreviousCaseFile = Button(self.otherFrame, text="Open previous Case File", command=printMessage,height = 4, width =25)
    #     OpenPreviousCaseFile.grid(row=5,column= 0,pady=5)

    def trouvermembres(self, comp):
        url = self.urlserveur+"/trouver_membres_par_compagnie"
        params = {"comp": comp}
        reptext=self.appelserveur(url, params)
    #     OpenPreviousTracingResult = Button(self.otherFrame, text="Open previous Tracing Result ", command=printMessage,height = 4, width =25)
    #     OpenPreviousTracingResult.grid(row=6,column= 0,pady=5)

        mondict=json.loads(reptext)
        return mondict
    #     OpenMenualbtn = Button(self.otherFrame, text="User Manual", command=printMessage,height =4, width =25)
    #     OpenMenualbtn.grid(row=7,column= 0,pady=5)

    #     AboutBtn = Button(self.otherFrame, text="About", command=printMessage,height = 4, width =25)
    #     AboutBtn.grid(row=8,column= 0,pady=5)

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url, data)
        reptext=rep.read()
        return reptext
def printMessage():
    print("Wow this actually worked!")
root = Tk()
root.title("COMMUNIQUÉ DE PRESSE ")
tif= Cadre_Communique(root)
root.mainloop()

if __name__ == '__main__':
    c=Controleur() 