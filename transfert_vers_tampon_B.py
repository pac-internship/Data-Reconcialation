import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connexion aux bases de données Tampon A et Tampon B
conn_Tampon_A = sqlite3.connect('C:/Users/HP/Documents/tampon_A.db')
conn_Tampon_B = sqlite3.connect('C:/Users/HP/Documents/tampon_B.db')

# Création de curseurs
cursor_Tampon_A = conn_Tampon_A.cursor()
cursor_Tampon_B = conn_Tampon_B.cursor()

# Variables pour le rapport d'email
factures_transferees = []
factures_ignorées = []
factures_absentes_dans_Tampon_A = []
factures_absentes_dans_Tampon_B = []

# Récupérer les données de la base Tampon A
cursor_Tampon_A.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_A = cursor_Tampon_A.fetchall()

# Récupérer les données de la base Tampon B
cursor_Tampon_B.execute('SELECT id, facture, date, statut FROM factures')
factures_Tampon_B = cursor_Tampon_B.fetchall()

# Vérification des factures présentes dans Tampon A mais absentes dans Tampon B
for facture in factures_Tampon_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    cursor_Tampon_B.execute('''SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?''', (contenu_facture, date_facture))
    count = cursor_Tampon_B.fetchone()[0]
    
    if count == 0:
        factures_absentes_dans_Tampon_B.append(contenu_facture)

# Vérification des factures présentes dans Tampon B mais absentes dans Tampon A
for facture in factures_Tampon_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture
    cursor_Tampon_A.execute('''SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?''', (contenu_facture, date_facture))
    count = cursor_Tampon_A.fetchone()[0]
    
    if count == 0:
        factures_absentes_dans_Tampon_A.append(f"Facture '{contenu_facture}' avec la date '{date_facture}' n'est pas dans la base Tampon A.")

# Insérer les données dans la base Tampon B après vérification du statut
for facture in factures_Tampon_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    # On vérifie d'abord que le statut est "Actif"
    if statut_facture == "Actif":
        # Vérification si la facture existe déjà dans Tampon B
        cursor_Tampon_B.execute('''SELECT COUNT(*) FROM factures WHERE facture = ? AND date = ?''', (contenu_facture, date_facture))
        count = cursor_Tampon_B.fetchone()[0]

        if count == 0:
            # Si la facture n'existe pas, on l'insère avec le statut "Actif"
            cursor_Tampon_B.execute('''INSERT INTO factures (facture, date, statut) VALUES (?, ?, ?)''', (contenu_facture, date_facture, statut_facture))
            factures_transferees.append(f"Facture '{contenu_facture}' transférée vers Tampon B avec statut '{statut_facture}'.")
        else:
            factures_ignorées.append(f"Facture '{contenu_facture}' déjà présente dans Tampon B, transfert ignoré.")
    else:
        factures_ignorées.append(f"Facture '{contenu_facture}' ignorée car son statut est '{statut_facture}'.")

# Enregistrer les changements dans Tampon B
conn_Tampon_B.commit()

# Fermer les connexions
conn_Tampon_A.close()
conn_Tampon_B.close()

print("\nTransfert des données de Tampon A vers Tampon B terminé avec succès.")

# Fonction d'envoi de mail
def envoyer_email(subject, body, to_email):
    # Configuration des informations d'authentification
    from_email = 'marcoagencys@gmail.com'  
    password = 'yzmx yqkr jvwf dazi'          

    # Configurer le serveur SMTP 
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Port 587 pour STARTTLS
    server.starttls()  # Démarrer une connexion sécurisée
    server.login(from_email, password)  # Authentification

    # Construire l'email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject  # Sujet de l'email

    # Construire le corps du message avec le rapport détaillé
    body = "Rapport sur le transfert des données de Tampon A vers Tampon B :\n\n"
    
    # Factures transférées
    body += "Factures transférées :\n"
    for facture in factures_transferees:
        body += f"- {facture}\n"
    
    # Factures ignorées
    body += "\nFactures ignorées :\n"
    for facture in factures_ignorées:
        body += f"- {facture}\n"

    # Factures absentes dans Tampon A
    body += "\nFactures absentes dans Tampon A :\n"
    for facture in factures_absentes_dans_Tampon_A:
        body += f"- {facture}\n"

    # Factures absentes dans Tampon B
    body += "\nFactures absentes dans Tampon B :\n"
    for facture in factures_absentes_dans_Tampon_B:
        body += f"- {facture}\n"

    msg.attach(MIMEText(body, 'plain'))  # Contenu du message (texte brut)

    # Envoyer l'email
    server.sendmail(from_email, to_email, msg.as_string())
    
    # Fermer la connexion au serveur SMTP
    server.quit()

    print(f"Email envoyé à {to_email} avec succès.")

# Appel de la fonction d'envoi de mail avec les détails du rapport
subject = "Rapport de transfert de données Tampon A vers Tampon B"
to_email = "vidalfandohan2001@gmail.com"  
envoyer_email(subject, "", to_email)
