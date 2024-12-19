import sqlite3
import pymysql
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fonction pour envoyer un email en HTML
def envoyer_email_html(subject, body, to_email):
    from_email = 'marcoagencys@gmail.com'
    password = 'yzmx yqkr jvwf dazi'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print(f"Email envoyé à {to_email} avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction pour générer le rapport en HTML
def generer_rapport_html(factures_transferees, factures_ignorées, erreurs):
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }}
            h1 {{ color: #2a7fdb; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #0078D7; color: white; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h1>Rapport de Transfert des Données de Base A vers Tampon A</h1>
        <p><b>Résumé :</b></p>
        <ul>
            <li><b>Factures transférées :</b> {len(factures_transferees)}</li>
            <li><b>Factures ignorées :</b> {len(factures_ignorées)}</li>
            <li><b>Erreurs rencontrées :</b> {len(erreurs)}</li>
        </ul>

        <h2>Factures Transférées</h2>
        <table>
            <tr><th>Numéro de Facture</th></tr>
            {''.join(f'<tr><td>{facture}</td></tr>' for facture in factures_transferees)}
        </table>

        <h2>Factures Ignorées</h2>
        <table>
            <tr><th>Numéro de Facture</th></tr>
            {''.join(f'<tr><td>{facture}</td></tr>' for facture in factures_ignorées)}
        </table>

        <h2>Erreurs Rencontrées</h2>
        <table>
            <tr><th>Erreur</th></tr>
            {''.join(f'<tr><td>{erreur}</td></tr>' for erreur in erreurs)}
        </table>
    </body>
    </html>
    """
    return body

# Fonction pour se connecter à une base de données
def connecter_bd(db_type, host, database, user, password):
    try:
        if db_type == "sqlite":
            return sqlite3.connect(database)
        elif db_type == "mysql":
            return pymysql.connect(host=host, user=user, password=password, database=database)
        elif db_type == "postgresql":
            return psycopg2.connect(host=host, user=user, password=password, dbname=database)
        else:
            raise ValueError("Type de base de données non pris en charge.")
    except Exception as e:
        raise ConnectionError(f"Erreur de connexion à la base de données : {e}")

# Gestion des placeholders selon le type de base de données
def get_placeholder(db_type):
    return "?" if db_type == "sqlite" else "%s"

# Paramètres de connexion
params_A = {"db_type": "sqlite", "host": "", "database": "base_A.db", "user": "", "password": ""}
params_Tampon_A = {"db_type": "sqlite", "host": "", "database": "tampon_A.db", "user": "", "password": ""}

# Connexion aux bases
conn_A = connecter_bd(**params_A)
conn_Tampon_A = connecter_bd(**params_Tampon_A)

cursor_A = conn_A.cursor()
cursor_Tampon_A = conn_Tampon_A.cursor()

placeholder_A = get_placeholder(params_A["db_type"])
placeholder_Tampon_A = get_placeholder(params_Tampon_A["db_type"])

# Récupérer les données de la base principale A
query_select_A = f'SELECT id, facture, date, statut FROM factures'
cursor_A.execute(query_select_A)
factures_A = cursor_A.fetchall()

factures_transferees = []
factures_ignorées = []
erreurs = []

# Transfert des données de la base A vers Tampon A
for facture in factures_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    try:
        if statut_facture == "Actif":
            query_check_Tampon_A = f'SELECT COUNT(*) FROM factures WHERE facture = {placeholder_Tampon_A} AND date = {placeholder_Tampon_A}'
            cursor_Tampon_A.execute(query_check_Tampon_A, (contenu_facture, date_facture))
            count = cursor_Tampon_A.fetchone()[0]

            if count == 0:
                query_insert_Tampon_A = f'INSERT INTO factures (facture, date, statut) VALUES ({placeholder_Tampon_A}, {placeholder_Tampon_A}, {placeholder_Tampon_A})'
                cursor_Tampon_A.execute(query_insert_Tampon_A, (contenu_facture, date_facture, statut_facture))
                factures_transferees.append(contenu_facture)
            else:
                factures_ignorées.append(contenu_facture)
        else:
            factures_ignorées.append(contenu_facture)
    except Exception as e:
        erreurs.append(f"Erreur pour la facture {contenu_facture} : {e}")

# Enregistrer les changements
conn_Tampon_A.commit()

# Fermer les connexions
conn_A.close()
conn_Tampon_A.close()

# Générer le rapport HTML
rapport_html = generer_rapport_html(factures_transferees, factures_ignorées, erreurs)

# Envoi de l'email avec le rapport HTML
sujet_email = "Rapport de Transfert de Données"
destinataire_email = "vidalfandohan2001@gmail.com"
envoyer_email_html(sujet_email, rapport_html, destinataire_email)

print(f"Transfert terminé : {len(factures_transferees)} factures transférées, {len(factures_ignorées)} ignorées, {len(erreurs)} erreurs.")
