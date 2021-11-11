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
        #self.cadres["nouveau_contact"]=self.creer_cadre_nouveau_contact()

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
        self.compagnie_label = Label(self.cadre_contacts, text=self.parent.modele.usager_compagnie["nom"],font=("Arial",18),    # ATTENTION!!! Usager n'est pas le même si on roule le module depuis le fichier client ou depuis VS Code
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
        self.tableau_frame = Frame(self.contacts_frame, width=500, height=300)
        self.tableau = Frame(self.tableau_frame)
        self.tableau = ttk.Treeview(show = 'headings')
        self.tableau.bind("<ButtonRelease-1>",self.afficher_details)
            # Remplissage tableau
        self.gerer_contacts_projet()

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
        self.btn_new_contact = Button(self.contacts_details_frame, text="Ajouter un contact", command= self.ajouter_contact)
        self.btn_edit_contact = Button(self.contacts_details_frame, text="Éditer un contact")
        self.btn_new_contact.pack(anchor=NW, padx=5, pady=5)
        self.btn_edit_contact.pack(anchor=NW, padx=5, pady=5)
        self.details_txt = StringVar()
        self.details_txt.set("")
        self.details_label = LabelFrame(self.contacts_details_frame, font=("Arial", 12))
        self.text_box = Label(self.details_label, textvariable=self.details_txt)
        self.text_box.pack()
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

    def gerer_contacts_projet(self):
        liste_contacts=self.parent.trouver_contacts_par_projet()
        print("ID COMPAGNIE ID COMPAGNIE")
        print(self.parent.modele.usager_compagnie["id"])
        entete=["Prénom","Nom","Expertise", "Courriel", "Ville", "Adresse", "Téléphone", "Notes", "Détails"]
        self.integretableau(liste_contacts,entete)
        for i in range(len(entete)):
            self.tableau.column('#' + str(i), width=50, stretch=0)

    def integretableau(self,liste_contacts,entete):
        self.data=liste_contacts
        self.colonnestableau = entete

        self.tableau.config(columns=self.colonnestableau)
        n=1
        for i in self.colonnestableau:
            no="#"+str(n)
            self.tableau.heading(no, text=i)
            n+=1

        self.ecriretableau()

    def ecriretableau(self):
        for i in self.tableau.get_children():
            self.tableau.delete(i)
        for item in self.data:
            self.tableau.insert('', 'end', values=item)

    def creer_cadre_nouveau_contact(self):
        self.cadre_inscrire_contact = Frame(self.cadreapp, width=800, height=400)

        self.contact_titre = Label(self.cadre_inscrire_contact, text="Ajout d'un nouveau contact à votre projet", font=("Arial", 18),
                                borderwidth=2, relief=GROOVE)

        self.list_entry_contact = []

        self.list_tags=self.parent.retourner_expertises()
        self.list_tags.append("Ajouter un tag")

        #self.combobox_role = ttk.Combobox(self.cadre_role, values=self.list_role)

        self.contact_lab_prenom = Label(self.cadre_inscrire_contact, text="Prénom:", font=("Arial", 14))
        self.contact_prenom = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_nom = Label(self.cadre_inscrire_contact, text="Nom:", font=("Arial", 14))
        self.contact_nom = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_tags = Label(self.cadre_inscrire_contact, text="Expertise:", font=("Arial", 14))
        self.contact_ajout_tag = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=20)

#        self.membre_role = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)

        self.value_inside = StringVar(self.cadre_inscrire_contact)
        #self.value_inside.set("Option")
        self.contact_tags = ttk.OptionMenu(self.cadre_inscrire_contact, self.value_inside, "Choisir une option", *self.list_tags, command=self.selection_tag)
        #ttk.Combobox(self.cadre_inscrire_contact, values=self.list_tags)

        self.contact_lab_courriel = Label(self.cadre_inscrire_contact, text="Courriel:", font=("Arial", 14))
        self.contact_courriel = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_ville = Label(self.cadre_inscrire_contact, text="Ville:", font=("Arial", 14))
        self.contact_ville = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_adresse = Label(self.cadre_inscrire_contact, text="Adresse:", font=("Arial", 14))
        self.contact_adresse = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_telephone = Label(self.cadre_inscrire_contact, text="Téléphone:", font=("Arial", 14))
        self.contact_telephone = Entry(self.cadre_inscrire_contact, font=("Arial", 14), width=30)
        self.contact_lab_details = Label(self.cadre_inscrire_contact, text="Détails:", font=("Arial", 14))
        self.contact_details = Text(self.cadre_inscrire_contact, font=("Arial", 14), width=30, height=5)
        self.contact_lab_note = Label(self.cadre_inscrire_contact, text="Notes importantes:", font=("Arial", 14))
        self.contact_note = Text(self.cadre_inscrire_contact, font=("Arial", 14), width=30, height=2)

                
        """ self.list_entry_contact.append(self.contact_prenom)
        self.list_entry_contact.append(self.contact_nom)
        self.list_entry_contact.append(self.contact_courriel)
        self.list_entry_contact.append(self.contact_ville)
        self.list_entry_contact.append(self.contact_adresse)
        self.list_entry_contact.append(self.contact_telephone)
        self.list_entry_contact.append(self.contact_details)
        self.list_entry_contact.append(self.contact_note) """

        self.btn_inscrire_contact = Button(self.cadre_inscrire_contact, text="Inscrire le nouveau contact", font=("Arial", 12), padx=10, pady=10,
                                      command=self.inscrire_contact)

        self.btn_annuler = Button(self.cadre_inscrire_contact, text="Annuler", font=("Arial", 12), padx=10, pady=10,
                                command=self.retour_cadre_principal)

        self.contact_titre.grid(row=10, column=10, columnspan=20, padx=10, pady=10, ipadx=10, ipady=10)
        self.contact_lab_prenom.grid(row=20, column=10, sticky=E, padx=5, pady=5)
        self.contact_prenom.grid(row=20, column=20, padx=10, pady=5)
        self.contact_lab_nom.grid(row=30, column=10, sticky=E, padx=5, pady=5)
        self.contact_nom.grid(row=30, column=20, padx=10, pady=5)
        self.contact_lab_tags.grid(row=40, column=10, sticky=E, padx=5, pady=5)
        self.contact_tags.grid(row=40, column=20, padx=10, pady=5)
        self.contact_lab_courriel.grid(row=50, column=10, sticky=E, padx=5, pady=5)
        self.contact_courriel.grid(row=50, column=20, padx=10, pady=5)
        self.contact_lab_ville.grid(row=60, column=10, sticky=E, padx=5, pady=5)
        self.contact_ville.grid(row=60, column=20, padx=10, pady=5)
        self.contact_lab_adresse.grid(row=70, column=10, sticky=E, padx=5, pady=5)
        self.contact_adresse.grid(row=70, column=20, padx=10, pady=5)
        self.contact_lab_telephone.grid(row=80, column=10, sticky=E, padx=5, pady=5)
        self.contact_telephone.grid(row=80, column=20, padx=10, pady=5)
        self.contact_lab_details.grid(row=90, column=10, sticky=NE, padx=5, pady=5)
        self.contact_details.grid(row=90, column=20, padx=10, pady=5)
        self.contact_lab_note.grid(row=100, column=10, sticky=NE, padx=5, pady=5)
        self.contact_note.grid(row=100, column=20, padx=10, pady=5)

        self.btn_inscrire_contact.grid(row=110, column=20, sticky=E, padx=10, pady=10)

        self.btn_annuler.grid(row=110, column=10, sticky=E, padx=10, pady=10)

        return self.cadre_inscrire_contact

    def selection_tag(self, evt):
        if self.value_inside.get() == "Ajouter un tag":
            self.contact_tags.grid(row=40, column=20, sticky=W, padx=10, pady=5)
            self.contact_ajout_tag.grid(row=40, column=20, sticky=E, padx=10, pady=5)

        else:
            self.contact_tags.grid(row=40, column=20, padx=10, pady=5)
            self.contact_ajout_tag.forget()

    def inscrire_contact(self):
        self.valider_contact()
        self.changercadre("principal")

    def valider_contact(self): #n
        form_valide = True

        self.form=[]

        self.form.append(self.contact_prenom.get())
        self.form.append(self.contact_nom.get())
        self.form.append(self.contact_courriel.get())
        self.form.append(self.contact_ville.get())
        self.form.append(self.contact_adresse.get())
        self.form.append(self.contact_telephone.get())
        self.form.append(self.contact_details.get("1.0",END))
        self.form.append(self.contact_note.get("1.0",END))
        if self.value_inside.get() == "Choisir une option":  # Aucune option sélectionnée
            self.form.append("")
        elif self.value_inside.get() == "Ajouter un tag":
            if self.contact_ajout_tag.get() == "":        # Champ vide
                self.form.append("")
            else:
                self.form.append(self.contact_ajout_tag.get())  # Ajout d'un NOUVEAU tag
        else:
            self.tag = self.value_inside.get()
            self.tag = self.tag.replace("(", "")
            self.tag = self.tag.replace(")", "")
            self.tag = self.tag.replace("\'", "")
            self.tag = self.tag.replace(",", "")
            self.form.append(self.tag)       # Ajout d'un tag existant

        if form_valide == True:
            self.parent.inscrire_contact(self.form)

    def retour_cadre_principal(self):
        self.changercadre("principal")

    def ajouter_contact(self):
        self.changercadre("nouveau_contact")

    def recherche_contacts(self):
        pass

    def afficher_details(self, evt):
        curItem = self.tableau.focus()
        self.details_txt.set(self.tableau.item(curItem)["values"][8])
        pass

    def avertirusager(self,titre,message):
        rep=messagebox.askyesno(titre,message)
        if not rep:
            self.root.destroy()

class Modele():
    def __init__(self,parent):
        self.parent=parent
        if len(sys.argv) > 1:
            #self.usager=sys.argv[2].split()
            self.usager=json.loads(sys.argv[2])[0]
            self.usager_compagnie=json.loads(sys.argv[2])[1]
            print("USAGER USAGER USAGER")
            print(self.usager)
            print(self.usager_compagnie["nom"])
            #self.usager = [s.strip("[],\"") for s in self.usager]
        else:
            self.data_temp = ['jmd', '{"nom": Cineclub', 'id:1}']
            self.usager="jmd"
            self.usager_compagnie={}
            self.usager_compagnie["nom"] = "Cinéclub"
            self.usager_compagnie["id"] = 1

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

    def retourner_expertises(self):
        url = self.urlserveur+"/trouver_expertises"
        params = {}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)         
        return (mondict)

    def trouver_contacts_par_projet(self):
        url = self.urlserveur+"/trouver_contacts_par_projet"
        params = {"comp": self.modele.usager_compagnie["id"]}
        reptext=self.appelserveur(url, params)

        mondict=json.loads(reptext)
        return mondict

    def inscrire_contact(self,form):        # On va devoir éventuellement ajouter l'ID du projet!
        url = self.urlserveur+"/inscrire_contact"
        identifiant_nom = form[0]+" "+form[1]
        params = {"prenom":form[0],
                    "nom":form[1],
                  "courriel":form[2],
                    "ville":form[3],
                    "adresse":form[4],
                  "telephone":form[5],
                  "details":form[6],
                  "notes":form[7],
                  "tag":form[8],
                  "comp":self.modele.usager_compagnie["id"],
                  "projet":1}
        print(params)
        pass
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