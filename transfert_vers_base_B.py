import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import psycopg2

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

# Fonction pour générer un rapport en HTML structuré
def generer_rapport_html(factures_transferees, factures_ignorées, erreurs):
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2a7fdb; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Rapport de Transfert des Données de Tampon B vers Base B</h1>
        <h2>Résumé</h2>
        <ul>
            <li><b>Factures transférées :</b> {len(factures_transferees)}</li>
            <li><b>Factures ignorées :</b> {len(factures_ignorées)}</li>
            <li><b>Erreurs rencontrées :</b> {len(erreurs)}</li>
        </ul>

        <h2>Détails des Factures Transférées</h2>
        <table>
            <tr><th>Id Factures</th><th>Facture</th></tr>
            {''.join(f'<tr><td>{i+1}</td><td>{facture}</td></tr>' for i, facture in enumerate(factures_transferees))}
        </table>

        <h2>Factures Ignorées</h2>
        <table>
            <tr><th>Id Factures</th><th>Facture</th></tr>
            {''.join(f'<tr><td>{i+1}</td><td>{facture}</td></tr>' for i, facture in enumerate(factures_ignorées))}
        </table>

        <h2>Erreurs Rencontrées</h2>
        <ul>{''.join(f'<li>{erreur}</li>' for erreur in erreurs)}</ul>
    </body>
    </html>
    """
    return body

# Fonction de connexion à la base de données
def connecter_db(db_type, host, database, user, password):
    try:
        if db_type == 'sqlite':
            return sqlite3.connect(database)
        elif db_type == 'mysql':
            return mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
        elif db_type == 'postgresql':
            return psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
        else:
            raise ValueError("Type de base de données non pris en charge")
    except Exception as e:
        raise ConnectionError(f"Erreur de connexion : {e}")

# Détection des placeholders en fonction du type de base de données
def get_placeholder(db_type):
    return "?" if db_type == "sqlite" else "%s"

# Paramètres de connexion
db_type = 'sqlite'
host = ''
database_Tampon_B = 'tampon_B.db'
database_Base_B = 'base_B.db'
user = ''
password = ''

# Initialisation des listes pour le rapport
factures_transferees = []
factures_ignorées = []
erreurs = []

try:
    conn_Tampon_B = connecter_db(db_type, host, database_Tampon_B, user, password)
    conn_Base_B = connecter_db(db_type, host, database_Base_B, user, password)

    cursor_Tampon_B = conn_Tampon_B.cursor()
    cursor_Base_B = conn_Base_B.cursor()

    placeholder = get_placeholder(db_type)

    cursor_Tampon_B.execute(f'SELECT id, facture, date, statut FROM factures WHERE statut = {placeholder}', ("Actif",))
    factures_B = cursor_Tampon_B.fetchall()

    for facture in factures_B:
        id_facture, contenu_facture, date_facture, statut_facture = facture
        try:
            cursor_Base_B.execute(
                f'SELECT COUNT(*) FROM factures WHERE facture = {placeholder} AND date = {placeholder}',
                (contenu_facture, date_facture)
            )
            count = cursor_Base_B.fetchone()[0]

            if count == 0:
                cursor_Base_B.execute(
                    f'INSERT INTO factures (facture, date, statut) VALUES ({placeholder}, {placeholder}, {placeholder})',
                    (contenu_facture, date_facture, statut_facture)
                )
                factures_transferees.append(contenu_facture)

                cursor_Tampon_B.execute(
                    f'UPDATE factures SET statut = "Transférée" WHERE id = {placeholder}',
                    (id_facture,)
                )
            else:
                factures_ignorées.append(contenu_facture)
        except Exception as e:
            erreurs.append(f"Erreur pour la facture {contenu_facture} : {e}")

    conn_Base_B.commit()
    conn_Tampon_B.commit()
except Exception as e:
    erreurs.append(f"Erreur générale : {e}")
finally:
    if 'conn_Tampon_B' in locals():
        conn_Tampon_B.close()
    if 'conn_Base_B' in locals():
        conn_Base_B.close()

# Générer et envoyer le rapport
rapport_html = generer_rapport_html(factures_transferees, factures_ignorées, erreurs)
envoyer_email_html("Rapport de Transfert de Données", rapport_html, "vidalfandohan2001@gmail.com")

print(f"Transfert terminé : {len(factures_transferees)} factures transférées, {len(factures_ignorées)} ignorées, {len(erreurs)} erreurs.")
