## -*- Encoding: UTF-8 -*-
import urllib.request
import urllib.parse
import json

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk

import sys
from subprocess import Popen
##################

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.cadreapp=Frame(self.root) # le cadre qui va afficher ou non tous les autres
        self.cadres={}
        self.tableaux = {}
        self.cadreapp.pack()
        self.cadreactif=None
        self.creercadres()

    def changercadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif = cadre
        self.cadreactif.pack()

    def creercadres(self):
         self.cadres["principal"]=self.creercadreprincipal()


    def creercadreprincipal(self):          # Alex
        self.root.title("SaaS - ADMIN")
        self.cadreprincipal = Frame(self.cadreapp, width=400, height=400)

        self.cadretitre = Frame(self.cadreprincipal, width=400, height=400)
        self.titreprincipal = Label(self.cadretitre, text="SaaS - ADMIN",
                                    font=("Arial", 18),
                                    borderwidth=2, relief=GROOVE)

        self.usagercourant = Label(self.cadretitre, text="ADMIN",# + ", " + usager.titre + " : " + usager.droit,
                                   font=("Arial", 14))
        self.titreprincipal.pack()
        self.usagercourant.pack()
        self.cadretitre.pack()

        # commande possible
        #self.cadrecommande = Frame(self.cadreprincipal, width=400, height=400)
        #btnsaction = []
        #for i in btnsaction:
        #    i.pack(side=LEFT, pady=10, padx=10)
        #self.cadrecommande.pack()

        self.options_list = self.parent.trouver_compagnies()
        self.value_inside = StringVar(self.cadreprincipal)
        self.value_inside.set("Option")
        self.menu_deroulant = ttk.OptionMenu(self.cadreprincipal, self.value_inside, self.options_list[0], *self.options_list, command=self.trouver_membres_par_compagnie)
        self.menu_deroulant.pack()
        self.cadrecontenu = Frame(self.cadreprincipal, width=600, height=400)
        self.cadrecontenu.pack()
        self.cadrepied = Frame(self.cadreprincipal, width=600, height=80)
        self.cadrepied.pack()

        self.creertableau(0)
        self.creertableau(1)


        return self.cadreprincipal

    def creertableau(self, id):             # Modifié par Alex
        f = Frame(self.cadrecontenu)
        f.pack(side=TOP, fill=BOTH, expand=Y, padx=(15, 0))

        self.tableaux[id] = ttk.Treeview(show='headings')

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tableaux[id].yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tableaux[id].xview)
        self.tableaux[id]['yscroll'] = ysb.set
        self.tableaux[id]['xscroll'] = xsb.set

        if id == 0:
            ######################### INSÉRER MÉTHODE POUR REFRESH 2e TABLE SELON SÉLECTION
            self.tableaux[0].bind("<ButtonRelease-1>", self.trouver_permissions_par_membre)
            pass

        # add tableau and scrollbars to frame
        self.tableaux[id].grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def integretableau(self, listeinfos, entete, id):       # Modifié par Alex
        self.data = listeinfos
        self.colonnestableau = entete

        self.tableaux[id].config(columns=self.colonnestableau)
        n = 1
        for i in self.colonnestableau:
            no = "#" + str(n)
            self.tableaux[id].heading(no, text=i)
            n += 1

        self.ecriretableau(id)

    def ecriretableau(self, id):        # Modifié par Alex
        for i in self.tableaux[id].get_children():
            self.tableaux[id].delete(i)
        for item in self.data:
            self.tableaux[id].insert('', 'end', values=item)

    def gerermembres(self):
        listemembres=self.parent.trouvermembres()
        entete=["identifiant","permission","titre"]
        self.integretableau(listemembres,entete, 0)

    def creation_compte(self):
        self.parent.creation_compte(nom,mdp)

    def avertirusager(self,titre,message):
        rep=messagebox.askyesno(titre,message)
        if not rep:
            self.root.destroy()

    def trouver_membres_par_compagnie(self, comp):
        listemembres = self.parent.trouver_membres_par_compagnie(comp)
        entete = ["identifiant", "permission", "titre"]
        self.integretableau(listemembres, entete, 0)

    def trouver_permissions_par_membre(self, evt):
        membre = None
        item = self.tableaux[0].selection()
        for i in item:
            membre = self.tableaux[0].item(i, "values")[0]
        if(membre):     # Safety au cas ou membre serait null
            listemembres = self.parent.trouver_permissions_par_membre(membre)
            entete = ["Rôles"]
            self.integretableau(listemembres, entete, 1)

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
        self.urlserveur = "http://127.0.0.1:5000"
        # self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.changercadre("principal")
        self.vue.root.mainloop()

    def telechargermodule(self, fichier):
        leurl = self.urlserveur + "/telechargermodule"
        params = {"fichier": fichier}
        reptext = self.appelserveur(leurl, params)
        rep = json.loads(reptext)
        fichier1 = open("./SaaS_modules/" + fichier, "w")
        fichier1.write(rep)
        fichier1.close()
        usager = json.dumps([self.modele.nom, self.modele.compagnie])
        pid = Popen([sys.executable, "./SaaS_modules/" + fichier, self.urlserveur, usager], shell=1).pid

    def testsimple(self):
        leurl = self.urlserveur
        r = urllib.request.urlopen(leurl)
        rep = r.read()
        dict = rep.decode('utf-8')
        print("testserveurSIMPLE", dict)

    def trouvermodules(self):
        url = self.urlserveur + "/trouvermodules"
        params = {}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    def trouverprojets(self):
        url = self.urlserveur + "/trouverprojets"
        params = {}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    def trouvermembres(self):
        url = self.urlserveur + "/trouvermembres"
        params = {}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    def trouver_compagnies(self):           # Alex
        url = self.urlserveur + "/trouvercompagnies"
        params = {}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    def trouver_membres_par_compagnie(self, comp):           # Alex
        url = self.urlserveur + "/trouver_membres_par_compagnie"
        params = {"comp": comp[0]}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    def trouver_permissions_par_membre(self, membre):           # Alex
        url = self.urlserveur + "/trouver_permissions_par_membre"
        params = {"membre": membre[0]}
        reptext = self.appelserveur(url, params)

        mondict = json.loads(reptext)
        return mondict

    # def identifierusager(self, nom, mdp):
    #     url = self.urlserveur + "/identifierusager"
    #     params = {"nom": nom,
    #               "mdp": mdp}
    #     reptext = self.appelserveur(url, params)
    #
    #     mondict = json.loads(reptext)
    #     print(mondict)
    #     if "inconnu" in mondict:
    #         self.vue.avertirusager("Inconnu", "Reprendre?")
    #     elif "Cineclub" not in mondict[1][0][0]:
    #         self.vue.avertirusager("Compte non autorisé", "Voulez-vous vous connecter avec un autre compte?")
    #     else:
    #         self.modele.inscrireusager(mondict)
    #         self.vue.creercadreprincipal(self.modele)
    #         self.vue.changercadre("principal")

    ####

    def creation_compte(self):
        # url = self.urlserveur+"/identifierusager"

        self.vue.creer_cadre_creation()
        self.vue.changercadre("creation")

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self, url, params):
        query_string = urllib.parse.urlencode(params)
        data = query_string.encode("ascii")
        url = url + "?" + query_string
        rep = urllib.request.urlopen(url, data)
        reptext = rep.read()
        return reptext


if __name__ == '__main__':
    c = Controleur()
    print("FIN DE PROGRAMME")