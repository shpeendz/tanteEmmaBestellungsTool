import sys
import os
from tokenize import String

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
#
@bestellungen_bp.route("/api/bestellungen", methods=["POST"])
def create_bestellungen():

    # Schritt 1 – JSON aus dem Request lesen
    daten = request.get_json()

    # Schritt 2 – neues Objekt erstellen
    neue_bestellung = Bestellung(
        ID = daten['ID'],
        Kunde       = daten['Kunde'],
        Datum     = daten.get('Datum', 0),
        Status   = daten.get('Status'),
        Wunschtermin = daten.get('Wunschtermin')
    )
