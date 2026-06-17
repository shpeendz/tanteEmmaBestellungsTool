import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Kunde, db

kunden_bp = Blueprint("kunden", __name__)


def kunde_to_dict(k):
    return {
        "id": k.KundeID,
        "vorname": k.Vorname,
        "nachname": k.Nachname,
        "email": k.Email,
        "telefon": k.Telefon,
        "adresse": k.Adresse
    }


def create_kunde_from_json(data):
    return Kunde(
        Vorname=str(data["vorname"]).strip(),
        Nachname=str(data["nachname"]).strip(),
        Email=str(data["email"]).strip(),
        Telefon=data.get("telefon"),
        Adresse=data.get("adresse")
    )


@kunden_bp.route("/api/kunden", methods=["GET"])
def get_kunden():
    kunden = Kunde.query.all()
    return jsonify([kunde_to_dict(k) for k in kunden]), 200


@kunden_bp.route("/api/kunden/<int:kunden_id>", methods=["GET"])
def get_kunde(kunden_id):
    kunde = Kunde.query.get(kunden_id)

    if kunde is None:
        return jsonify({"error": "Kunde nicht gefunden"}), 404

    return jsonify(kunde_to_dict(kunde)), 200


@kunden_bp.route("/api/kunden", methods=["POST"])
def create_kunde():
    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    if "vorname" not in data or "nachname" not in data or "email" not in data:
        return jsonify({"error": "Pflichtfelder: vorname, nachname, email"}), 400

    if not str(data["vorname"]).strip() or not str(data["nachname"]).strip() or not str(data["email"]).strip():
        return jsonify({"error": "Vorname, Nachname und Email dürfen nicht leer sein"}), 400

    try:
        neuer_kunde = create_kunde_from_json(data)
        db.session.add(neuer_kunde)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Kunde konnte nicht gespeichert werden"}), 500

    return jsonify(kunde_to_dict(neuer_kunde)), 201


@kunden_bp.route("/api/kunden/<int:kunden_id>", methods=["PUT"])
def update_kunde(kunden_id):
    kunde = Kunde.query.get(kunden_id)

    if kunde is None:
        return jsonify({"error": "Kunde nicht gefunden"}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    try:
        if "vorname" in data:
            if not str(data["vorname"]).strip():
                return jsonify({"error": "Vorname darf nicht leer sein"}), 400
            kunde.Vorname = str(data["vorname"]).strip()

        if "nachname" in data:
            if not str(data["nachname"]).strip():
                return jsonify({"error": "Nachname darf nicht leer sein"}), 400
            kunde.Nachname = str(data["nachname"]).strip()

        if "email" in data:
            if not str(data["email"]).strip():
                return jsonify({"error": "Email darf nicht leer sein"}), 400
            kunde.Email = str(data["email"]).strip()

        if "telefon" in data:
            kunde.Telefon = data["telefon"]

        if "adresse" in data:
            kunde.Adresse = data["adresse"]

        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Kunde konnte nicht aktualisiert werden"}), 500

    return jsonify(kunde_to_dict(kunde)), 200


@kunden_bp.route("/api/kunden/<int:kunden_id>", methods=["DELETE"])
def delete_kunde(kunden_id):
    kunde = Kunde.query.get(kunden_id)

    if kunde is None:
        return jsonify({"error": "Kunde nicht gefunden"}), 404

    try:
        db.session.delete(kunde)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Kunde konnte nicht gelöscht werden"}), 500

    return jsonify({"message": "Kunde gelöscht"}), 200