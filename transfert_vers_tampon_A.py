import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connexion à la base de données principale A et Tampon A
conn_A = sqlite3.connect('C:/Users/HP/Documents/base_A.db')
conn_Tampon_A = sqlite3.connect('C:/Users/HP/Documents/tampon_A.db')

# Création de curseurs
cursor_A = conn_A.cursor()
cursor_Tampon_A = conn_Tampon_A.cursor()

# Récupérer les données de la base principale A
cursor_A.execute('SELECT id, facture, date, statut FROM factures')
factures_A = cursor_A.fetchall()

# Récupérer les données de la base Tampon A
cursor_Tampon_A.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_A = cursor_Tampon_A.fetchall()

#  Vérification des factures présentes dans Base A mais absentes dans Tampon A
print("\nBase A ==> Tampon A : Données non transmises")
for facture in factures_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_Tampon_A.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_Tampon_A.fetchone()[0]
    
    if count == 0:
        print(contenu_facture)

#  Vérification des factures présentes dans Tampon A mais absentes dans la base principale A
print("\nFactures présentes dans Tampon A mais absentes dans la base principale A :")
for facture in factures_Tampon_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    
    cursor_A.execute('''
    SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?
    ''', (contenu_facture, date_facture))
    
    count = cursor_A.fetchone()[0]
    
    if count == 0:
        print(contenu_facture)

# Initialisation du compteur pour les factures avec statut "Inactif"
factures_inactives = 0
factures_inactives_details = []  # Liste pour stocker les factures "Inactif" ignorées

# Insérer les données dans la base Tampon A après vérification
for facture in factures_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    # On vérifie d'abord que le statut est "Actif"
    if statut_facture == "Actif":
        # Vérification si la facture existe déjà dans Tampon A
        cursor_Tampon_A.execute(''' 
        SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ? 
        ''', (contenu_facture, date_facture))
        
        count = cursor_Tampon_A.fetchone()[0]

        if count == 0:
            # Si la facture n'existe pas, on l'insère avec le statut "Actif"
            cursor_Tampon_A.execute(''' 
            INSERT INTO factures (facture, date, statut) 
            VALUES (?, ?, ?) 
            ''', (contenu_facture, date_facture, statut_facture))
            print(f"Facture '{contenu_facture}' avec statut '{statut_facture}' transférée vers Tampon A.")
        else:
            print(f"Facture '{contenu_facture}' déjà présente dans Tampon A, transfert ignoré.")
    else:
        # Incrémenter le compteur pour les factures "Inactif" et stocker les détails
        factures_inactives += 1
        factures_inactives_details.append(contenu_facture)

# Affichage du nombre total de factures "Inactif" non transférées
print(f"\nNombre total de factures non transférées en raison du statut 'Inactif' : {factures_inactives}")

# Affichage des détails des factures "Inactif" ignorées
for details in factures_inactives_details:
    print(details)

# Enregistrer les changements dans Tampon A
conn_Tampon_A.commit()

# Fermer les connexions
conn_A.close()
conn_Tampon_A.close()

print("Transfert des données de A vers Tampon A terminé avec succès.")

# Fonction pour envoyer un email
def envoyer_email(subject, body, to_email):
    from_email = 'marcoagencys@gmail.com'
    password = 'yzmx yqkr jvwf dazi'

    # Configurer le serveur SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    # Construire l'email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Envoyer l'email
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

    print(f"Email envoyé à {to_email} avec succès.")

#  Envoyer un email avec les détails du transfert
subject = "Rapport de transfert vers Tampon A"
body = f"""
Le transfert des données de la base A vers Tampon A a été éffectué avec succès.

Nombre total de factures transférées : {len(factures_A) - factures_inactives}
Nombre de factures ignorées (statut 'Inactif') : {factures_inactives}

"""
to_email = "vidalfandohan2001@gmail.com"
envoyer_email(subject, body, to_email)
