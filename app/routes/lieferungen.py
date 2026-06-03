import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, jsonify

from models import Lieferung

lieferungen_bp = Blueprint("lieferungen", __name__)


@lieferungen_bp.route("/api/lieferungen", methods=["GET"])
def get_lieferungen():
    lieferungen = Lieferung.query.all()

    return jsonify([
        {
            "id": l.LieferungID,
            "bestellung_id": l.BestellungID,
            "mitarbeiter_id": l.MitarbeiterID,
            "lieferdatum": str(l.Lieferdatum) if l.Lieferdatum else None,
            "status": l.Status
        }
        for l in lieferungen
    ])