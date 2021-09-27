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
        nomdb=os.getcwd()+"/SaaS_clients/"+"GestMedia_client.sqlite"
        self.conn = sqlite3.connect(nomdb)
        self.curs = self.conn.cursor()

    def trouverprojets(self):
        sqlnom=("select Nomdeprojet, datedelancement, datedefinprevue from 'projet'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info
    
    def trouverclients(self):
        sqlnom=("select compagnie, nom, courriel from 'client'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def fermerdb(self):
        self.conn.close()

    def verifier_projet(self,nom_projet, nom_client):
        sql_proj=("select * from 'projet' where Nomdeprojet=:nom_projet")
        self.curs.execute(sql_proj, {'nom_projet': nom_projet})

        info_projet=self.curs.fetchall()

        sql_client=("select * from 'client' where nom=:nom_client")
        self.curs.execute(sql_client, {'nom_client':nom_client})

        info_client=self.curs.fetchall()

        return [info_projet,info_client]


    def ajouter_projet(self,nom_projet, nom_client, responsable, date_deb, date_fin):
        sql_nom=("insert into 'projet' ('Nomdeprojet', 'client', 'chargedeprojet', 'datedelancement', 'datedefinprevue') values (:nom_projet, (select idclient from client where nom=:nom_client), :responsable, :date_deb, :date_fin)")                         
        self.curs.execute(sql_nom, {
                                    'nom_projet':nom_projet,
                                    'nom_client': nom_client,
                                    'responsable': responsable,
                                    'date_deb': date_deb,
                                    'date_fin': date_fin})                       
        self.conn.commit()
        return "test"

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
#####################################################################################################
    def trouver_membres_par_compagnie(self, comp):        # Alex
        sqlnom = ("select identifiant, permission,titre from 'membre' INNER JOIN 'compagnie' ON membre.compagnie=compagnie.idcompagnie WHERE compagnie.nomcompagnie=:comp")
        self.curs.execute(sqlnom, {'comp': comp})
        info = self.curs.fetchall()
        return info

    def trouver_permissions_par_membre(self, membre):        # Alex
        sqlnom = ("select nommodule from 'modules' "
                  "INNER JOIN 'Tbl_role_module' ON modules.idmodule=Tbl_role_module.id_role_module "
                  "INNER JOIN 'Tbl_role' ON Tbl_role_module.role=Tbl_role.id_role "
                  "INNER JOIN 'Tbl_membre_role' ON Tbl_role.id_role=Tbl_membre_role.role "
                  "INNER JOIN 'membre' ON Tbl_membre_role.membre=membre.idmembre WHERE membre.identifiant=:membre")
        self.curs.execute(sqlnom, {'membre': membre})
        info = self.curs.fetchall()
        return info
#####################################################################################################
    def trouver_compagnies(self):           # Alex
        sqlnom=("select nomcompagnie from 'compagnie'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def trouver_roles(self):
        sql_role = ("select id_role, nom_role from 'Tbl_role'")
        self.curs.execute(sql_role)
        info = self.curs.fetchall()
        return info


    def fermerdb(self):
        self.conn.close()

    ##
    def verifier_usager(self,nom_org, courriel):
        sql_org=("select * from 'compagnie' where nomcompagnie=:nom_org")
        sql_user=("select * from 'membre' where courriel=:courriel")
        self.curs.execute(sql_org, {'nom_org': nom_org})
        info_org = self.curs.fetchall()
        self.curs.execute(sql_user, { 'courriel':courriel})
        info_user=self.curs.fetchall()

        return [info_org,info_user]

    def verifier_membre(self, id):
        sql_user=("select * from 'membre' where identifiant=:id")
        self.curs.execute(sql_user, { 'id':id})
        info_user=self.curs.fetchall()

        return info_user

    def inscrire_usager(self,nom, courriel, telephone, mdp, nom_org, type_org):
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

    def inscrire_membre(self,nom, courriel, telephone, mdp, id_emp, nom_admin):
        sql_nom=("insert into 'membre' ('compagnie', 'identifiant', 'mdp', 'permission', 'titre', 'courriel', 'telephone') values ((select compagnie from 'membre' where identifiant=:nom_admin), :id_emp, :mdp,  'user', 'employe', :courriel, :telephone)")                         
        self.curs.execute(sql_nom, {
                                    'nom_admin':nom_admin,
                                    'mdp': mdp,
                                    'id_emp': id_emp,
                                    'courriel': courriel,
                                    'telephone': telephone})                       
        self.conn.commit()
        return "test"

def demanderclients():
    db=Dbclient()
    clients=db.trouverclients()
    db.fermerdb()
    return clients
    
mesfonctions={"demanderclients":demanderclients}

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



@app.route('/trouverprojets', methods=["GET","POST"])
def trouverprojets():
    if request.method=="POST":
        db=Dbclient()
        projets=db.trouverprojets()
        #db=Dbman()
        #projets=db.trouvermembres()
        db.fermerdb()
        return Response(json.dumps(projets), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/trouvermembres', methods=["GET","POST"])
def trouvermembres():
    if request.method=="POST":
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
        db=Dbman()
        compagnies=db.trouver_compagnies()

        db.fermerdb()
        return Response(json.dumps(compagnies), mimetype='application/json')

@app.route('/trouver_membres_par_compagnie', methods=["GET","POST"])        # Alex
def trouver_membres_par_compagnie():
    if request.method=="POST":
        db=Dbman()
        comp = request.form["comp"]
        membres=db.trouver_membres_par_compagnie(comp)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_permissions_par_membre', methods=["GET","POST"])        # Alex
def trouver_permissions_par_membre():
    if request.method=="POST":
        db=Dbman()
        membre = request.form["membre"]
        membres=db.trouver_permissions_par_membre(membre)

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')

@app.route('/trouver_roles', methods=["GET","POST"])
def trouver_roles():
    if request.method == "POST":
        db = Dbman()
        roles = db.trouver_roles()

        db.fermerdb()
        return Response(json.dumps(roles), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")
    
@app.route('/requeteserveur', methods=["GET","POST"])
def requeteserveur():
    if request.method=="POST":
        nomfonction=request.form["fonction"]
        rep=mesfonctions[nomfonction]()
        n=1
        return Response(json.dumps(rep), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")
##

@app.route('/verifierusager', methods=["GET","POST"])
def verifier_usager():
    if request.method=="POST":
        nom_org=request.form["nom_org"]
        courriel=request.form["courriel"]
        db=Dbman()
        usager=db.verifier_usager(nom_org, courriel)

        #db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/verifiermembre', methods=["GET","POST"])
def verifier_membre():
    if request.method=="POST":
        id_emp=request.form["id"]
        db=Dbman()
        usager=db.verifier_membre(id_emp)

        #db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/verifierprojet', methods=["GET","POST"])
def verifier_projet():
    if request.method=="POST":
        nom_projet=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        db=Dbclient()
        usager=db.verifier_projet(nom_projet, nom_client)
        #db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")


@app.route('/inscrireusager', methods=["GET","POST"])
def inscrire_usager():
    if request.method=="POST":
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

@app.route('/inscriremembre', methods=["GET","POST"])
def inscrire_membre():
    if request.method=="POST":
        nom=request.form["nom_user"]
        courriel=request.form["courriel"]
        telephone=request.form["telephone"]
        mdp=request.form["mdp"]
        id_emp=request.form["id"]
        nom_admin=request.form["nom_admin"]

        db=Dbman()
        usager=db.inscrire_membre(nom, courriel, telephone, mdp, id_emp, nom_admin)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

@app.route('/ajouterprojet', methods=["GET","POST"])
def ajouter_projet():
    if request.method=="POST":
        nom_proj=request.form["nom_projet"]
        nom_client=request.form["nom_client"]
        responsable=request.form["responsable"]
        date_deb=request.form["date_deb"]
        date_fin=request.form["date_fin"]

        db=Dbclient()
        usager=db.ajouter_projet(nom_proj, nom_client, responsable, date_deb, date_fin)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        #return repr(usager)
    else:
        return repr("pas ok")

if __name__ == '__main__':
    #print(flask.__version__)
    #app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
