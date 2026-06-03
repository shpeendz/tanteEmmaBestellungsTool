import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, jsonify, request

from models import Artikel, db

artikel_bp = Blueprint('artikel', __name__)


@artikel_bp.route('/api/artikel', methods=['GET'])
def get_artikel():
    # Schritt 1 – alle Artikel aus DB holen
    artikel = Artikel.query.all()

    # Schritt 2 – Objekte in Dictionaries umwandeln
    ergebnis = [
        {
            'id': a.ArtikelID,
            'bezeichnung': a.Bezeichnung,
            'preis': float(a.Preis),
            'bestand': a.Bestand,
            'kategorie': a.Kategorie
        }
        for a in artikel
    ]

    # Schritt 3 – als JSON zurückgeben
    return jsonify(ergebnis)

@artikel_bp.route('/api/artikel', methods=['POST'])
def create_artikel():

    # Schritt 1 – JSON aus dem Request lesen
    daten = request.get_json()

    # Schritt 2 – neues Objekt erstellen
    neuer_artikel = Artikel(
        Bezeichnung = daten['bezeichnung'],
        Preis       = daten['preis'],
        Bestand     = daten.get('bestand', 0),
        Kategorie   = daten.get('kategorie')
    )

    # Schritt 3 – in DB speichern
    db.session.add(neuer_artikel)
    db.session.commit()

    # Schritt 4 – neuen Artikel als JSON zurückgeben
    return jsonify({'id': neuer_artikel.ArtikelID, 'bezeichnung': neuer_artikel.Bezeichnung}), 201