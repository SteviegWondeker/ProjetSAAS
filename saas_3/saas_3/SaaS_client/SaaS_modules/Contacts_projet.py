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
        self.cadreapp=Frame(self.root)
        #self.canevas=Canvas(self.cadreapp,width=800,height=600)
        #self.canevas.create_text(400,300,anchor=CENTER,text="Bienvenue a SaaS PROJET")
        #self.canevas.pack()
        self.cadreapp.pack(expand=1, fill=BOTH)

        self.cadre_contacts=Frame(self.cadreapp)
        # Titre
        self.compagnie_label = Label(self.cadre_contacts, text="Nom de compagnie",font=("Arial",18),
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
        self.btn_new_contact = Button(self.contacts_details_frame, text="Ajouter un contact")
        self.btn_edit_contact = Button(self.contacts_details_frame, text="Éditer un contact")
        self.btn_new_contact.pack(padx=5, pady=5, anchor=NW)
        self.btn_edit_contact.pack(padx=5, pady=5, anchor=NW)
        self.details_label = LabelFrame(self.contacts_details_frame, text="Détails", font=("Arial", 12))
        self.text_temp = Label(self.details_label, text="Blablabla")
        self.text_temp.pack()
        self.details_label.pack(anchor=NW)

        # Packing des frames
        self.compagnie_label.pack()

        self.nom_module_label.grid(row=0, column=0)
        self.nom_projet_label.grid(row=0, column=1)
        self.entete.pack(fill=BOTH)

        self.tag_frame.pack(side=LEFT, anchor=N)
        self.recherche_frame.pack(side=RIGHT, anchor=N)
        self.tag_recherche_frame.pack(expand=1, fill=BOTH)

        self.tableau_frame.pack(side=LEFT, anchor=W)
        self.contacts_details_frame.pack(fill=BOTH, expand=1, side=RIGHT, anchor=NE)
        self.contacts_frame.pack(expand=1, fill=BOTH)

        self.cadre_contacts.pack(fill=BOTH, expand=1, padx=20, pady=20)

    def recherche_contacts(self):
        pass

    def afficher_details(self, evt):
        pass

class Controleur():
    def __init__(self):
        self.vue=Vue(self)
        self.vue.root.mainloop()

if __name__ == '__main__':
    c=Controleur()