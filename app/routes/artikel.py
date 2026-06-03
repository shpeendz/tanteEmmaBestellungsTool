import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, jsonify

from models import Artikel

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