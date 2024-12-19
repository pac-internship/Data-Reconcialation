import sqlite3
import mysql.connector
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fonction pour envoyer un email en HTML
def envoyer_email_html(subject, body, to_email):
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

    # Corps du message en HTML
    msg.attach(MIMEText(body, 'html'))

    # Envoyer l'email
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

    print(f"Email envoyé à {to_email} avec succès.")

# Fonction pour générer le rapport en HTML
def generer_rapport_html(factures_inserrees, erreurs_insertion, factures_ignorées):
    body = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2a7fdb; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Rapport d'Insertion des Données</h1>
        <p>Voici un rapport détaillé sur l'insertion des données :</p>

        <h2>Factures Insérées</h2>
        <table>
            <tr><th>Facture</th><th>Status</th></tr>"""
    
    for facture in factures_inserrees:
        body += f"<tr><td>{facture}</td><td>Insérées avec succès</td></tr>"

    body += """
        </table>

        <h2>Erreurs d'Insertion</h2>
        <table>
            <tr><th>Facture</th><th>Erreur</th></tr>"""
    
    for facture, erreur in erreurs_insertion:
        body += f"<tr><td>{facture}</td><td>{erreur}</td></tr>"

    body += """
        </table>

        <h2>Factures Ignorées (Déjà Présentes)</h2>
        <table>
            <tr><th>Facture</th><th>Status</th></tr>"""
    
    for facture in factures_ignorées:
        body += f"<tr><td>{facture}</td><td>Déjà présente dans la base</td></tr>"

    body += """
        </table>
    </body>
    </html>
    """
    
    return body

# Configuration des bases de données
configs = {
    'sqlite': {
        'type': 'sqlite',
        'path': 'C:/Users/HP/Documents/base_A.db'
    },
    'mysql': {
        'type': 'mysql',
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'base_A'
    },
    'postgresql': {
        'type': 'postgresql',
        'host': 'localhost',
        'user': 'postgres',
        'password': 'password',
        'database': 'base_A'
    }
}

# Connexion à la base de données
config = configs['sqlite']  # Remplacer par 'mysql' ou 'postgresql' si nécessaire

if config['type'] == 'sqlite':
    conn = sqlite3.connect(config['path'])
    placeholder = "?"  # SQLite utilise "?"
elif config['type'] == 'mysql':
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    placeholder = "%s"  # MySQL utilise "%s"
elif config['type'] == 'postgresql':
    conn = psycopg2.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    placeholder = "%s"  # PostgreSQL utilise "%s"

cursor = conn.cursor()

# Liste des factures à insérer
factures_a_inserer = [
    ('Facture 1', '2024-12-07', 'Actif'),
    ('Facture 2', '2024-12-07', 'Actif'),
    ('Facture 3', '2024-12-07', 'Actif'),
    ('Facture 4', '2024-12-07', 'Actif'),
    ('Facture 5', '2024-12-07', 'Actif'),
    ('Facture 6', '2024-12-07', 'Actif'),
    ('Facture 7', '2024-12-07', 'Actif'),
    ('Facture 8', '2024-12-07', 'Actif'),
    ('Facture 9', '2024-12-07', 'Inactif'),
    ('Facture 10', '2024-12-07', 'Inactif')
]

# Listes pour les résultats d'insertion
factures_inserrees = []
erreurs_insertion = []
factures_ignorées = []

# Insertion des factures
def inserer_factures():
    for facture in factures_a_inserer:
        contenu_facture, date_facture, statut_facture = facture

        # Vérifier si la facture existe déjà
        query_check = f'SELECT COUNT(*) FROM factures WHERE facture = {placeholder} AND date = {placeholder}'
        cursor.execute(query_check, (contenu_facture, date_facture))
        count = cursor.fetchone()[0]

        if count == 0:
            try:
                query_insert = f'INSERT INTO factures (facture, date, statut) VALUES ({placeholder}, {placeholder}, {placeholder})'
                cursor.execute(query_insert, (contenu_facture, date_facture, statut_facture))
                factures_inserrees.append(contenu_facture)
            except Exception as e:
                erreurs_insertion.append((contenu_facture, str(e)))
        else:
            factures_ignorées.append(contenu_facture)

    conn.commit()

# Exécution de l'insertion
inserer_factures()

# Résumé
print(f"Factures insérées : {len(factures_inserrees)}")
print(f"Factures ignorées : {len(factures_ignorées)}")
print(f"Erreurs : {len(erreurs_insertion)}")

# Générer et envoyer le rapport
rapport_html = generer_rapport_html(factures_inserrees, erreurs_insertion, factures_ignorées)
envoyer_email_html("Rapport d'Insertion", rapport_html, "vidalfandohan2001@gmail.com")

# Fermer la connexion
conn.close()
