import sqlite3

# Créer les connexions aux bases de données
conn_A = sqlite3.connect('C:/Users/HP/Documents/base_A.db')  
conn_Tampon_A = sqlite3.connect('C:/Users/HP/Documents/tampon_A.db') 
conn_B = sqlite3.connect('C:/Users/HP/Documents/base_B.db') 
conn_Tampon_B = sqlite3.connect('C:/Users/HP/Documents/tampon_B.db') 

# Création de curseurs pour exécuter des commandes SQL
cursor_A = conn_A.cursor()
cursor_Tampon_A = conn_Tampon_A.cursor()
cursor_B = conn_B.cursor()
cursor_Tampon_B = conn_Tampon_B.cursor()

# Créer les tables dans les bases de données (A, Tampon A, B, et Tampon B)

# Table dans la base principale A
cursor_A.execute('''
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture TEXT NOT NULL,
    date TEXT NOT NULL,
    statut TEXT NOT NULL  
)
''')

# Table dans la base Tampon A
cursor_Tampon_A.execute('''
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture TEXT NOT NULL,
    date TEXT NOT NULL,
    statut TEXT NOT NULL  
)
''')

# Table dans la base principale B
cursor_B.execute('''
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture TEXT NOT NULL,
    date TEXT NOT NULL,
    statut TEXT NOT NULL  
)
''')

# Table dans la base Tampon B
cursor_Tampon_B.execute('''
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture TEXT NOT NULL,
    date TEXT NOT NULL,
    statut TEXT NOT NULL  
)
''')

# Enregistrer les modifications dans toutes les bases
conn_A.commit()
conn_Tampon_A.commit()
conn_B.commit()
conn_Tampon_B.commit()

# Fermer les connexions à toutes les bases
conn_A.close()
conn_Tampon_A.close()
conn_B.close()
conn_Tampon_B.close()

print("Tables créées avec succès dans toutes les bases de données.")
