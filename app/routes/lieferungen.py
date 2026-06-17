import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Lieferung, db

lieferungen_bp = Blueprint("lieferungen", __name__)


def lieferung_to_dict(l):
    return {
        "id": l.LieferungID,
        "bestellung_id": l.BestellungID,
        "mitarbeiter_id": l.MitarbeiterID,
        "lieferdatum": str(l.Lieferdatum) if l.Lieferdatum else None,
        "status": l.Status
    }


def create_lieferung_from_json(data):
    return Lieferung(
        LieferungID=int(data["id"]),
        BestellungID=int(data["bestellung_id"]),
        MitarbeiterID=int(data["mitarbeiter_id"]) if data.get("mitarbeiter_id") is not None else None,
        Lieferdatum=data.get("lieferdatum"),
        Status=data.get("status")
    )


@lieferungen_bp.route("/api/lieferungen", methods=["GET"])
def get_lieferungen():
    lieferungen = Lieferung.query.all()
    return jsonify([lieferung_to_dict(l) for l in lieferungen]), 200


@lieferungen_bp.route("/api/lieferungen/<int:lieferung_id>", methods=["GET"])
def get_lieferung(lieferung_id):
    lieferung = Lieferung.query.get(lieferung_id)

    if lieferung is None:
        return jsonify({"error": "Lieferung nicht gefunden"}), 404

    return jsonify(lieferung_to_dict(lieferung)), 200


@lieferungen_bp.route("/api/lieferungen", methods=["POST"])
def create_lieferung():
    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    if "id" not in data or "bestellung_id" not in data:
        return jsonify({"error": "Pflichtfelder: id, bestellung_id"}), 400

    try:
        neue_lieferung = create_lieferung_from_json(data)
        db.session.add(neue_lieferung)
        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "id, bestellung_id oder mitarbeiter_id müssen Zahlen sein"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Lieferung konnte nicht gespeichert werden"}), 500

    return jsonify(lieferung_to_dict(neue_lieferung)), 201


@lieferungen_bp.route("/api/lieferungen/<int:lieferung_id>", methods=["PUT"])
def update_lieferung(lieferung_id):
    lieferung = Lieferung.query.get(lieferung_id)

    if lieferung is None:
        return jsonify({"error": "Lieferung nicht gefunden"}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    try:
        if "bestellung_id" in data:
            lieferung.BestellungID = int(data["bestellung_id"])

        if "mitarbeiter_id" in data:
            lieferung.MitarbeiterID = int(data["mitarbeiter_id"]) if data["mitarbeiter_id"] is not None else None

        if "lieferdatum" in data:
            lieferung.Lieferdatum = data["lieferdatum"]

        if "status" in data:
            lieferung.Status = data["status"]

        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "bestellung_id oder mitarbeiter_id müssen Zahlen sein"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Lieferung konnte nicht aktualisiert werden"}), 500

    return jsonify(lieferung_to_dict(lieferung)), 200


@lieferungen_bp.route("/api/lieferungen/<int:lieferung_id>", methods=["DELETE"])
def delete_lieferung(lieferung_id):
    lieferung = Lieferung.query.get(lieferung_id)

    if lieferung is None:
        return jsonify({"error": "Lieferung nicht gefunden"}), 404

    try:
        db.session.delete(lieferung)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Lieferung konnte nicht gelöscht werden"}), 500

    return jsonify({"message": "Lieferung gelöscht"}), 200