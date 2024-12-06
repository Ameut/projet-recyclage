# Utiliser une image Python de base
FROM python:3.9

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du projet dans le conteneur
COPY . /app

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
