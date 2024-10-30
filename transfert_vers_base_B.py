import sqlite3

# Connexion aux bases de données Tampon B et la base principale B
conn_Tampon_B = sqlite3.connect('C:/Users/HP/Documents/tampon_B.db') 
conn_B = sqlite3.connect('C:/Users/HP/Documents/base_B.db') 

# Création de curseurs
cursor_Tampon_B = conn_Tampon_B.cursor()
cursor_B = conn_B.cursor()

# Récupérer les données de la base Tampon B
cursor_Tampon_B.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_B = cursor_Tampon_B.fetchall()

# Récupérer les données de la base principale B
cursor_B.execute('SELECT id, facture, date, statut FROM factures')
factures_B = cursor_B.fetchall()

#  Vérification des factures présentes dans Tampon B mais absentes dans la base principale B 
print("\nFactures présentes dans Tampon B mais absentes dans la base principale B :")   
for facture in factures_Tampon_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_B.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_B.fetchone()[0]
    
    if count == 0:
        print(contenu_facture)

#  Vérification des factures présentes dans la base principale B mais absentes dans Tampon B 
print("\nFactures présentes dans la base principale B mais absentes dans Tampon B :")
for facture in factures_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_Tampon_B.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_Tampon_B.fetchone()[0]
    
    if count == 0:
        print(contenu_facture) 

#  Transfert des données de Tampon B vers la base principale B après vérification du statut
# Insérer les données dans la base principale B après vérification
for facture in factures_Tampon_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    # On vérifie d'abord que le statut est "Actif"
    if statut_facture == "Actif":
        # Vérification si la facture existe déjà dans la base principale B
        cursor_B.execute(''' 
        SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
        ''', (contenu_facture, date_facture))
        
        count = cursor_B.fetchone()[0]

        if count == 0:
            # Si la facture n'existe pas, on l'insère avec le statut "Actif"
            cursor_B.execute('''
            INSERT INTO factures (facture, date, statut)
            VALUES (?, ?, ?)
            ''', (contenu_facture, date_facture, statut_facture))
            print(f"Facture '{contenu_facture}' transférée vers la base principale B avec statut '{statut_facture}'.")
        else:
            print(f"Facture '{contenu_facture}' déjà présente dans la base principale B, transfert ignoré.")
    else:
        print(f"Facture '{contenu_facture}' ignorée car son statut est '{statut_facture}'.")       


# Enregistrer les changements dans la base principale B
conn_B.commit()

# Fermer les connexions
conn_Tampon_B.close()
conn_B.close()

print("\nTransfert des données de Tampon B vers la base principale B terminé avec succès.")
