# ProjetSAAS

Équipe: Samuel, Alex Bouchard, Norman Tao

** Logiciel Client **

Fonctionnalités : 
  - Sign up: un locataire peut créer une compagnie
  - Ajout de membre : un locataire peut ajouter un membre dans le module "Membre"
		- Reste a remplacer le champ texte "Rôle" par un menu déroulant quand l'ajout de rôles sera complété
  - Ajout de projet : un locataire peut ajouter un nouveau projet dans le module "Gestion de projet"
		- Pour l'instant, on doit utiliser un client déjà existant pour créer une nouvelle compagnie. *POUR TESTER, ENTREZ "joebine" DANS LE CHAMP "Nom de l'organisation client"
  - Ajout de rôle   : un locataire peut ajouter de nouveaux rôles et leur assigner des modules disponibles dans le module "Gestion de membres -> Définir les rôles (INCOMPLET):
		- interface graphique terminé, implémentations des fonctions d'appel et d'inscription a la bdd reste à compléter
Instruction : 
  - Un bouton est ajouté dans les cadres respectifs pour l'ajout dans les bases de données. Lorsque le formulaire est envoyé, le serveur envoie une requête à la base de données et inscrit les informations si l'objet qu'on désire ajouter n'existe pas.


** Logiciel Fournisseur **

Fonctionnalités :
  - L'utilisateur peut sélectionner la compagnie qu'il désire consulter en utilisant le menu déroulant
  - Le premier cadre affiche la liste de membres de la compagnie sélectionnée
  - Quand l'utilisateur sélectionne un nom dans la liste, le cadre inférieur affiche la liste des modules pour cet utilisateur
  

NOTES :
  - Pour l'instant, on ne voit pas de rôles affichés lorsqu'on sélectionne un membre puisque les rôles ne sont pas encore inscrits aux usagers tel que prévu.

