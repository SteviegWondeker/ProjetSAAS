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
        self.cadreapp.pack()
        self.cadreactif=None
        self.creercadres()
    
    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()
            
    def creercadres(self):
        self.cadres["login"]=self.creercadrelogin()
        self.cadres["creation"]=self.creer_cadre_creation()
        #self.cadres["principal"]=self.creercadreprincipal()
        
    def creercadrelogin(self):
        self.cadrelogin=Frame(self.cadreapp,width=800,height=400)
        
        self.loginlabel=Label(self.cadrelogin,text="Identification pour GestMedia",font=("Arial",18),
                              borderwidth=2,relief=GROOVE)
        
        self.loginlabnom=Label(self.cadrelogin,text="Nom",font=("Arial",14))
        self.loginnom=Entry(self.cadrelogin,font=("Arial",14),width=30)
        self.loginlabmdp=Label(self.cadrelogin,text="MotdePasse",font=("Arial",14))
        self.loginmdp=Entry(self.cadrelogin,font=("Arial",14),show="*",width=30)
        
        # les boutons d'actions
        self.btnannulerlogin=Button(self.cadrelogin,text="Annuler",font=("Arial",12),padx=10,pady=10,command=self.annulerlogin)
        self.btnidentifierlogin=Button(self.cadrelogin,text="Identifier",font=("Arial",12),padx=10,pady=10,command=self.identifierlogin)

        self.btn_creation=Button(self.cadrelogin,text="Creer un usager",font=("Arial",12),padx=10,pady=10,command=self.creation_compte)
        
        self.loginlabel.grid(row=10,column=10,columnspan=20,padx=10,pady=10,ipadx=10,ipady=10)
        self.loginlabnom.grid(row=20,column=10,sticky=E,padx=5,pady=5)
        self.loginnom.grid(row=20,column=20,padx=10,pady=5)
        self.loginlabmdp.grid(row=30,column=10,sticky=E,padx=5,pady=5)
        self.loginmdp.grid(row=30,column=20,padx=10,pady=5)
        
        self.btnannulerlogin.grid(row=40,column=20,sticky=W,padx=10,pady=10)
        self.btnidentifierlogin.grid(row=40,column=20,padx=10,pady=10)

        self.btn_creation.grid(row=40,column=30,padx=10,pady=10)
        
        return self.cadrelogin
    
    def creercadreprincipal(self, usager):
        self.root.title("GestionMedia")
        self.cadreprincipal=Frame(self.cadreapp,width=400,height=400)
        
        self.cadretitre=Frame(self.cadreapp,width=400,height=400)
        self.titreprincipal=Label(self.cadretitre,text="GestMedia"+" pour "+usager.compagnie["nom"],font=("Arial",18),
                              borderwidth=2,relief=GROOVE)
        
        self.usagercourant=Label(self.cadretitre,text=usager.nom+", "+usager.titre +" : "+usager.droit,font=("Arial",14))
        self.titreprincipal.pack()
        self.usagercourant.pack()
        self.cadretitre.pack()
        
        # commande possible
        self.cadrecommande=Frame(self.cadreprincipal,width=400,height=400)
        btnsaction=[]
        if usager.droit=="admin":
            btnsaction.append(Button(self.cadrecommande,text="Gestion de membres",
                                     font=("Arial",12),padx=10,pady=10,command=self.gerermembres))
        btnsaction.append(Button(self.cadrecommande,text="Gestion des projetsERP",
                                 font=("Arial",12),padx=10,pady=10,command=self.gererprojets))
        btnsaction.append(Button(self.cadrecommande,text="Modules disponiblesSaaS",
                                 font=("Arial",12),padx=10,pady=10,command=self.gerermodules))
        for i in btnsaction:
            i.pack(side=LEFT, pady=10,padx=10)
        self.cadrecommande.pack()
        self.cadrecontenu=Frame(self.cadreprincipal, width=600,height=400,bg="green")
        self.cadrecontenu.pack()
        self.cadrepied=Frame(self.cadreprincipal, width=600,height=80)
        self.cadrepied.pack()
        
        self.creertableau()
        self.cadres["principal"]=self.cadreprincipal
    
    def creertableau(self):
        f = Frame(self.cadrecontenu)
        f.pack(side=TOP, fill=BOTH, expand=Y)
                
        self.tableau = ttk.Treeview(show = 'headings')
        
        self.tableau.bind("<Double-1>",self.affichertelecharger)
        
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
               
    def affichertelecharger(self,evt):
        item = self.tableau.selection()
        for i in item:
            fichier=self.tableau.item(i, "values")[0]
        self.parent.telechargermodule(fichier)
        
        
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
    
    def afficherlogin(self,nom="",mdp=""):
        self.root.title("GestMedia: Identification")
        if nom:
            self.loginnom.insert(0,nom)
        if mdp:
            self.loginmdp.insert(0,mdp)
        self.loginnom.focus_set()
        self.changercadre("login")
        # centrer au depart
        #self.root.update()
        #self.centrerfenetre()
        
    def gerermembres(self):
        listemembres=self.parent.trouvermembres()
        entete=["identifiant","permission","titre"]
        self.integretableau(listemembres,entete)
             
    def gererprojets(self):
        listeprojets=self.parent.trouverprojets()
        entete=["compagnie","projet","date de fin"]
        self.integretableau(listeprojets,entete)
             
    def gerermodules(self):
        listemodules=self.parent.trouvermodules()
        entete=["modules disponibles"]
        self.integretableau(listemodules,entete)
    
    def annulerlogin(self):
        self.root.destroy()
        
    def identifierlogin(self):
        nom=self.loginnom.get()
        mdp=self.loginmdp.get()
        self.parent.identifierusager(nom,mdp)

    def creation_compte(self):
        self.parent.creation_compte(nom,mdp)
        
    def avertirusager(self,titre,message):
        rep=messagebox.askyesno(titre,message)
        if not rep:
            self.root.destroy()
            
    def centrerfenetre(self):
        w=self.root.winfo_width()
        h=self.root.winfo_height()
        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/3) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    ####

    def creation_compte(self):
        self.parent.creation_compte()

    def creer_cadre_creation(self):
        self.root.title("Creation")
        self.cadre_creation=Frame(self.cadreapp,width=800,height=400)

        self.list_entry=[]
        self.list_lab=[]

        self.signup_label=Label(self.cadre_creation,text="Création pour GestMedia",font=("Arial",18),
                              borderwidth=2,relief=GROOVE)

        self.signup_lab_pre=Label(self.cadre_creation,text="Prénom",font=("Arial",14))
        self.signup_pre=Entry(self.cadre_creation,font=("Arial",14),width=30)
        self.list_entry.append(self.signup_pre)
        self.list_lab.append(self.signup_lab_pre)

        self.signup_lab_nom=Label(self.cadre_creation,text="Nom",font=("Arial",14))
        self.signup_nom=Entry(self.cadre_creation,font=("Arial",14),width=30)
        self.list_entry.append(self.signup_nom)
        self.list_lab.append(self.signup_lab_nom)

        self.signup_lab_mail=Label(self.cadre_creation,text="Courriel",font=("Arial",14))

        self.list_entry.append(        (self.signup_mail=Entry(self.cadre_creation,font=("Arial",14),width=30)))
        self.list_lab.append(self.signup_lab_mail)

        self.signup_lab_tel=Label(self.cadre_creation,text="Télephone",font=("Arial",14))
        self.signup_tel=Entry(self.cadre_creation,font=("Arial",14),width=30)
        self.list_entry.append(self.signup_tel)
        self.list_lab.append(self.signup_lab_tel)
        
        self.signup_lab_mdp=Label(self.cadre_creation,text="Mot de Passe",font=("Arial",14))
        self.signup_mdp=Entry(self.cadre_creation,font=("Arial",14),show="*",width=30)
        self.list_entry.append(self.signup_mdp)
        self.list_lab.append(self.signup_lab_mdp)

        self.signup_lab_mdpval=Label(self.cadre_creation,text="Confirmation de mot de passe",font=("Arial",14))
        self.signup_mdpval=Entry(self.cadre_creation,font=("Arial",14),show="*",width=30)
        self.list_entry.append(self.signup_mdpval)
        self.list_lab.append(self.signup_lab_mdpval)

        self.signup_lab_nom_org=Label(self.cadre_creation,text="Nom organisation",font=("Arial",14))
        self.signup_nom_org=Entry(self.cadre_creation,font=("Arial",14),width=30)
        self.list_entry.append(self.signup_nom_org)
        self.list_lab.append(self.signup_lab_nom_org)

        self.signup_lab_type_org=Label(self.cadre_creation,text="Type d'organisation",font=("Arial",14))
        self.signup_type_org=Entry(self.cadre_creation,font=("Arial",14),width=30)
        self.list_entry.append(self.signup_type_org)
        self.list_lab.append(self.signup_lab_type_org)

        for i in range(len(self.list_entry)):
            temp = 10*(i+1)
            self.list_lab[i].grid(row=temp,column=10, sticky=E,padx=10,pady=5)
            self.list_entry[i].grid(row=temp,column=20,sticky=E,padx=5,pady=5)


        self.btn_annuler_signup=Button(self.cadre_creation,text="Annuler",font=("Arial",12),padx=10,pady=10,command=self.annuler_signup)
        self.btn_valider_signup=Button(self.cadre_creation,text="Valider",font=("Arial",12),padx=10,pady=10,command=self.valider_signup)

        self.btn_annuler_signup.grid(row=100,column=20,sticky=W,padx=10,pady=10)
        self.btn_valider_signup.grid(row=100,column=20,padx=10,pady=10)

        self.cadres["creation"]=self.cadre_creation

        return self.cadre_creation

    def annuler_signup(self):
        self.afficherlogin()

    def valider_signup(self):
        valide = True

        for i in self.list_entry:
            if not i.get():
                self.avertirusager("Invalide","Des champs sont vides, reprendre?")
                valide=False
                break

        if ((self.signup_mdp.get() != self.signup_mdpval.get()) and valide == True):
            valide=False
            self.avertirusager("Invalide","Mots de passe ne concordent pas, reprendre?")

        if valide == True:
            self.parent.signup_usager(nom,mdp)
            pass
#        
                
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
        self.vue.afficherlogin("jmd","jmd1")
        self.vue.root.mainloop()
    
    def telechargermodule(self,fichier):
        leurl=self.urlserveur+"/telechargermodule"
        params = {"fichier":fichier}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        fichier1=open("./SaaS_modules/"+fichier,"w")
        fichier1.write(rep)
        fichier1.close()
        usager=json.dumps([self.modele.nom,self.modele.compagnie])
        pid = Popen([sys.executable, "./SaaS_modules/"+fichier,self.urlserveur,usager],shell=1).pid 
                  
    def testsimple(self):
        leurl=self.urlserveur
        r=urllib.request.urlopen(leurl)
        rep=r.read()
        dict=rep.decode('utf-8')
        print("testserveurSIMPLE", dict)
    
    def trouvermodules(self): 
        url = self.urlserveur+"/trouvermodules"
        params = {}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        return mondict  
    
    def trouverprojets(self): 
        url = self.urlserveur+"/trouverprojets"
        params = {}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        return mondict
     
    def trouvermembres(self): 
        url = self.urlserveur+"/trouvermembres"
        params = {}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        return mondict
    
    def identifierusager(self,nom,mdp): 
        url = self.urlserveur+"/identifierusager"
        params = {"nom":nom,
                  "mdp":mdp}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        print(mondict)
        if "inconnu" in mondict:
            self.vue.avertirusager("Inconnu","Reprendre?")
        else:
            self.modele.inscrireusager(mondict)
            self.vue.creercadreprincipal(self.modele)
            self.vue.changercadre("principal")

####

    def creation_compte(self): 
        #url = self.urlserveur+"/identifierusager"
        
        self.vue.creer_cadre_creation()
        self.vue.changercadre("creation")

    def signup_usager(self,dict): 
        #url = self.urlserveur+"/identifierusager"
        params = {"nom":nom,
                  "mdp":mdp}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        print(mondict)
        if "inconnu" in mondict:
            self.vue.avertirusager("Inconnu","Reprendre?")
        else:
            self.modele.inscrireusager(mondict)
            self.vue.creercadreprincipal(self.modele)
            self.vue.changercadre("principal")

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
    print("FIN DE PROGRAMME")