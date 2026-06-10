import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Bestellung

bestellungen_bp = Blueprint("bestellungen", __name__)


def create_bestellung_from_json(data):
    return Bestellung(
        BestellungID=data["ID"],
        KundeID=data["Kunde"],
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
    data = request.get_json()

    neue_bestellung = create_bestellung_from_json(data)

    # Save to database
    db.session.add(neue_bestellung)
    db.session.commit()

    return jsonify({
        "message": "Bestellung erstellt",
        "id": neue_bestellung.BestellungID
    }), 201