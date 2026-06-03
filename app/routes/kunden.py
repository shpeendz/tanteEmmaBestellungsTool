import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, jsonify

from models import Kunde

kunden_bp = Blueprint("kunden", __name__)

@kunden_bp.route("/api/kunden", methods=["GET"])
def get_kunden():
    kunden = Kunde.query.all()

    return jsonify([
        {
            "id": k.KundeID,
            "vorname": k.Vorname,
            "nachname": k.Nachname,
            "email": k.Email,
            "telefon": k.Telefon,
            "adresse": k.Adresse
        }
        for k in kunden
    ])