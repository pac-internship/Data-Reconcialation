import sqlite3
from datetime import datetime

# Connexion à la base de données principale A
conn_A = sqlite3.connect('C:/Users/HP/Documents/base_A.db')
cursor_A = conn_A.cursor()

# Ajout du champ statut si ce n'est pas encore fait (décommenter si nécessaire)
# cursor_A.execute('ALTER TABLE factures ADD COLUMN statut TEXT NOT NULL DEFAULT "Actif"')

# Liste des factures à insérer avec le statut
factures = [
    ("Facture 001", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 002", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 003", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 004", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 005", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 006", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 007", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 008", datetime.now().strftime('%Y-%m-%d'), "Actif"),
    ("Facture 009", datetime.now().strftime('%Y-%m-%d'), "Inactif"),
    ("Facture 010", datetime.now().strftime('%Y-%m-%d'), "Inactif")
]

# Insertion des factures seulement si elles n'existent pas déjà
for facture, date, statut in factures:
    cursor_A.execute(''' 
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ? 
    ''', (facture, date))
    
    # Récupérer le nombre de factures correspondantes
    count = cursor_A.fetchone()[0]
    
    if count == 0:
        cursor_A.execute('''
        INSERT INTO factures (facture, date, statut)
        VALUES (?, ?, ?)
        ''', (facture, date, statut))
        print(f"Facture '{facture}' insérée avec succès.")
    else:
        print(f"Facture '{facture}' existe déjà, insertion ignorée.")

# Enregistrer les modifications
conn_A.commit()

# Fermer la connexion à la base de données A
conn_A.close()

print("Vérification et insertion des factures terminées.")
