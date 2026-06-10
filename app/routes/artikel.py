import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Artikel, db

artikel_bp = Blueprint('artikel', __name__)


def create_artikel_from_json(data):
    return Artikel(
        Bezeichnung=data["bezeichnung"],
        Preis=data["preis"],
        Bestand=data.get("bestand", 0),
        Kategorie=data.get("kategorie")
    )


# ← NEU: Alle Artikel abrufen
@artikel_bp.route('/api/artikel', methods=['GET'])
def get_artikel():
    artikel = Artikel.query.all()
    return jsonify([{
        'id':          a.ArtikelID,
        'bezeichnung': a.Bezeichnung,
        'preis':       float(a.Preis),
        'bestand':     a.Bestand,
        'kategorie':   a.Kategorie
    } for a in artikel])


@artikel_bp.route('/api/artikel', methods=['POST'])
def create_artikel():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    artikel = create_artikel_from_json(data)

    db.session.add(artikel)
    db.session.commit()

    return jsonify({
        "id": artikel.ArtikelID,
        "bezeichnung": artikel.Bezeichnung
    }), 201