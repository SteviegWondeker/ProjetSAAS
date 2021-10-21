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

    def creertableau(self):
        f = Frame(self.cadre_gestion)
        f.pack(side=TOP, fill=BOTH, expand=Y)

        self.tableau = ttk.Treeview(show = 'headings')

        self.tableau.bind("<Double-1>",self.selectionner_projet(self.tableau.get_children))

        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tableau.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tableau.xview)
        self.tableau['yscroll'] = ysb.set
        self.tableau['xscroll'] = xsb.set

        # add tableau and scrollbars to frame
        self.tableau.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
    
    def ecriretableau(self):
        for i in self.tableau.get_children():
            self.tableau.delete(i)
        for item in self.data:
            self.tableau.insert('', 'end', values=item)

    def integretableau(self,listemembre,entete):
        self.data=listemembre
        self.colonnestableau = entete

        self.tableau.config(columns=self.colonnestableau)
        n=1
        for i in self.colonnestableau:
            no="#"+str(n)
            self.tableau.heading(no, text=i)
            n+=1

        self.ecriretableau()

    def form_modifier_projet(self):
        self.changercadre("modifier_projet")

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

        self.creertableau()
        listeprojets=self.parent.trouverprojets()
        entete=["Nom du projet","date de début","date de fin"]
        self.integretableau(listeprojets,entete)

        self.btn_modifier_projet = Button(self.cadre_gestion,text="Modifier projet", font=("Arial", 12),
                                         padx=10, pady=10, command=self.form_modifier_projet)

        self.btn_supprimer_projet = Button(self.cadre_gestion,text="Supprimer projet", font=("Arial", 12),
                                         padx=20, pady=10, command=self.supprimer_projet)

        infos_generals=["Nom du projet","Date de début","Date de fin","Responsable","Budget"]
        info_tâche=["Nom de tâche","Description","Deadline","Responsable"]

        self.creertableau()
        self.integretableau(self.afficher_infos_projet(self.selection),infos_generals)

        self.btn_modifier_projet.pack()
        self.btn_supprimer_projet.pack()

        return self.cadre_gestion

    def refresh(self):
        self.list_membre= self.list_nom_projet.get()
        self.listbox = Listbox(self.cadre_gestion, font=("Arial", 16), selectmode="multiple")
        
        self.listbox.grid (row=3, column=1, columnspan='10')

        self.listemodules=self.parent.trouvermembres("Cineclub")

        entete="modules disponibles"
        for items in self.listemodules:
            self.listbox.insert(END, items)

    def supprimer_projet(self):
        rep=messagebox.askyesno("Supression","Voulez-vous confirmer la supression du projet ?")
        if not rep:
            self.root.destroy()
    
    def afficher_infos_projet(self,projet):
        infos=self.parent.trouver_projet_infos
    
    def selectionner_projet(self,projet):
        self.selection = projet
        print(self.selection)



class Modele():
    def __init__(self,parent):
        self.parent=parent
        print(sys.argv)
        self.usager=sys.argv[2].split()
        self.inscrireusager(self.usager)

    def inscrireusager(self,dictinfo):
        self.nom=dictinfo[0]
        self.compagnie={"nom":dictinfo[2],
                        "id":dictinfo[4]}

class Controleur:
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"
        #self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()


    def trouver_projets_par_compagnie(self):
        url = self.urlserveur+"/trouver_projet_par_compagnie"
        params ={"id": self.modele.compagnie["id"]}
        #params = {self.modele.usager[1]}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

    def trouvermembres(self, comp):
        url = self.urlserveur+"/trouver_membres_par_compagnie"
        params = {"comp": comp}
        reptext=self.appelserveur(url, params)

        mondict=json.loads(reptext)
        return mondict
    
    def trouver_projet_infos(self, comp):
        url = self.urlserveur+"/trouver_projet_infos"
        params = {"comp": comp}
        reptext=self.appelserveur(url, params)

        mondict=json.loads(reptext)
        return mondict

    def trouverprojets(self):
        url = self.urlserveur+"/trouverprojets"
        params = {}
        reptext=self.appelserveur(url,params)

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