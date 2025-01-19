**Auteur** : Ameur Ouafi  
**Projet** : Sud Recycling  
**Description** : Une plateforme web pour promouvoir l'entreprise, faciliter la communication entre les clients et l'entreprise, et gérer les inventaires internes de manière sécurisée pour les salariés. Ce projet est conteneurisé avec Docker pour une installation et un déploiement simplifiés.

---

## Fonctionnalités

- **Promotion de l'entreprise** : Présentation des services et des valeurs de Sud Recycling.
- **Communication client-entreprise** : Formulaire de contact, suivi des demandes, et notifications.
- **Gestion des inventaires** : Interface sécurisée pour les salariés afin de gérer les stocks et les matériaux recyclés.
- **Sécurité** : Accès protégé par mot de passe pour les sections réservées aux salariés.

---

## Technologies Utilisées

- **Framework** : Django (backend)
- **Base de données** : PostgreSQL (ou SQLite pour le développement)
- **Conteneurisation** : Docker et Docker Compose
- **Frontend** : HTML, CSS, JavaScript (avec Bootstrap pour le design)
- **Autres outils** : Git, Nginx (pour le reverse proxy en production)

---

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker** : [Guide d'installation de Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** : [Guide d'installation de Docker Compose](https://docs.docker.com/compose/install/)
- **Git** : [Guide d'installation de Git](https://git-scm.com/downloads)

---

## Installation

### 1. Cloner le projet

Ouvrez un terminal et exécutez la commande suivante pour cloner le dépôt :

```bash
git clone https://github.com/votre_nom_utilisateur/sud-recycling.git
cd sud-recycling
