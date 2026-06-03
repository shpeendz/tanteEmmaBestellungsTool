import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, jsonify

from models import Bestellung

bestellungen_bp = Blueprint("bestellungen", __name__)

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