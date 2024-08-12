# Utilisez une image Python officielle comme base
FROM python:3.10-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet dans le conteneur
COPY . /app/

# Exposer le port 8000 pour accéder à l'application
EXPOSE 8000

# Commande pour lancer le serveur de développement Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
