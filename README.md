# Park Control - Système de Gestion de Parc Automobile

<div align="center">
  <img src="https://www.fede.education/wp-content/uploads/2024/10/logo-FEDE_2023_2xRetina.png" alt="FEDE Logo" width="200"/>
  <br/>
  <small>Projet réalisé dans le cadre du Bachelor Européen en Informatique et Réseaux</small>
  <br/>
  <small>Spécialisation : Développement Logiciel et Bases de Données</small>
</div>

## 📝 Description
Park Control est une application web de gestion de parc automobile développée dans le cadre d'un projet de fin d'études pour le Bachelor Européen FEDE en Informatique et Réseaux, spécialisation Développement Logiciel et Bases de Données. Cette application permet de gérer efficacement une flotte de véhicules, les réservations, les employés et les utilisateurs du système.

## 🚀 Fonctionnalités

### 1. Tableau de Bord
- Visualisation des statistiques en temps réel
- Graphiques interactifs pour les véhicules, réservations et employés
- Vue d'ensemble de l'activité du parc automobile

### 2. Gestion des Véhicules
- Suivi de l'état des véhicules
- Gestion des marques et modèles
- Suivi des maintenances
- Historique des utilisations

### 3. Gestion des Réservations
- Système de réservation de véhicules
- Validation des disponibilités
- Prévention des doubles réservations
- Historique des réservations

### 4. Gestion des Employés
- Suivi du personnel
- Gestion des départements
- Historique des utilisations de véhicules

### 5. Gestion des Utilisateurs
- Système d'authentification sécurisé
- Gestion des rôles et permissions
- Interface d'administration

## 🛠️ Technologies Utilisées

### Backend
- Python 3.x
- Flask (Framework Web)
- SQLAlchemy (ORM)
- MySQL (Base de données)

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Chart.js (Visualisation de données)

### Sécurité
- Authentification par session
- Gestion des rôles
- Protection CSRF
- Validation des entrées

## 📋 Prérequis

- Python 3.x
- MySQL Server
- pip (Gestionnaire de paquets Python)

## 🔧 Installation

1. Cloner le repository
```bash
git clone https://github.com/votre-username/park_control.git
cd park_control
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données
```bash
# Créer la base de données MySQL
mysql -u root -p
CREATE DATABASE park_control;
```

5. Configurer les variables d'environnement
```bash
# Créer un fichier .env
cp .env.example .env
# Modifier les variables selon votre configuration
```

6. Initialiser la base de données
```bash
flask db upgrade
```

7. Lancer l'application
```bash
python app.py
```

## 📚 Structure du Projet

```
park_control/
├── app.py                 # Point d'entrée de l'application
├── config.py             # Configuration de l'application
├── requirements.txt      # Dépendances Python
├── models/              # Modèles de données
│   ├── database.py
│   ├── utilisateur.py
│   ├── vehicule.py
│   ├── reservation.py
│   └── employee.py
├── routes/              # Routes de l'application
│   ├── auth.py
│   ├── users.py
│   ├── vehicules.py
│   ├── reservations.py
│   └── dashboard.py
├── templates/           # Templates HTML
│   ├── base.html
│   ├── auth/
│   ├── users/
│   ├── vehicules/
│   └── reservations/
└── static/             # Fichiers statiques
    ├── css/
    ├── js/
    └── assets/
```

## 🔐 Sécurité

- Authentification requise pour toutes les routes
- Gestion des rôles (Admin, Utilisateur)
- Protection contre les injections SQL
- Validation des entrées utilisateur
- Sessions sécurisées

## 👥 Rôles Utilisateurs

1. **Administrateur**
   - Accès complet à toutes les fonctionnalités
   - Gestion des utilisateurs
   - Gestion des véhicules
   - Gestion des réservations

2. **Utilisateur Standard**
   - Consultation des véhicules
   - Création de réservations
   - Consultation de son profil

## 📊 Base de Données

### Tables Principales
- `utilisateurs`: Gestion des utilisateurs
- `vehicules`: Informations sur les véhicules
- `reservations`: Gestion des réservations
- `employees`: Gestion du personnel
- `etats`: États des véhicules

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence [MIT](LICENSE).

## 👨‍💻 Auteur

- **Younes EL BORAKI** - *Développeur*
  - Bachelor Européen FEDE en Informatique et Réseaux
  - Spécialisation : Développement Logiciel et Bases de Données
  - Projet de fin d'études

## 🙏 Remerciements

- [FEDE - Fédération Européenne des Écoles](https://www.fede.education/) pour le cadre du projet
- Tous les contributeurs

---

*Ce projet a été réalisé dans le cadre du Bachelor Européen FEDE en Informatique et Réseaux, spécialisation Développement Logiciel et Bases de Données en 2024* 
