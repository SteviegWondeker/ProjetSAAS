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
        self.selection=None
        self.creercadres()
        self.changercadre("Gestion")
        self.tbi_crée=FALSE
        self.data_infos=None


    

    def creertableau(self):
        f = Frame(self.cadre_gestion)
        f.pack(side=TOP, fill=BOTH, expand=Y)

        self.tableau = ttk.Treeview(show = 'headings')
        self.tableau['selectmode']="browse"
        self.tableau.bind("<ButtonRelease-1>",self.selectionner_projet)

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
    
    def selectionner_projet(self,evt):
        self.selection = self.tableau.item(self.tableau.focus(),'value')
        self.selection = self.selection[0]
    
    def ecriretableau(self):
        for i in self.tableau.get_children():
            self.tableau.delete(i)
        for item in self.data:
            if(item):
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
        if(self.selection!=None):
            self.changercadre("modifier_projet")
            self.data_infos=self.afficher_infos_projet(self.selection)
            for item in self.data_infos:
                if(item is None):
                    item=""
            
            self.modif_nom_projet.delete(0,END)
            if(self.data_infos[0][1] is not None):
                self.modif_nom_projet.insert(0,self.data_infos[0][1])
            self.modif_nom_client.delete(0,END)
            if(self.data_infos[0][2] is not None):
                self.modif_nom_client.insert(0,self.data_infos[0][2])
            self.modif_resp.delete(0,END)
            if(self.data_infos[0][3] is not None):
                self.modif_resp.insert(0,self.data_infos[0][3])
            self.modif_date_debut.delete(0,END)
            if(self.data_infos[0][4] is not None):
                self.modif_date_debut.insert(0,self.data_infos[0][4])
            self.modif_date_fin.delete(0,END)
            if(self.data_infos[0][5] is not None):
                self.modif_date_fin.insert(0,self.data_infos[0][5])
            self.modif_comp.delete(0,END)
            if(self.data_infos[0][6] is not None):
                self.modif_comp.insert(0,self.data_infos[0][6])
        else:
            show_method = getattr(messagebox, 'show{}'.format('warning'))
            show_method('ERREUR', 'Veuillez choisir un projet)')

    def confirmer_modification(self):
        self.form=[]
        self.form.append(self.data_infos[0][0])
        for i in self.list_modif_projet:
            self.form.append(i.get())
        print(self.form)
        self.parent.envoyer_modifs(self.form)
        self.cadres["Gestion"]=self.creer_cadre_gestion()
        self.tbi_crée=FALSE
        self.changercadre("Gestion")

    def retour_cadre_principal(self):
        # bla bla bla
        self.changercadre("Gestion")
        pass

    def creercadres(self):
        self.cadres["Gestion"]=self.creer_cadre_gestion()
        self.cadres["modifier_projet"]=self.creer_cadre_mp()
    
    def create_label(self, champ, cadre): #n
        label = Label(cadre, text=champ,font=("Arial",14))
        return label

    def create_entry(self, cadre): #n
        entry = Entry(cadre,font=("Arial",14),width=30)
        return entry

    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()
    
    
    def creer_tableau_infos(self):
        if(self.tbi_crée is FALSE):
            self.f = Frame(self.cadre_gestion)
            self.f.pack(fill=X)

        self.tableau_infos = ttk.Treeview(show = 'headings')
        
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tableau_infos.xview)
        self.tableau_infos['xscroll'] = xsb.set

        # add tableau_infos and scrollbars to frame
        self.tableau_infos.grid(in_=self.f, row=0, column=0, sticky=EW)
        
        xsb.grid(in_=self.f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        self.f.rowconfigure(0, weight=1)
        self.f.columnconfigure(0, weight=1)

        self.data_infos=self.afficher_infos_projet(self.selection)
        self.tableau_infos_cols = ["Id du projet","Nom du projet","Client","Responsable","Date de début","Date de fin","Compagnie"]

        self.tableau_infos.config(columns=self.tableau_infos_cols)
        n=1
        for i in self.tableau_infos_cols:
            no="#"+str(n)
            self.tableau_infos.heading(no, text=i)
            n+=1

        for i in self.tableau_infos.get_children():
            self.tableau_infos.delete(i)
        for item in self.data_infos:
            if(item):
                self.tableau_infos.insert('', 'end', values=item)

        self.tbi_crée=TRUE
    
    def choisirTriage(self):
         self.data_infos=self.afficher_infos_projet_avec_triage(self.selection,self.choixTriage)
        

    def creer_cadre_mp(self):
        self.root.title("modifier_projet")
        self.cadre_mp = Frame(self.cadreapp)

        self.list_modif_projet=[]
        self.list_lab_mp=[]
        self.params=[]

        self.modif_lab_nom_projet=self.create_label("Nom du projet", self.cadre_mp)
        self.modif_nom_projet=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_nom_projet)
        self.list_lab_mp.append(self.modif_lab_nom_projet)

        self.modif_lab_nom_client=self.create_label("Nom du Client", self.cadre_mp)
        self.modif_nom_client=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_nom_client)
        self.list_lab_mp.append(self.modif_lab_nom_client)

        self.modif_lab_resp=self.create_label("Responsable du projet", self.cadre_mp)
        self.modif_resp=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_resp)
        self.list_lab_mp.append(self.modif_lab_resp)
        
        self.modif_lab_date_debut=self.create_label("Date de début", self.cadre_mp)
        self.modif_date_debut=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_date_debut)
        self.list_lab_mp.append(self.modif_lab_date_debut)

        self.modif_lab_date_fin=self.create_label("Date de fin", self.cadre_mp)
        self.modif_date_fin=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_date_fin)
        self.list_lab_mp.append(self.modif_lab_date_fin)

        self.modif_lab_comp=self.create_label("Compagnie", self.cadre_mp)
        self.modif_comp=self.create_entry(self.cadre_mp)
        self.list_modif_projet.append(self.modif_comp)
        self.list_lab_mp.append(self.modif_lab_comp)

        for i in range(len(self.list_modif_projet)):
            temp = 10*(i+1)
            self.list_lab_mp[i].grid(row=temp,column=10, sticky=E,padx=10,pady=5)
            self.list_modif_projet[i].grid(row=temp,column=20,sticky=E,padx=5,pady=5)

        self.btn_annuler_signup=Button(self.cadre_mp,text="Annuler",font=("Arial",12),padx=10,pady=10,command=self.retour_cadre_principal)
        self.btn_valider_signup=Button(self.cadre_mp,text="Valider",font=("Arial",12),padx=10,pady=10,command=self.confirmer_modification)

        self.btn_annuler_signup.grid(row=100,column=20,sticky=W,padx=10,pady=10)
        self.btn_valider_signup.grid(row=100,column=20,padx=10,pady=10)

        return self.cadre_mp


    def creer_cadre_gestion(self,triage=None):
        self.root.title("Gestion")
        self.cadre_gestion = Frame(self.cadreapp)

        self.cblabel = Label(self.cadre_gestion,text="Trier selon :",font=('Times', 16))
        self.choixTriage=""
        self.cb=ttk.Combobox(self.cadre_gestion, textvariable=self.choixTriage, values=[
                                "Ordre alphabétique", 
                                "Date début",
                                "Date fin",
                                "Client",
                                "Responsable"])
        self.cblabel.pack()
        self.cb.pack()
        self.cb.bind('<<ComboboxSelected>>', self.choisirTriage)

        self.creertableau()
        if(triage==None):
            listeprojets=self.parent.trouverprojets()
        else:
            listeprojets=self.parent.trouverprojetsAvecTriage(triage)
        entete=["Nom du projet","date de début","date de fin"]
        self.integretableau(listeprojets,entete)

        self.btn_modifier_projet = Button(self.cadre_gestion,text="Modifier projet", font=("Arial", 12),
                                         padx=10, pady=10, command=self.form_modifier_projet)

        self.btn_supprimer_projet = Button(self.cadre_gestion,text="Supprimer projet", font=("Arial", 12),
                                         padx=20, pady=10, command=self.supprimer_projet)
        
        self.btn_afficher_infos = Button(self.cadre_gestion,text="Afficher Infos", font=("Arial", 12),
                                         padx=20, pady=10, command=self.creer_tableau_infos)

     
        


        self.btn_afficher_infos.pack()
        self.btn_modifier_projet.pack()
        self.btn_supprimer_projet.pack()

        return self.cadre_gestion

    def choisirTriage(self,event):
        self.cadres["Gestion"]=self.creer_cadre_gestion(self.cb.get())
        self.tbi_crée=FALSE
        self.changercadre("Gestion")

    def refresh(self):
        self.list_membre= self.list_nom_projet.get()
        self.listbox = Listbox(self.cadre_gestion, font=("Arial", 16), selectmode="multiple")
        
        self.listbox.grid (row=3, column=1, columnspan='10')

        self.listemodules=self.parent.trouvermembres("Cineclub")

        entete="modules disponibles"
        for items in self.listemodules:
            self.listbox.insert(END, items)

    def supprimer_projet(self):
        if(self.selection!=None):
            rep=messagebox.askyesno("Supression","Voulez-vous confirmer la supression du projet ?")
            if not rep:
                self.root.destroy()
            else:
                self.parent.envoyer_supression(self.selection)
                self.cadres["Gestion"]=self.creer_cadre_gestion()
                self.tbi_crée=FALSE
                self.changercadre("Gestion")
        else:
            show_method = getattr(messagebox, 'show{}'.format('warning'))
            show_method('ERREUR', 'Veuillez choisir un projet)')

    
    def afficher_infos_projet(self,projet):
        infos=self.parent.trouver_projet_infos(projet)
        return infos



class Modele():
    def __init__(self,parent):
        self.parent=parent
        print(sys.argv)
        self.usager=sys.argv[2].split()
        self.inscrireusager(self.usager)
        self.usager_compagnie=json.loads(sys.argv[2])[1]["nom"]
        self.usager_id=json.loads(sys.argv[2])[1]["id"]
        print(self.usager)
        print(self.usager_compagnie)
        print(self.usager_id)

        self.acces_modification_suppression = self.parent.trouver_permissions(self.usager)
        print(self.acces_modification_suppression)

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

    def envoyer_modifs(self,form): #n
        url = self.urlserveur+"/envoyer_modifs"
        params = {"idprojet":form[0],
                "nom_projet":form[1],
                "nom_client":form[2],
                "responsable":form[3],
                "date_deb":form[4],
                "date_fin":form[5],
                "nom_compagnie": form[6]}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)         
        print(mondict)

    def envoyer_supression(self,selection): #n
        url = self.urlserveur+"/envoyer_supression"
        params = {"nom_projet":selection}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)         
        print(mondict)


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
    
    def trouverprojets(self):
        url = self.urlserveur+"/trouverprojets"
        params = {}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict
    
    def trouver_permissions_par_membre(self,membre):
        url = self.urlserveur+"/trouver_permissions_par_membre"
        params = {"membre":membre}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

    def trouverprojetsAvecTriage(self,triage):
        url = self.urlserveur+"/trouverprojetsAvecTriage"
        params = {"triage":triage}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

    def trouver_projet_infos(self,projet):
        url = self.urlserveur+"/trouver_projet_infos"
        params = {"projet":projet}
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