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

# Fonction pour générer le rapport en HTML
def generer_rapport_html(factures_transferees, factures_ignorées, factures_absentes_dans_Tampon_B):
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2a7fdb; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Rapport de Transfert des Données de Tampon A vers Tampon B</h1>
        <p>Voici un rapport détaillé sur le transfert des données de Tampon A vers Tampon B :</p>

        <h2>Résumé</h2>
        <ul>
            <li><b>Factures Transférées :</b> {len(factures_transferees)}</li>
            <li><b>Factures Ignorées :</b> {len(factures_ignorées)}</li>
            <li><b>Factures Absentes dans Tampon B :</b> {len(factures_absentes_dans_Tampon_B)}</li>
        </ul>

        <h2>Factures Transférées</h2>
        <table>
            <tr><th>Facture</th><th>Status</th></tr>"""
    
    for facture in factures_transferees:
        body += f"<tr><td>{facture}</td><td>Actif</td></tr>"

    body += """
        </table>

        <h2>Factures Ignorées</h2>
        <table>
            <tr><th>Facture</th><th>Status</th></tr>"""
    
    for facture in factures_ignorées:
        body += f"<tr><td>{facture}</td><td>Ignorée</td></tr>"

    body += """
        </table>

        <h2>Factures Absentes dans Tampon B</h2>
        <table>
            <tr><th>Facture</th></tr>"""
    
    for facture in factures_absentes_dans_Tampon_B:
        body += f"<tr><td>{facture}</td></tr>"

    body += """
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

# Obtenir le placeholder spécifique à la base de données
def get_placeholder(db_type):
    if db_type == "sqlite":
        return "?"
    elif db_type in ["mysql", "postgresql"]:
        return "%s"
    else:
        raise ValueError("Type de base de données non pris en charge.")

# Paramètres de connexion
params_A = {"db_type": "sqlite", "host": "", "database": "tampon_A.db", "user": "", "password": ""}
params_B = {"db_type": "sqlite", "host": "", "database": "tampon_B.db", "user": "", "password": ""}

# Connexion aux bases de données
conn_Tampon_A = connecter_bd(**params_A)
conn_Tampon_B = connecter_bd(**params_B)

cursor_Tampon_A = conn_Tampon_A.cursor()
cursor_Tampon_B = conn_Tampon_B.cursor()

placeholder_A = get_placeholder(params_A["db_type"])
placeholder_B = get_placeholder(params_B["db_type"])

# Récupérer les données de Tampon A
cursor_Tampon_A.execute(f'SELECT id, facture, date, statut FROM factures')
factures_A = cursor_Tampon_A.fetchall()

# Liste pour suivre les résultats du transfert
factures_transferees = []
factures_ignorées = []
factures_absentes_dans_Tampon_B = []

# Transfert des données de Tampon A vers Tampon B
for facture in factures_A:
    id_facture, contenu_facture, date_facture, statut_facture = facture

    if statut_facture == "Actif":
        # Vérification si la facture existe déjà dans Tampon B
        cursor_Tampon_B.execute(f'''
            SELECT COUNT(*) FROM factures WHERE facture = {placeholder_B} AND date = {placeholder_B}
        ''', (contenu_facture, date_facture))
        count = cursor_Tampon_B.fetchone()[0]

        if count == 0:
            # Si la facture n'existe pas, on l'insère dans Tampon B
            cursor_Tampon_B.execute(f'''
                INSERT INTO factures (facture, date, statut) 
                VALUES ({placeholder_B}, {placeholder_B}, {placeholder_B})
            ''', (contenu_facture, date_facture, statut_facture))
            factures_transferees.append(contenu_facture)
        else:
            factures_ignorées.append(contenu_facture)
    else:
        factures_ignorées.append(contenu_facture)

# Enregistrer les changements dans Tampon B
conn_Tampon_B.commit()

# Fermer les connexions
conn_Tampon_A.close()
conn_Tampon_B.close()

print("\nTransfert des données de Tampon A vers Tampon B terminé avec succès.")

# Générer le rapport HTML
rapport_html = generer_rapport_html(factures_transferees, factures_ignorées, factures_absentes_dans_Tampon_B)

# Envoi de l'email avec le rapport HTML
sujet_email = "Rapport de Transfert de Données"
destinataire_email = "vidalfandohan2001@gmail.com"
envoyer_email_html(sujet_email, rapport_html, destinataire_email)
