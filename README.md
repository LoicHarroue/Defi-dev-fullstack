# Defi-dev-fullstack
Test technique Scanlitt


# Installation 
Après avoir déployer le projet dans Docker (build puis up), vous pouvez l'ouvrir dans un IDE (VSCode) 
et exécuter ces commandes :

docker exec -it defidev-web-1 bash
python manage.py makemigrations
python manage.py migrate
python manage.py search_index --delete --force
python manage.py search_index --create
python manage.py search_index --populate

après cela l'API sera prête sur cette adresse http://127.0.0.1:8000/recherche

# Tests
Pour tester directement l'application vous pouvez :
-Ajouter une équipe
-Ajouter onze joueur (un douzième pour tester la limite)
-Crée un match après avoir crée une autre équipe
-Rechercher un joueur ou une équipe

sinon un test.py est présent pour pouvoir tester le programme avec python manage.py test
