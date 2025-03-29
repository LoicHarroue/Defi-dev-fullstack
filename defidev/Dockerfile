# Utilisation d'une image Python officielle
FROM python:3.11-slim
LABEL authors="loicharroue"
# Définir les variables d'environnement
ENV PYTHONUNBUFFERED 1

# Créer un répertoire pour l'application
RUN mkdir /app
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port par défaut (8000 pour Django)
EXPOSE 8000

# Commande pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
