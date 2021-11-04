## -*- Encoding: UTF-8 -*-
import urllib.request
import urllib.parse 
import json 

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk

import sys

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.root.minsize(width=600, height=400)
        self.cadreapp=Frame(self.root)
        self.cadreapp.pack(expand=1, fill=BOTH)
        self.cadres={}
        self.cadreactif=None
        self.creercadres()
        self.changercadre("principal")


    def creercadres(self):
        self.cadres["principal"]=self.creercadreprincipal(self.parent.modele.usager)
        self.cadres["nouveau_contact"]=self.creer_cadre_nouveau_contact()

    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()


    def creercadreprincipal(self, usager):
        self.usager=usager
        print(self.usager)
        self.cadre_contacts=Frame(self.cadreapp)
        # Titre
        self.compagnie_label = Label(self.cadre_contacts, text=self.usager[2],font=("Arial",18),    # ATTENTION!!! Usager n'est pas le même si on roule le module depuis le fichier client ou depuis VS Code
                              borderwidth=2, relief=GROOVE)

        # Frame d'entête -> Contacts - Nom du projet
        self.entete = Frame(self.cadre_contacts)
        self.nom_module_label = Label(self.entete, text="Contact - ",font=("Arial",18),
                              borderwidth=2)
        self.nom_projet_label = Label(self.entete, text="Nom du Projet",font=("Arial",16),
                              borderwidth=2)

        self.tag_recherche_frame = Frame(self.cadre_contacts)
        # Section Tags
        self.tag_frame = LabelFrame(self.tag_recherche_frame, text="Tags", font=("Arial", 16))
        self.tag1 = Checkbutton(self.tag_frame, text="Tag1")
        self.tag2 = Checkbutton(self.tag_frame, text="Tag2")
        self.tag3 = Checkbutton(self.tag_frame, text="Tag3")
        self.tag4 = Checkbutton(self.tag_frame, text="Tag4")
        self.tag5 = Checkbutton(self.tag_frame, text="Tag5")
        self.tag6 = Checkbutton(self.tag_frame, text="Tag6")
        self.ajout_tag_btn = Button(self.tag_frame, text="Ajouter un tag")
        
        self.tag1.grid(row=0, column=0)
        self.tag2.grid(row=0, column=1)
        self.tag3.grid(row=0, column=2)
        self.tag4.grid(row=1, column=0)
        self.tag5.grid(row=1, column=1)
        self.tag6.grid(row=1, column=2)
        self.ajout_tag_btn.grid(row=2, column=0)

        # Section Recherche
        self.recherche_frame = LabelFrame(self.tag_recherche_frame, text="Recherche", font=("Arial", 16))
        self.search_box = Entry(self.recherche_frame, width=15, font=("Arial", 14))
        self.btn_search = Button(self.recherche_frame, text="Rechercher", command=self.recherche_contacts)

        self.search_box.pack(padx=20)
        self.btn_search.pack(padx=20, pady = 10, anchor=E)

        # Section Contacts
        self.contacts_frame = Frame(self.cadre_contacts)
            # Tableau Contacts
        self.tableau_frame = Frame(self.contacts_frame)
        self.tableau = Frame(self.tableau_frame)
        self.tableau = ttk.Treeview(show = 'headings')
        self.tableau.bind("<Button-1>",self.afficher_details)

        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tableau.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tableau.xview)
        self.tableau['yscroll'] = ysb.set
        self.tableau['xscroll'] = xsb.set

        self.tableau.grid(in_=self.tableau_frame, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=self.tableau_frame, row=0, column=1, sticky=NS)
        xsb.grid(in_=self.tableau_frame, row=1, column=0, sticky=EW)

        self.tableau.rowconfigure(0, weight=1)
        self.tableau.columnconfigure(0, weight=1)

            # Frame Contacts détails
        self.contacts_details_frame = Frame(self.contacts_frame)
        self.btn_new_contact = Button(self.contacts_details_frame, text="Ajouter un contact", command= self.inscrire_contact)
        self.btn_edit_contact = Button(self.contacts_details_frame, text="Éditer un contact")
        self.btn_new_contact.pack(anchor=NW, padx=5, pady=5)
        self.btn_edit_contact.pack(anchor=NW, padx=5, pady=5)
        self.details_label = LabelFrame(self.contacts_details_frame, text="Détails", font=("Arial", 12))
        self.text_temp = Label(self.details_label, text="Blablabla")
        self.text_temp.pack()
        self.details_label.pack(anchor=NW, padx=5, pady=5)

        # Packing des frames
        self.compagnie_label.pack()

        self.nom_module_label.grid(row=0, column=0)
        self.nom_projet_label.grid(row=0, column=1)
        self.entete.pack(fill=BOTH)

        self.tag_frame.pack(side=LEFT, anchor=N)
        self.recherche_frame.pack(side=RIGHT, anchor=N)
        self.tag_recherche_frame.pack(expand=1, fill=BOTH)

        self.tableau_frame.pack(side=LEFT, anchor=N)
        self.contacts_details_frame.pack(side=LEFT, anchor=N)
        self.contacts_frame.pack(expand=1, fill=BOTH)

        self.cadre_contacts.pack(fill=BOTH, expand=1, padx=20, pady=20)

        return self.cadre_contacts

    def creer_cadre_nouveau_contact(self):
        self.cadre_inscrire_contact = Frame(self.cadreapp, width=800, height=400)

        self.contact_titre = Label(self.cadre_inscrire_contact, text="Ajout d'un nouveau membre à votre compagnie", font=("Arial", 18),
                                borderwidth=2, relief=GROOVE)

        self.list_entry_contact = []


        self.list_role=self.parent.retourner_roles_nom()

        #self.combobox_role = ttk.Combobox(self.cadre_role, values=self.list_role)

        self.contact_lab_prenom = Label(self.cadre_inscrire_contact, text="Prénom:", font=("Arial", 14))
        self.contact_prenom = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_nom = Label(self.cadre_inscrire_contact, text="Nom:", font=("Arial", 14))
        self.contact_nom = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_role = Label(self.cadre_inscrire_contact, text="Rôle:", font=("Arial", 14))

#        self.membre_role = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)

        self.contact_role = ttk.Combobox(self.cadre_inscrire_contact, values=self.list_role)

        self.contact_lab_id = Label(self.cadre_inscrire_contact, text="#ID d'employé:", font=("Arial", 14))
        self.contact_id = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_courriel = Label(self.cadre_inscrire_contact, text="Courriel:", font=("Arial", 14))
        self.contact_courriel = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_telephone = Label(self.cadre_inscrire_contact, text="# téléphone:", font=("Arial", 14))
        self.contact_telephone = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_mdp = Label(self.cadre_inscrire_contact, text="Mot de passe (par défaut):", font=("Arial", 14))
        self.contact_mdp = Label(self.cadre_inscrire_contact, text="AAAaaa111", font=("Arial", 14), width=30)

                
        self.list_entry_contact.append(self.contact_prenom)
        self.list_entry_contact.append(self.contact_nom)
        self.list_entry_contact.append(self.contact_id)
        self.list_entry_contact.append(self.contact_courriel)
        self.list_entry_contact.append(self.contact_telephone)
        self.list_entry_contact.append(self.contact_mdp)

        self.btn_inscrire_contact = Button(self.cadre_inscrire_contact, text="Inscrire le nouveau contact", font=("Arial", 12), padx=10, pady=10,
                                      command=self.inscrire_contact)

        self.btn_annuler = Button(self.cadre_inscrire_contact, text="Annuler", font=("Arial", 12), padx=10, pady=10,
                                command=self.retour_cadre_principal)

        self.contact_titre.grid(row=10, column=10, columnspan=20, padx=10, pady=10, ipadx=10, ipady=10)
        self.contact_lab_prenom.grid(row=20, column=10, sticky=E, padx=5, pady=5)
        self.contact_prenom.grid(row=20, column=20, padx=10, pady=5)
        self.contact_lab_nom.grid(row=30, column=10, sticky=E, padx=5, pady=5)
        self.contact_nom.grid(row=30, column=20, padx=10, pady=5)
        self.contact_lab_role.grid(row=40, column=10, sticky=E, padx=5, pady=5)
        self.contact_role.grid(row=40, column=20, padx=10, pady=5)
        self.contact_lab_id.grid(row=50, column=10, sticky=E, padx=5, pady=5)
        self.contact_id.grid(row=50, column=20, padx=10, pady=5)
        self.contact_lab_courriel.grid(row=60, column=10, sticky=E, padx=5, pady=5)
        self.contact_courriel.grid(row=60, column=20, padx=10, pady=5)
        self.contact_lab_telephone.grid(row=70, column=10, sticky=E, padx=5, pady=5)
        self.contact_telephone.grid(row=70, column=20, padx=10, pady=5)
        self.contact_lab_mdp.grid(row=80, column=10, sticky=E, padx=5, pady=5)
        self.contact_mdp.grid(row=80, column=20, padx=10, pady=5)

        self.btn_inscrire_contact.grid(row=100, column=20, sticky=E, padx=10, pady=10)

        self.btn_annuler.grid(row=100, column=10, sticky=E, padx=10, pady=10)

        return self.cadre_inscrire_contact

    def valider_contact(self):
        form_valide = True

        self.form=[]

        for i in self.list_entry_contact:
            if not i.get():
                self.avertirusager("Invalide","Des champs sont vides, reprendre?")
                form_valide=False
                break
            else:
                self.form.append(i.get())

        if form_valide == True:
            if not self.parent.verifier_contact(self.form):
                self.parent.inscrire_contact(self.form)

    def inscrire_contact(self):
        self.valider_contact()
        self.changercadre("principal")

    def retour_cadre_principal(self):
        self.changercadre("principal")

    def recherche_contacts(self):
        pass

    def afficher_details(self, evt):
        pass

class Modele():
    def __init__(self,parent):
        self.parent=parent
        if len(sys.argv) > 1:
            self.usager=sys.argv[2].split()
            self.usager = [s.strip("[],\"") for s in self.usager]
        else:
            self.usager = ["jmd", "Cineclub", "1"]
        print(self.usager)

class Controleur():
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url, data)
        reptext=rep.read()
        return reptext

    def retourner_roles_nom(self):
        url = self.urlserveur+"/trouver_roles_nom"
        params = {}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)         
        return (mondict)

    def inscrire_contact(self,form):
        url = self.urlserveur+"/inscrirecontact"
        identifiant_nom = form[0]+" "+form[1]
        identifiant_id = form[1]+form[3]
        params = {"nom_user":identifiant_nom,
                    "nom_role": form[2],
                    "id_complet":identifiant_id,
                    "id":form[3],
                  "courriel":form[4],
                  "telephone":form[5],
                  "mdp":"AAAaaa111",
                  "nom_admin":self.vue.loginnom.get()}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        print(mondict)

    def verifier_contact(self,form):
        url = self.urlserveur+"/verifiercontact"
        params = {"courriel":form[4]}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        if len(mondict)>0:
            self.vue.avertirusager("Compte existe déjà","Reprendre?")
            return True
        else:
            return False

if __name__ == '__main__':
    c=Controleur()