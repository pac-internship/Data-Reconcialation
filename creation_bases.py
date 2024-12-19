import sqlite3
import mysql.connector
import psycopg2

def create_connection(db_type, db_config):
    """
    Crée une connexion à une base de données en fonction de son type et des configurations fournies.

    :param db_type: Le type de base de données ('sqlite', 'mysql', 'postgresql').
    :param db_config: Dictionnaire contenant les configurations de connexion.
    :return: Objet de connexion.
    """
    if db_type == 'sqlite':
        return sqlite3.connect(db_config['name'])
    elif db_type == 'mysql':
        return mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['name']
        )
    elif db_type == 'postgresql':
        return psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            dbname=db_config['name']
        )
    else:
        raise ValueError("Type de base de données non supporté")

# Configuration des bases de données
configs = {
    'base_A': {
        'type': 'sqlite',
        'name': 'C:/Users/HP/Documents/base_A.db'
    },
    'tampon_A': {
        'type': 'sqlite',
        'name': 'C:/Users/HP/Documents/tampon_A.db'
    },
    'base_B': {
        'type': 'sqlite',
        'name': 'C:/Users/HP/Documents/base_B.db'
    },
    'tampon_B': {
        'type': 'sqlite',
        'name': 'C:/Users/HP/Documents/tampon_B.db'
    }
}

# Remplacer par des configurations MySQL ou PostgreSQL si nécessaire
# configs['base_A'] = {
#     'type': 'mysql',
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'password',
#     'name': 'base_A'
# }

# Connexions aux bases de données
connections = {}
cursors = {}

for db_key, db_config in configs.items():
    connections[db_key] = create_connection(db_config['type'], db_config)
    cursors[db_key] = connections[db_key].cursor()

# Création des tables
create_table_query = '''
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture TEXT NOT NULL,
    date TEXT NOT NULL,
    statut TEXT NOT NULL  
)
'''

for db_key, cursor in cursors.items():
    cursor.execute(create_table_query)

# Validation et fermeture des connexions
for db_key, connection in connections.items():
    connection.commit()
    connection.close()

print("Tables créées avec succès dans toutes les bases de données.")
