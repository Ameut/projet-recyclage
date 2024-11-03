"""
WSGI config for recycling_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recycling_project.settings')

application = get_wsgi_application()


#DATABASES = {
  #  'default': {
     #   'ENGINE': 'django.db.backends.postgresql',
      #  'NAME': 'projet-recyclage',  # Nom de la base de données
      #  'USER': 'root',  # Remplace par ton nom d'utilisateur PostgreSQL
      #  'PASSWORD': 'recyclage2024projet',  # Remplace par ton mot de passe PostgreSQL
      #  'HOST': 'localhost',  # Ou l'IP du serveur si la base n'est pas en local
      #  'PORT': '5432',  # Port par défaut pour PostgreSQL
   # }
#}

