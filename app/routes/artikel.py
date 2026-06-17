import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Artikel, db

artikel_bp = Blueprint('artikel', __name__)


def create_artikel_from_json(data):
    return Artikel(
        Bezeichnung=data["bezeichnung"].strip(),
        Preis=float(data["preis"]),
        Bestand=int(data.get("bestand", 0)),
        Kategorie=data.get("kategorie")
    )


@artikel_bp.route('/api/artikel', methods=['GET'])
def get_artikel():
    artikel = Artikel.query.all()
    return jsonify([{
        'id': a.ArtikelID,
        'bezeichnung': a.Bezeichnung,
        'preis': float(a.Preis),
        'bestand': a.Bestand,
        'kategorie': a.Kategorie
    } for a in artikel])


@artikel_bp.route('/api/artikel', methods=['POST'])
def create_artikel():
    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    if "bezeichnung" not in data or "preis" not in data:
        return jsonify({"error": "Pflichtfelder: bezeichnung, preis"}), 400

    if not str(data["bezeichnung"]).strip():
        return jsonify({"error": "Bezeichnung darf nicht leer sein"}), 400

    try:
        artikel = create_artikel_from_json(data)
        db.session.add(artikel)
        db.session.commit()
    except ValueError:
        return jsonify({"error": "preis oder bestand hat ein ungültiges Format"}), 400

    return jsonify({
        "id": artikel.ArtikelID,
        "bezeichnung": artikel.Bezeichnung
    }), 201