# Transfert de données contrôlé entre bases de données

Ce projet implémente un système de transfert de données sécurisé entre deux bases de données principales à travers des bases tampons. Il s'assure que les données respectent des conditions spécifiques avant d'être transférées.

## Fonctionnalités principales

- **Transfert Tampon A → Tampon B** : Vérification des données dans Tampon A et leur transfert contrôlé vers Tampon B si elles respectent les critères définis.
- **Transfert Tampon B → Base principale B** : Validation et transfert des données de Tampon B vers la base principale B avec gestion du statut des factures.
- **Rapports d'activité par e-mail** : Un email est envoyé après chaque transfert pour informer de son succès ou de ses échecs.

## Prérequis

1. **Python 3.x** : Assurez-vous d'avoir une version compatible de Python installée sur votre machine.
2. **Bibliothèques Python nécessaires** :
   - `sqlite3` (module standard)
   - `smtplib` (module standard)
   - `email` (module standard)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/<ton-nom-utilisateur>/<Data-reconcialation>.git
   
2. Accédez au dossier du projet
     cd <Data-reconcialation>

3. Configurez les fichiers de base de données SQLite nécessaires (tampon_A.db, tampon_B.db, base_A.db, base_B.db) dans le répertoire du projet.

**Utilisation**
Exécution des scripts

**Transfert Tampon A → Tampon B :**
python transfert_tampon_A_vers_tampon_B.py

**Transfert Tampon B → Base principale B :**
python transfert_tampon_B_vers_base_B.py

Configuration des emails
Remplacez les informations suivantes dans les scripts Python avant exécution :

ton_email@example.com : votre adresse email.
ton_mot_de_passe : mot de passe de votre compte email.
destinataire@example.com : adresse email du destinataire.
Si vous utilisez Gmail, assurez-vous d’activer l'accès pour les applications tierces ou configurer Gmail (désormais via mots de passe d'application).

**Structure du projet**
├── tampon_A.db         # Base de données tampon A
├── tampon_B.db         # Base de données tampon B
├── base_A.db           # Base principale A
├── base_B.db           # Base principale B
├── transfert_tampon_A_vers_tampon_B.py  # Script de transfert A → B
├── transfert_tampon_B_vers_base_B.py    # Script de transfert B → Base principale
├── README.md           # Documentation du projet




Ce projet a été réalisé dans le cadre de la gestion de données entre systèmes isolés avec transfert sécurisé.


   

