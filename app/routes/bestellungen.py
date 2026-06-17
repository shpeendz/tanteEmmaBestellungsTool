import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Bestellung, db

bestellungen_bp = Blueprint("bestellungen", __name__)


def create_bestellung_from_json(data):
    return Bestellung(
        BestellungID=int(data["ID"]),
        KundeID=int(data["Kunde"]),
        Datum=data.get("Datum"),
        Status=data.get("Status"),
        Wunschtermin=data.get("Wunschtermin")
    )


@bestellungen_bp.route("/api/bestellungen", methods=["GET"])
def get_bestellungen():
    bestellungen = Bestellung.query.all()

    return jsonify([
        {
            "id": b.BestellungID,
            "status": b.Status,
            "kunde_id": b.KundeID
        }
        for b in bestellungen
    ])


@bestellungen_bp.route("/api/bestellungen", methods=["POST"])
def create_bestellungen():
    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    if "ID" not in data or "Kunde" not in data:
        return jsonify({"error": "Pflichtfelder: ID, Kunde"}), 400

    try:
        neue_bestellung = create_bestellung_from_json(data)
        db.session.add(neue_bestellung)
        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "ID und Kunde müssen Zahlen sein"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Bestellung konnte nicht gespeichert werden"}), 500

    return jsonify({
        "message": "Bestellung erstellt",
        "id": neue_bestellung.BestellungID
    }), 201