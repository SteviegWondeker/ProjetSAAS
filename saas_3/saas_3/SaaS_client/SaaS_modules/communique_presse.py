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
        self.canevas = Canvas(self.cadreapp,width=800,heigh=600)
        self.canevas.create_text(400,100,anchor= CENTER,text="Bienvenu a SaaS Communiqué Presse")
        self.canevas.pack()
        self.canevas.create_window(400,300,anchor=CENTER,text="section1")
        self.canevas.create_window(400,500,anchor=CENTER,text="section2")
        self.cadreapp.pack()

class Modele():
     def __init__(self,parent):
        self.parent=parent
        self.nom = nom
        self.compagnie = compagnie


class Controleur:
    def __init__(self):
        self.vue=Vue(self)
        print(sys.argv)
        self.urlserveur=sys.argv[1]
        usager=json.loads(sys.args[2])
        self.modele=Modele(self,usager[0],usager[1])
        self.vue.root.mainloop()

 
    def requeteserveur(self,fonc):
        leurl=self.urlserveur+"/requeteserveur"
        params = {"fonction":fonc}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        return rep

# fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string 
        rep=urllib.request.urlopen(url , data)
        reptext=rep.read()
        return reptext






if __name__ == '__main__':
    c=Controleur()