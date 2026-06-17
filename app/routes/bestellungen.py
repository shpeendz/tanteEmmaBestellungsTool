import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Bestellung, db

bestellungen_bp = Blueprint("bestellungen", __name__)


def bestellung_to_dict(b):
    return {
        "id": b.BestellungID,
        "kunde_id": b.KundeID,
        "bestelldatum": str(b.Bestelldatum) if b.Bestelldatum else None,
        "status": b.Status,
        "wunschtermin": str(b.Wunschtermin) if b.Wunschtermin else None,
        "mitarbeiter_id": b.MitarbeiterID
    }


def create_bestellung_from_json(data):
    return Bestellung(
        KundeID=int(data["kunde_id"]),
        Status=data.get("status", "offen"),
        Wunschtermin=data.get("wunschtermin"),
        MitarbeiterID=int(data["mitarbeiter_id"]) if data.get("mitarbeiter_id") is not None else None
    )


@bestellungen_bp.route("/api/bestellungen", methods=["GET"])
def get_bestellungen():
    bestellungen = Bestellung.query.all()
    return jsonify([bestellung_to_dict(b) for b in bestellungen]), 200


@bestellungen_bp.route("/api/bestellungen/<int:bestellung_id>", methods=["GET"])
def get_bestellung(bestellung_id):
    bestellung = Bestellung.query.get(bestellung_id)

    if bestellung is None:
        return jsonify({"error": "Bestellung nicht gefunden"}), 404

    return jsonify(bestellung_to_dict(bestellung)), 200


@bestellungen_bp.route("/api/bestellungen", methods=["POST"])
def create_bestellung():
    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    if "kunde_id" not in data:
        return jsonify({"error": "Pflichtfeld: kunde_id"}), 400

    try:
        neue_bestellung = create_bestellung_from_json(data)
        db.session.add(neue_bestellung)
        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "kunde_id oder mitarbeiter_id müssen Zahlen sein"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Bestellung konnte nicht gespeichert werden"}), 500

    return jsonify(bestellung_to_dict(neue_bestellung)), 201


@bestellungen_bp.route("/api/bestellungen/<int:bestellung_id>", methods=["PUT"])
def update_bestellung(bestellung_id):
    bestellung = Bestellung.query.get(bestellung_id)

    if bestellung is None:
        return jsonify({"error": "Bestellung nicht gefunden"}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    try:
        if "kunde_id" in data:
            bestellung.KundeID = int(data["kunde_id"])

        if "status" in data:
            bestellung.Status = data["status"]

        if "wunschtermin" in data:
            bestellung.Wunschtermin = data["wunschtermin"]

        if "mitarbeiter_id" in data:
            bestellung.MitarbeiterID = int(data["mitarbeiter_id"]) if data["mitarbeiter_id"] is not None else None

        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "kunde_id oder mitarbeiter_id müssen Zahlen sein"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Bestellung konnte nicht aktualisiert werden"}), 500

    return jsonify(bestellung_to_dict(bestellung)), 200


@bestellungen_bp.route("/api/bestellungen/<int:bestellung_id>", methods=["DELETE"])
def delete_bestellung(bestellung_id):
    bestellung = Bestellung.query.get(bestellung_id)

    if bestellung is None:
        return jsonify({"error": "Bestellung nicht gefunden"}), 404

    try:
        db.session.delete(bestellung)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Bestellung konnte nicht gelöscht werden"}), 500

    return jsonify({"message": "Bestellung gelöscht"}), 200