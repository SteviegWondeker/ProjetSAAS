# ProjetSAAS

Équipe: Samuel, Alex Bouchard, Norman Tao

** Logiciel Client **

Fonctionnalités : 
  - Sign up: un locataire peut créer ajouter une compagnie
  - Ajout de membre : un locataire peut ajouter un membre dans le module "Membre"
  - Ajout de projet : un locataire peut ajouter un nouveau projet dans le module "Gestion de projet"

Instruction : 
  - Un bouton est ajouté dans les cadres respectifs pour l'ajout dans les bases de données. Lorsque le formulaire est envoyé, le serveur envoie une requête à la base de données et inscrit les informations si l'objet qu'on désire ajouter n'existe pas.


** Logiciel Fournisseur **

Fonctionnalités :
  - L'utilisateur peut sélectionner la compagnie qu'il désire consulter en utilisant le menu déroulant
  - Le premier cadre affiche la liste de membres de la compagnie sélectionnée
  - Quand l'utilisateur sélectionne un nom dans la liste, le cadre inférieur affiche la liste des modules pour cet utilisateur
  
NOTES :
  - Pour l'instant, on ne voit pas de rôles affichés lorsqu'on sélectionne un membre puisque les rôles ne sont pas encore inscrits aux usagers tel que prévu.