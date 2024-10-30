import sqlite3

# Connexion aux bases de données Tampon A et Tampon B
conn_Tampon_A = sqlite3.connect('C:/Users/HP/Documents/tampon_A.db')
conn_Tampon_B = sqlite3.connect('C:/Users/HP/Documents/tampon_B.db')

# Création de curseurs
cursor_Tampon_A = conn_Tampon_A.cursor()
cursor_Tampon_B = conn_Tampon_B.cursor()

# Récupérer les données de la base Tampon A
cursor_Tampon_A.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_A = cursor_Tampon_A.fetchall()

# Récupérer les données de la base Tampon B
cursor_Tampon_B.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_B = cursor_Tampon_B.fetchall()

#  Vérification des factures présentes dans Tampon A mais absentes dans Tampon B
print("\nTampon A ==> Tampon B : Données non transmises")   
for facture in factures_Tampon_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_Tampon_B.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_Tampon_B.fetchone()[0]
    
    if count == 0:
        print(contenu_facture)

#  Vérification des factures présentes dans Tampon B mais absentes dans Tampon A
for facture in factures_Tampon_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_Tampon_A.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_Tampon_A.fetchone()[0]
    
    if count == 0:
        print(f"Facture '{contenu_facture}' avec la date '{date_facture}' n'est pas dans la base Tampon A.")

# Insérer les données dans la base Tampon B après vérification du statut
for facture in factures_Tampon_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    # On vérifie d'abord que le statut est "Actif"
    if statut_facture == "Actif":
        # Vérification si la facture existe déjà dans Tampon B
        cursor_Tampon_B.execute('''
        SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
        ''', (contenu_facture, date_facture))
        
        count = cursor_Tampon_B.fetchone()[0]

        if count == 0:
            # Si la facture n'existe pas, on l'insère avec le statut "Actif"
            cursor_Tampon_B.execute('''
            INSERT INTO factures (facture, date, statut)
            VALUES (?, ?, ?)
            ''', (contenu_facture, date_facture, statut_facture))
            print(f"Facture '{contenu_facture}' transférée vers Tampon B avec statut '{statut_facture}'.")
        else:
            print(f"Facture '{contenu_facture}' déjà présente dans Tampon B, transfert ignoré.")
    else:
        print(f"Facture '{contenu_facture}' ignorée car son statut est '{statut_facture}'.")



# Enregistrer les changements dans Tampon B
conn_Tampon_B.commit()

# Fermer les connexions
conn_Tampon_A.close()
conn_Tampon_B.close()

print("\nTransfert des données de Tampon A vers Tampon B terminé avec succès.")

