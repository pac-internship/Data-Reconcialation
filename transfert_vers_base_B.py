import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Liste pour suivre les résultats du transfert
resultats_transfert = []

# Transfert des données de Tampon B vers la base B après vérification du statut 
for facture in factures_Tampon_B:
    id_facture, contenu_facture, date_facture, statut_facture = facture

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
            resultats_transfert.append(
                f"Facture '{contenu_facture}' transférée avec succès vers la base principale B."
            )
        else:
            resultats_transfert.append(
                f"Facture '{contenu_facture}' déjà présente dans la base principale B, transfert ignoré."
            )
    else:
        resultats_transfert.append(
            f"Facture '{contenu_facture}' ignorée car son statut est '{statut_facture}'."
        )       

# Enregistrer les changements dans la base principale B
conn_B.commit()

# Fermer les connexions
conn_Tampon_B.close()
conn_B.close()

print("\nTransfert des données de Tampon B vers la base principale B terminé avec succès.")

#  Envoi du rapport par mail 
sujet_email = "Rapport de transfert : Tampon B vers Base principale B"
corps_email = "\n".join(resultats_transfert)
destinataire_email = "vidalfandohan2001@gmail.com"  

envoyer_email(sujet_email, corps_email, destinataire_email)
