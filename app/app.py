import os
from flask import Flask
from models import db

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, '..', 'db', 'tante_emma.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tante-emma-dev'

db.init_app(app)

@app.route('/')
def index():
    return 'Tante Emma läuft!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Tabellen erstellt!')
    app.run(debug=True)