import os
from flask import Flask, send_from_directory
from models import db, Lieferant
from routes.artikel import artikel_bp
from routes.kunden import kunden_bp
from routes.bestellungen import bestellungen_bp
from routes.lieferungen import lieferungen_bp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, '..', 'db', 'tante_emma.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tante-emma-dev'

db.init_app(app)

app.register_blueprint(artikel_bp)
app.register_blueprint(kunden_bp)
app.register_blueprint(bestellungen_bp)
app.register_blueprint(lieferungen_bp)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Tabellen erstellt!')
        if Lieferant.query.count() == 0:
            from seed import seed_daten
            seed_daten()
            print('Testdaten eingefügt!')
    app.run(debug=True)