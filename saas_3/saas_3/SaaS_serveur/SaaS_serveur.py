#import flask
from flask import Flask,request,json
from werkzeug.wrappers import Response
import os
# pour retrouver le dossier courant d'execution
import sys

import sqlite3

app = Flask(__name__)

app.secret_key="qwerasdf1234"

class Dbclient():   # Base de données du locateur
    def __init__(self):
        nomdb=os.getcwd()+"/SaaS_clients/"+"InkInc_client.sqlite"
        self.conn = sqlite3.connect(nomdb)
        self.curs = self.conn.cursor()

    def ajouter_projet_fournisseur(self,nom_projet, nom_client, responsable, date_deb, date_fin, nom_compagnie):
        sql_nom=("insert into 'projet' ('Nomdeprojet', 'client', 'chargedeprojet', 'datedelancement', 'datedefinprevue', 'compagnie') values (:nom_projet, :nom_client, :responsable, :date_deb, :date_fin, :nom_compagnie)")                         
                              
        self.curs.execute(sql_nom, {
                                'nom_projet':nom_projet,
                                'nom_client': nom_client,
                                'responsable': responsable,
                                'date_deb': date_deb,
                                'date_fin': date_fin,
                                'nom_compagnie':nom_compagnie})          

        self.conn.commit() 
        self.conn.commit()
        return "test"

    def trouverprojets(self):
        sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info
    
    def trouverprojetsAvecTriage(self,triage):
        print("banana")
        if(triage=="Ordre alphabétique"):
            sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' ORDER BY NomdeProjet")
        elif(triage=="Date début"):
            sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' ORDER BY datedelancement")
        elif(triage=="Date fin"):
            sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' ORDER BY datedefinprevue")
        elif(triage=="Responsable"):
            sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' ORDER BY chargedeprojet")
        elif(triage=="Client"):
            sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' ORDER BY client")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info
    
    def trouver_projet_infos(self,nom_projet):
        sqlnom=("select idprojet, Nomdeprojet, client, chargedeprojet, datedelancement, datedefinprevue, compagnie from 'projet' WHERE Nomdeprojet=:nom_projet")
        self.curs.execute(sqlnom, {'nom_projet': nom_projet})
        
        info=self.curs.fetchall()
        return info

    
    def trouverclients(self):
        sqlnom=("select compagnie, nom, courriel from 'client'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def trouver_projets_par_compagnie(self, comp):        # Alex
        print(comp)
        sqlnom = ("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' WHERE compagnie=:comp")
        self.curs.execute(sqlnom, {'comp': comp})
        info = self.curs.fetchall()
        return info

    def fermerdb(self):
        self.conn.close()

    def verifier_projet(self,nom_projet, nom_client): #n 
        sql_proj=("select * from 'projet' where Nomdeprojet=:nom_projet")
        self.curs.execute(sql_proj, {'nom_projet': nom_projet})

        info_projet=self.curs.fetchall()

        sql_client=("select * from 'client' where nom=:nom_client")
        self.curs.execute(sql_client, {'nom_client':nom_client})

        info_client=self.curs.fetchall()

        return [info_projet,info_client]

    def verifier_client(self,courriel): #n 
        sql_client=("select * from 'client' where courriel=:courriel")
        self.curs.execute(sql_client, {'courriel':courriel})

        info=self.curs.fetchall()

        return info

    def trouver_projet_par_compagnie(self):
        sqlnom=("select Nomdeprojet from 'projet' where")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def inscrire_client(self, nom_client, courriel, telephone, compagnie, adresse, rue, ville):
        sql_client=("insert into 'client' ('nom', 'courriel', 'tel', 'compagnie', 'adresse', 'rue', 'ville') values (:nom_client, :courriel, :telephone, :compagnie, :adresse, :rue, :ville)")                         
        self.curs.execute(sql_client, {
                                    'nom_client':nom_client,
                                    'courriel': courriel,
                                    'telephone': telephone,
                                    'compagnie': compagnie,
                                    'adresse': adresse,
                                    'rue': rue,
                                    'ville': ville})                       
        self.conn.commit()
        return "test"


    def ajouter_projet(self,nom_projet, nom_client, responsable, date_deb, date_fin, nom_compagnie):
        sql_nom=("insert into 'projet' ('Nomdeprojet', 'client', 'chargedeprojet', 'datedelancement', 'datedefinprevue', 'compagnie') values (:nom_projet, (select idclient from client where nom=:nom_client), :responsable, :date_deb, :date_fin, :nom_compagnie)")                         
                              
        self.curs.execute(sql_nom, {
                                'nom_projet':nom_projet,
                                'nom_client': nom_client,
                                'responsable': responsable,
                                'date_deb': date_deb,
                                'date_fin': date_fin,
                                'nom_compagnie':nom_compagnie})          

        self.conn.commit()                                
        #sql_projet("insert into 'tbl_projet_compagnie' ('nom_compagnie', 'id') values ((select compagnie from 'membre' where identifiant=:nom_admin), (select idprojet from 'projet' where nomdeprojet=:nom_projet))")
        #self.curs.execute(sql_projet, {
        #                        'nom_admin':nom_admin,
        #                        'nom_projet': nom_projet})     
        self.conn.commit()
        return "test"
    
    def envoyer_modifs(self,idprojet,nom_projet, nom_client, responsable, date_deb, date_fin, nom_compagnie): 
        sql_nom=("update 'projet' set 'Nomdeprojet'=:nom_projet, 'client'=(select idclient from client where nom=:nom_client), 'chargedeprojet'=:responsable, 'datedelancement'=:date_deb, 'datedefinprevue'=:date_fin, 'compagnie'=:nom_compagnie where idprojet=:idprojet")               
        self.curs.execute(sql_nom, {
                                'idprojet': idprojet,
                                'nom_projet': nom_projet,
                                'nom_client': nom_client,
                                'responsable': responsable,
                                'date_deb': date_deb,
                                'date_fin': date_fin,
                                'nom_compagnie':nom_compagnie})          

        self.conn.commit()                                
        #sql_projet("insert into 'tbl_projet_compagnie' ('nom_compagnie', 'id') values ((select compagnie from 'membre' where identifiant=:nom_admin), (select idprojet from 'projet' where nomdeprojet=:nom_projet))")
        #self.curs.execute(sql_projet, {
        #                        'nom_admin':nom_admin,
        #                        'nom_projet': nom_projet})     
        self.conn.commit()
        return "test"

    def envoyer_supression(self,nom_projet): 
        sql_nom=("DELETE from projet where Nomdeprojet=:nom_projet")               
        self.curs.execute(sql_nom, {'nom_projet': nom_projet})          
        self.conn.commit()                                
        return "test"

    def inscrire_contact(self, prenom, nom, courriel, ville, adresse, telephone, details, notes, tag, comp, projet):
        if tag != "":
            sql_tag_id = ("select idexpertise from 'contacts_expertises' where expertise = :tag")
            self.curs.execute(sql_tag_id, {'tag': tag})
            tag_id=self.curs.fetchall()
            print("TAG ID 1")
            print(tag_id)
            if not tag_id:
                sql_tag_insert = ("insert into 'contacts_expertises' ('expertise') values (:tag)")
                self.curs.execute(sql_tag_insert, {'tag': tag})
                self.conn.commit()
            self.curs.execute(sql_tag_id, {'tag': tag})
            
            tag_id=self.curs.fetchall()[0][0]
        else:
            tag_id = ""
        sql_nom=("insert into 'contacts_projets' ('prenom', 'nom', 'courriel', 'ville', 'adresse', 'telephone', 'details', 'notes', 'expertise', 'compagnie', 'projet') values (:prenom, :nom, :courriel, :ville, :adresse, :telephone, :details, :notes, :tag_id, :comp, :projet)")
        self.curs.execute(sql_nom, {
                                'prenom':prenom,
                                'nom': nom,
                                'courriel': courriel,
                                'ville': ville,
                                'adresse': adresse,
                                'telephone':telephone,
                                'details':details,
                                'notes':notes,
                                'tag_id':tag_id,
                                'comp':comp,
                                'projet':projet})

        self.conn.commit()  

    
    def inscrire_taches(self, nom_tache, details, notes, employe, comp, courriel, projet,tag):
        print(tag)
        if tag != "":
            sql_tag_id = ("select idexpertise from 'contacts_expertises' where expertise = :tag")
            self.curs.execute(sql_tag_id, {'tag': tag})
            tag_id=self.curs.fetchall()
            print("TAG ID 1")
            print(tag_id)
            if not tag_id:
                sql_tag_insert = ("insert into 'contacts_expertises' ('expertise') values (:tag)")
                self.curs.execute(sql_tag_insert, {'tag': tag})
                self.conn.commit()
            self.curs.execute(sql_tag_id, {'tag': tag})
            
            tag_id=self.curs.fetchall()[0][0]
        else:
            tag_id = ""
        sql_nom=("insert into 'tache' ('nom_tache','details','notes','employe','comp','courriel','projet','role') values (:nom_tache,:details,:notes,:employe,:compagnie,:courriel,:projet,:role)")
        self.curs.execute(sql_nom, {
                                'nom_tache':nom_tache,
                                'details':details,
                                'notes':notes,
                                'employe':employe,
                                'comp':comp,
                                'courriel': courriel,
                                'projet':projet,
                                'role':tag
                                # 'tag_id':tag                 
                                })

        self.conn.commit()      

    def trouver_expertises(self):
        sql_expertises = ("select expertise from 'contacts_expertises'")
        self.curs.execute(sql_expertises)
        info = self.curs.fetchall()
        return info

    def trouver_contacts_par_projet(self, comp):        # Alex
        # Va devoir ajouter le critère "compagnie"
        sqlnom = ("select prenom, nom, contacts_expertises.expertise from 'contacts_projets' INNER JOIN 'contacts_expertises' ON contacts_projets.expertise=contacts_expertises.idexpertise")  #, courriel, ville, adresse, telephone, notes, details
        #self.curs.execute(sqlnom, {'comp': comp})
        self.curs.execute(sqlnom)
        info = self.curs.fetchall()
        return info

    def get_contact_details(self, prenom, nom, expertise):        # Alex
        sqldetails = ("select prenom, nom, contacts_expertises.expertise, courriel, ville, adresse, telephone, notes, details, idcontacts from 'contacts_projets' INNER JOIN 'contacts_expertises' ON contacts_projets.expertise=contacts_expertises.idexpertise WHERE prenom = :prenom AND nom = :nom AND contacts_expertises.expertise = :expertise")
        self.curs.execute(sqldetails, {'prenom': prenom, "nom": nom, "expertise": expertise})
        info = self.curs.fetchall()
        print(info)
        return info

    def supprimer_contact(self, idcontacts):
        sqlrequete = ("DELETE FROM 'contacts_projets' WHERE idcontacts = :idcontacts;")
        self.curs.execute(sqlrequete, {'idcontacts': idcontacts})
        self.conn.commit() 

    def ajouter_role():
        pass

class Dbman():  # DB Manager - Base donnée du fournisseur
    def __init__(self):
        self.conn = sqlite3.connect("CVMJMD_clientscorpo.sqlite")
        self.curs = self.conn.cursor()

    def identifierusager(self,nom,mdp):
        sqlnom=("select * from 'membre' where identifiant=:qui and mdp=:secret")
        self.curs.execute(sqlnom, {'qui': nom, 'secret': mdp})
        info=self.curs.fetchall()

        if info:
            sqlnom=("select nomcompagnie from 'compagnie' where idcompagnie=:qui")
            self.curs.execute(sqlnom, {'qui': info[0][1]})
            co=self.curs.fetchall()
            return [info,co]
        return "inconnu"


    def trouvermembres(self):
        sqlnom=("select identifiant, permission,titre from 'membre'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def trouver_membres_par_compagnie(self, comp):        # Alex
        sqlnom = ("select identifiant, permission,titre from 'membre' INNER JOIN 'compagnie' ON membre.compagnie=compagnie.idcompagnie WHERE compagnie.nomcompagnie=:comp")
        self.curs.execute(sqlnom, {'comp': comp})
        info = self.curs.fetchall()
        return info

    def trouver_permissions_par_membre(self, membre):        # Alex
        sqlnom = ("select nommodule from 'modules' INNER JOIN 'Tbl_role_module' ON modules.idmodule=Tbl_role_module.module INNER JOIN 'Tbl_role' ON Tbl_role_module.role=Tbl_role.id_role INNER JOIN 'Tbl_membre_role' ON Tbl_role.id_role=Tbl_membre_role.role INNER JOIN 'membre' ON Tbl_membre_role.membre=membre.idmembre WHERE membre.identifiant=:membre")
        self.curs.execute(sqlnom, {'membre': membre})
        info = self.curs.fetchall()
        print(membre)
        print("testtestest")
        return info

    def trouver_compagnies(self):           # Alex
        sqlnom=("select nomcompagnie from 'compagnie'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def trouver_compagnie_id(self, comp):
        sqlnom=("select idcompagnie from 'compagnie' where nomcompagnie = :comp")
        self.curs.execute(sqlnom, {'comp': comp})
        info = self.curs.fetchall()
        return info
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
    def trouver_transactions_par_compagnie(self, comp):        # Alex
        print(comp)
        sqlnom = ("select Nomdeprojet, datedelancement, datedefinprevue from 'projet' WHERE compagnie=:comp")
        self.curs.execute(sqlnom, {'comp': comp})
        info = self.curs.fetchall()
        return info

        """SELECT modules.nommodule, (SELECT COUNT(*) FROM transactions WHERE lecture = 1), (SELECT COUNT(*) FROM transactions WHERE lecture = 0)
	FROM transactions
		INNER JOIN modules ON transactions.module = modules.idmodule
		INNER JOIN compagnie ON compagnie.idcompagnie = transactions.compagnie 
	WHERE compagnie.nomcompagnie = 'Cineclub'
	GROUP BY modules.nommodule;"""
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

    def trouver_roles(self):
        sql_role = ("select id_role, nom_role from 'Tbl_role'")
        self.curs.execute(sql_role)
        info = self.curs.fetchall()
        return info

    def trouver_roles_nom(self):
        sql_role = ("select nom_role from 'Tbl_role'")
        self.curs.execute(sql_role)
        info = self.curs.fetchall()
        return info

    def fermerdb(self):
        self.conn.close()

    ##
    def verifier_usager(self,nom_org, courriel): #n
        sql_org=("select * from 'compagnie' where nomcompagnie=:nom_org")
        sql_user=("select * from 'membre' where courriel=:courriel")
        self.curs.execute(sql_org, {'nom_org': nom_org})
        info_org = self.curs.fetchall()
        self.curs.execute(sql_user, { 'courriel':courriel})
        info_user=self.curs.fetchall()

        return [info_org,info_user]

    def verifier_membre(self, courriel): #n
        sql_user=("select * from 'membre' where courriel=:courriel")
        self.curs.execute(sql_user, { 'courriel':courriel})
        info_user=self.curs.fetchall()

        return info_user
        
    def retourner_role(self,role): #n
        sql_user=("select nom_role from 'tbl_role'")
        self.curs.execute(sql_user)
        info_user=self.curs.fetchall()
        sql_role=("select * from 'TBL_role' where nom_role=:role")
        self.curs.execute(sql_role, {
                                    'role': role})
                                    
        info_role=self.curs.fetchall()
        
    def inscrire_usager(self,nom, courriel, telephone, mdp, nom_org, type_org): #n
        sql_org=("insert into 'compagnie' ('nomcompagnie', 'type_entreprise') values (:nom_org, :type_org)")
        sql_nom=("insert into 'membre' ('compagnie', 'identifiant', 'mdp', 'permission', 'titre', 'courriel', 'telephone') values ((select idcompagnie from 'compagnie' where nomcompagnie=:nom_org), :courriel, :mdp,  'admin', 'président', :courriel, :telephone)")
        self.curs.execute(sql_org, {'nom_org': nom_org,
                                    'type_org': type_org})                          
        self.curs.execute(sql_nom, {'nom_org': nom_org,
                                    'mdp': mdp,
                                    'courriel': courriel,
                                    'telephone': telephone})                       
        self.conn.commit()
        return "test"

    def inscrire_module_role(self,nom_module, nom_role): #n
        sql_module_role=("insert into 'tbl_role_module' ('role', 'module') values ((select id_role from 'tbl_role' where nom_role=:nom_role), (select idmodule from 'modules' where nommodule=:nom_module))")                    
     
        self.curs.execute(sql_module_role, {'nom_role': nom_role,
                                        'nom_module': nom_module})                       
        self.conn.commit()
        return "test"

    
    def ajouter_module(self,nom_module): #n
        try:
            sql_module=("insert into 'modules' ('nommodule', 'version') values (:nom_module, 1)")
            self.curs.execute(sql_module, {'nom_module': nom_module})    
                        
            self.conn.commit()
        except:
            print("erreur")
        return "test"

    def inscrire_membre(self,nom, courriel, telephone, mdp, id_complet, id_emp, nom_admin, nom_role): #n
        sql_nom=("insert into 'membre' ('compagnie', 'identifiant', 'mdp', 'permission', 'titre', 'courriel', 'telephone') values ((select compagnie from 'membre' where identifiant=:nom_admin), :id_complet, :mdp,  'user', 'employe', :courriel, :telephone)")                         
        sql_role=("insert into 'Tbl_membre_role' ('membre', 'role') values (:id_emp, (select id_role from 'tbl_role' where nom_role=:nom_role))")                         
        self.curs.execute(sql_nom, {
                                    'nom_admin':nom_admin,
                                    'mdp': mdp,
                                    'id_complet': id_complet,
                                    'courriel': courriel,
                                    'telephone': telephone})
        self.conn.commit()

        sql_id=("select idmembre from 'membre' where identifiant=:id_complet")
        self.curs.execute(sql_id, {'id_complet':id_complet})
        id_membre=self.curs.fetchall()
        print(f'ID MEMBRE : {id_membre[0][0]}')

        self.curs.execute(sql_role, {
                                    'id_emp':id_membre[0][0],
                                    'nom_role':nom_role})                       
        self.conn.commit()
        return "test"


    def ajouter_role(self,role): #n
        sql_nom=("insert into 'Tbl_role' ('nom_role') values (:nom_role)")                         
        self.curs.execute(sql_nom, {'nom_role':role})                       
        self.conn.commit()
        return "test"

    # Inscrit les données de transactions de base de données
    def dataWrite(self, transac):
        print("I'M WRITING!!!")
        transac = json.loads(transac)
        print(f'VARIABLE TRANSAC: {transac["usager"]}')
        sqltransac = ("insert into 'transactions' ('lecture', 'membre', 'compagnie', 'module', 'date') values (0, :usager, :comp, :mod, CURRENT_TIMESTAMP)")                         
        self.curs.execute(sqltransac, {
                                    'usager':transac["usager"],
                                    'comp': transac["compagnie"],
                                    'mod': transac["module"]})
        self.conn.commit()
    
    # Inscrit les données de transactions de base de données
    def dataRead(self, transac):
        print("Je passe une transaction!")
        transac = json.loads(transac)
        print(f'VARIABLE TRANSAC: {transac["usager"]}')
        sqltransac = ("insert into 'transactions' ('lecture', 'membre', 'compagnie', 'module', 'date') values (1, :usager, :comp, :mod, CURRENT_TIMESTAMP)")                         
        self.curs.execute(sqltransac, {
                                    'usager':transac["usager"],
                                    'comp': transac["compagnie"],
                                    'mod': transac["module"]})  
        self.conn.commit()

def demanderclients():
    db=Dbclient()
    clients=db.trouverclients()
    db.fermerdb()
    return clients

#def inscrire
    
mesfonctions={"demanderclients":demanderclients}

def dataRead(transac):
    db=Dbman()
    db.dataRead(transac)
    db.fermerdb()

def dataWrite(transac):
    db=Dbman()
    db.dataWrite(transac)
    db.fermerdb()
    
@app.route('/')
def index():
    return 'Hello world du serveur '+ os.getcwd()

@app.route('/trouvermodules',methods=["GET","POST"])
def trouvermodules():
    listefichiers=[]
    monhome=os.path.dirname(os.path.realpath(sys.argv[0]))+"/SaaS_modules"
    #monhome=os.getcwd()+"/SaaS_modules"
    listefichiers=os.listdir(monhome)
    return Response(json.dumps(listefichiers), mimetype='application/json')

@app.route('/telechargermodule', methods=["GET","POST"])
def telechargermodule():
    if request.method=="POST":
        fichier=request.form["fichier"]
        monhome=os.path.dirname(os.path.realpath(sys.argv[0]))+"/SaaS_modules"
        bonfichier=open(monhome+"/"+fichier)
        lemodule=bonfichier.read()
        bonfichier.close()
        return Response(json.dumps(lemodule), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/identifierusager', methods=["GET","POST"])
def identifierusager():
    if request.method=="POST":
        nom=request.form["nom"]
        mdp=request.form["mdp"]
        db=Dbman()
        usager=db.identifierusager(nom,mdp)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

#################################################################################################################
#################################################################################################################
@app.route('/trouverprojets', methods=["GET","POST"])
def trouverprojets():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        db=Dbclient()
        projets=db.trouverprojets()
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouverprojetsAvecTriage', methods=["GET","POST"])
def trouverprojetsAvecTriage():
    if request.method=="POST":
        triage=request.form["triage"]
        db=Dbclient()
        projets=db.trouverprojetsAvecTriage(triage)
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/inscrire_contact', methods=["GET","POST"])
def inscrire_contact():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        db=Dbclient()
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        courriel = request.form["courriel"]
        ville = request.form["ville"]
        adresse = request.form["adresse"]
        telephone = request.form["telephone"]
        details = request.form["details"]
        notes = request.form["notes"]
        tag = request.form["tag"]
        projet = request.form["projet"]
        comp = request.form["comp"]
        transac = request.form["transac"]
        projets=db.inscrire_contact(prenom, nom, courriel, ville, adresse, telephone, details, notes, tag, comp, projet)
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/inscrire_taches', methods=["GET","POST"])
def inscrire_taches():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)
        
        db=Dbclient()
        nom_tache = request.form["nom_tache"]
        employe = request.form["employe"]
        role = request.form["role"]
        courriel = request.form["courriel"]
        details = request.form["details"]
        notes = request.form["notes"]
        # tag = request.form["tag"]
        projet = request.form["projet"]
        comp = request.form["comp"]
        projets=db.inscrire_contact(  nom_tache , employe,role,courriel,details, notes,projet, comp)
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")        
@app.route('/supprimer_contact', methods=["GET","POST"])
def supprimer_contact():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)
        
        db=Dbclient()
        idcontacts = request.form["idcontacts"]
        transac = request.form["transac"]
        projets=db.supprimer_contact(idcontacts)
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')

@app.route('/trouver_projet_infos', methods=["GET","POST"])
def trouver_projet_infos():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        db=Dbclient()
        projet = request.form["projet"]
        infos=db.trouver_projet_infos(projet)
       
        db.fermerdb()
        return Response(json.dumps(infos), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouvermembres', methods=["GET","POST"])
def trouvermembres():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        db=Dbman()
        membres=db.trouvermembres()
        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouvercompagnies', methods=["GET","POST"])        # Alex
def trouvercompagnies():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        db=Dbman()
        compagnies=db.trouver_compagnies()

        db.fermerdb()
        return Response(json.dumps(compagnies), mimetype='application/json')

@app.route('/trouver_membres_par_compagnie', methods=["GET","POST"])        # Alex
def trouver_membres_par_compagnie():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        db=Dbman()
        comp = request.form["comp"]
        membres=db.trouver_membres_par_compagnie(comp)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_projets_par_compagnie', methods=["GET","POST"])        # Alex
def trouver_projets_par_compagnie():
    if request.method=="POST":
        db=Dbclient()
        comp = request.form["comp"]
        print(comp)
        membres=db.trouver_projets_par_compagnie(comp)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_transactions_par_compagnie', methods=["GET","POST"])        # Alex
def trouver_transactions_par_compagnie():
    if request.method=="POST":
        db=Dbman()
        comp = request.form["comp"]
        print(comp)
        membres=db.trouver_transactions_par_compagnie(comp)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_contacts_par_projet', methods=["GET","POST"])        # Alex
def trouver_contacts_par_projet():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        db=Dbclient()
        comp = request.form["comp"]
        contacts=db.trouver_contacts_par_projet(comp)

        db.fermerdb()
        return Response(json.dumps(contacts), mimetype='application/json')

@app.route('/get_contact_details', methods=["GET","POST"])        # Alex
def get_contact_details():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        db=Dbclient()
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        expertise = request.form["expertise"]
        contacts=db.get_contact_details(prenom, nom, expertise)

        db.fermerdb()
        return Response(json.dumps(contacts), mimetype='application/json')

@app.route('/trouver_projet_par_compagnie', methods=["GET","POST"]) #N
def trouver_projet_par_compagnie():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        id_comp=request.form["id"]
        db=Dbclient()
        projets=db.trouver_projet_par_compagnie(id_comp)
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouver_permissions_par_membre', methods=["GET","POST"])        # Alex
def trouver_permissions_par_membre():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        db=Dbman()
        membre = request.form["membre"]
        membres=db.trouver_permissions_par_membre(membre)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_roles', methods=["GET","POST"])
def trouver_roles():
    if request.method == "POST":
        db = Dbman()
        # transac = request.form["transac"]
        # roles = db.trouver_roles(transac)
        roles = db.trouver_roles()

        db.fermerdb()
        return Response(json.dumps(roles), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouver_roles_nom', methods=["GET","POST"]) #n
def trouver_roles_nom():
    if request.method == "POST":
        db = Dbman()
        # transac = request.form["transac"]
        # roles = db.trouver_roles_nom(transac)
        roles = db.trouver_roles_nom()

        db.fermerdb()
        return Response(json.dumps(roles), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouver_expertises', methods=["GET","POST"])
def trouver_expertises():
    if request.method == "POST":
        transac = request.form["transac"]
        dataRead(transac)

        db = Dbclient()
        expertises = db.trouver_expertises()

        db.fermerdb()
        return Response(json.dumps(expertises), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")
    
@app.route('/requeteserveur', methods=["GET","POST"])
def requeteserveur():
    if request.method=="POST":
        nomfonction=request.form["fonction"]
        transac = request.form["transac"]
        rep=mesfonctions[nomfonction]()
        n=1
        return Response(json.dumps(rep), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")
##

@app.route('/verifierusager', methods=["GET","POST"]) #N
def verifier_usager():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        nom_org=request.form["nom_org"]
        courriel=request.form["courriel"]
        db=Dbman()
        usager=db.verifier_usager(nom_org, courriel)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")



@app.route('/verifiermembre', methods=["GET","POST"]) #N
def verifier_membre():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        courriel=request.form["courriel"]
        db=Dbman()
        usager=db.verifier_membre(courriel)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/verifierprojet', methods=["GET","POST"]) #N
def verifier_projet():
    if request.method=="POST":
        transac = request.form["transac"]
        dataRead(transac)

        nom_projet=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        db=Dbclient()
        usager=db.verifier_projet(nom_projet, nom_client)
        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/verifierclient', methods=["GET","POST"]) #N
def verifier_client():
    if request.method=="POST":
        # transac = request.form["transac"]
        # dataRead(transac)

        courriel=request.form["courriel"]
        db=Dbclient()
        usager=db.verifier_client(courriel)
        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")


@app.route('/inscrireusager', methods=["GET","POST"]) #N
def inscrire_usager():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom=request.form["nom_user"]
        courriel=request.form["courriel"]
        telephone=request.form["telephone"]
        mdp=request.form["mdp"]
        nom_org=request.form["nom_org"]
        type_org=request.form["type_org"]

        db=Dbman()
        usager=db.inscrire_usager(nom, courriel, telephone, mdp, nom_org, type_org)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/inscriremodulemembre', methods=["GET","POST"]) #N
def inscrire_module_role():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom_module=request.form["nom_module"]
        nom_role=request.form["nom_role"]

        db=Dbman()
        usager=db.inscrire_module_role(nom_module,nom_role)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/inscrireclient', methods=["GET","POST"]) #N
def inscrire_client():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom_client=request.form["nom_client"]
        courriel=request.form["courriel"]
        telephone=request.form["telephone"]
        compagnie=request.form["compagnie"]
        adresse=request.form["adresse"]
        rue=request.form["rue"]
        ville=request.form["ville"]

        db=Dbclient()
        usager=db.inscrire_client(nom_client, courriel, telephone, compagnie, adresse, rue,ville)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/inscriremembre', methods=["GET","POST"]) #N
def inscrire_membre():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom=request.form["nom_user"]
        courriel=request.form["courriel"]
        telephone=request.form["telephone"]
        mdp=request.form["mdp"]
        id_complet=request.form["id_complet"]
        id_emp=request.form["id"]
        nom_admin=request.form["nom_admin"]
        nom_role=request.form["nom_role"]

        db=Dbman()
        usager=db.inscrire_membre(nom, courriel, telephone, mdp, id_complet, id_emp, nom_admin, nom_role)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/ajouterprojet', methods=["GET","POST"]) #N
def ajouter_projet():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom_proj=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        responsable=request.form["responsable"]
        date_deb=request.form["date_deb"]
        date_fin=request.form["date_fin"]
        nom_compagnie=request.form["nom_compagnie"]

        db=Dbclient()
        usager=db.ajouter_projet(nom_proj, nom_client, responsable, date_deb, date_fin, nom_compagnie)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/ajouterprojetfournisseur', methods=["GET","POST"]) #N
def ajouter_projet_fournisseur():
    if request.method=="POST":
        nom_proj=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        responsable=request.form["responsable"]
        date_deb=request.form["date_deb"]
        date_fin=request.form["date_fin"]
        nom_compagnie=request.form["nom_compagnie"]

        db=Dbclient()
        usager=db.ajouter_projet_fournisseur(nom_proj, nom_client, responsable, date_deb, date_fin, nom_compagnie)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")


@app.route('/envoyer_modifs', methods=["GET","POST"]) #N
def envoyer_modifs():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        idprojet=request.form["idprojet"]
        nom_proj=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        responsable=request.form["responsable"]
        date_deb=request.form["date_deb"]
        date_fin=request.form["date_fin"]
        nom_compagnie=request.form["nom_compagnie"]

        db=Dbclient()
        usager=db.envoyer_modifs(idprojet, nom_proj, nom_client, responsable, date_deb, date_fin, nom_compagnie)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/envoyer_supression', methods=["GET","POST"]) #N
def envoyer_supression():
    if request.method=="POST":
        nom_proj=request.form["nom_projet"]
        db=Dbclient()
        usager=db.envoyer_supression(nom_proj)
        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/ajoutermodulebd', methods=["GET","POST"]) #N
def ajouter_module():
    if request.method=="POST":
        nom_module=request.form["nom_module"]
        # transac = request.form["transac"]

        db=Dbman()
        # usager=db.ajouter_module(nom_module, transac)
        usager=db.ajouter_module(nom_module)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/ajouterrole', methods=["GET","POST"]) #N
def ajouter_role():
    if request.method=="POST":
        transac = request.form["transac"]
        dataWrite(transac)

        nom_role=request.form["nom_role"]

        db=Dbman()
        usager=db.ajouter_role(nom_role)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

if __name__ == '__main__':
    #print(flask.__version__)
    #app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
