import os
import time
import pymysql
from flask import Flask, send_from_directory
from flask_cors import CORS

from models import db, Lieferant
from routes.artikel import artikel_bp
from routes.kunden import kunden_bp
from routes.bestellungen import bestellungen_bp
from routes.lieferungen import lieferungen_bp

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# MySQL statt SQLite — kommt aus Docker Environment Variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://emma:emmapasswort@db/tanteemma'  # Fallback lokal
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'tante-emma-dev')

db.init_app(app)

# Blueprints
app.register_blueprint(artikel_bp)
app.register_blueprint(kunden_bp)
app.register_blueprint(bestellungen_bp)
app.register_blueprint(lieferungen_bp)

# Frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# Warten bis MySQL bereit ist
def wait_for_db():
    print('Warte auf MySQL...')
    retries = 30
    while retries:
        try:
            # Verbindungsparameter aus DATABASE_URL lesen
            url = app.config['SQLALCHEMY_DATABASE_URI']
            # Direkt mit pymysql testen
            conn = pymysql.connect(
                host='db',
                user=os.environ.get('MYSQL_USER', 'emma'),
                password=os.environ.get('MYSQL_PASSWORD', 'emmapasswort'),
                database=os.environ.get('MYSQL_DATABASE', 'tanteemma')
            )
            conn.close()
            print('MySQL ist bereit!')
            return
        except Exception as e:
            print(f'MySQL noch nicht bereit, warte... ({retries} Versuche übrig)')
            retries -= 1
            time.sleep(5)
    print('MySQL nicht erreichbar nach mehreren Versuchen!')


# Startup
with app.app_context():
    wait_for_db()
    db.create_all()
    print('Tabellen erstellt!')

    if Lieferant.query.count() == 0:
        from seed import seed_daten
        seed_daten()
        print('Testdaten eingefügt!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)