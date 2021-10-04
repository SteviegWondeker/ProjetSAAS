## -*- Encoding: UTF-8 -*-
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
        self.changercadre("Gestion")


    def creercadres(self):
        self.cadres["Gestion"]=self.creer_cadre_gestion()

    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()

    def creer_cadre_gestion(self):
        self.root.title("Gestion")
        self.cadre_gestion = Frame(self.cadreapp)
        
        self.list_membre= None

        self.label_nom_projet = Label(self.cadre_gestion, text="Nom du projet", font=("Arial", 12))
        self.list_nom_projet = ttk.Combobox(self.cadre_gestion, values=self.parent.trouverprojets())

        self.label_choix_existant = Label(self.cadre_gestion, text="choisir un role existant : ", font=("Arial", 12))

        self.comboBox_choix_du_role = ttk.Combobox(self.cadre_gestion)
        self.tableau = ttk.Treeview(self.cadre_gestion, columns=('modules'))
        self.btn_inscrire_modules = Button(self.cadre_gestion, text="Rafrachir", font=("Arial", 12), padx=10, pady=10, command=self.refresh)
        
        self.btn_annuler = Button(self.cadre_gestion, text="Annuler", font=("Arial", 12), padx=10, pady=10)
        self.btn_retour = Button(self.cadre_gestion, text="Valider", font=("Arial", 12), padx=10, pady=10)

        self.listbox = Listbox(self.cadre_gestion, font=("Arial", 16), selectmode="multiple")



        self.label_nom_projet.grid        (row=1, column=1, sticky='w')
        self.list_nom_projet.grid        (row=1, column=2, sticky='w')

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

        self.listemodules=self.parent.trouvermembres("Cineclub")

        entete="modules disponibles"
        for items in self.listemodules:
            self.listbox.insert(END, items)


class Modele():
    def __init__(self,parent):
        self.parent=parent
        
    def inscrireusager(self,dictinfo):
        self.nom=dictinfo[0][0][2]
        self.droit=dictinfo[0][0][4]
        self.titre=dictinfo[0][0][5]
        self.compagnie={"nom":dictinfo[1][0][0],
                        "id":dictinfo[0][0][0]}

class Controleur:
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"
        #self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()


    def trouverprojets(self):
        url = self.urlserveur+"/trouverprojets"
        params = {}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

    def trouvermembres(self, comp):
        url = self.urlserveur+"/trouver_membres_par_compagnie"
        params = {"comp": comp}
        reptext=self.appelserveur(url, params)

        mondict=json.loads(reptext)
        return mondict


    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url, data)
        reptext=rep.read()
        return reptext

if __name__ == '__main__':
    c=Controleur()