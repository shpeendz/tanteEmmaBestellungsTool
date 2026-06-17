import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Blueprint, jsonify, request
from models import Artikel, db

artikel_bp = Blueprint("artikel", __name__)


def artikel_to_dict(a):
    return {
        "id": a.ArtikelID,
        "bezeichnung": a.Bezeichnung,
        "preis": float(a.Preis),
        "bestand": a.Bestand,
        "kategorie": a.Kategorie,
        "lieferant_id": a.LieferantID
    }


def create_artikel_from_json(data):
    return Artikel(
        Bezeichnung=str(data["bezeichnung"]).strip(),
        Preis=float(data["preis"]),
        Bestand=int(data.get("bestand", 0)),
        Kategorie=data.get("kategorie"),
        LieferantID=int(data["lieferant_id"]) if data.get("lieferant_id") is not None else None
    )


@artikel_bp.route("/api/artikel", methods=["GET"])
def get_artikel():
    artikel = Artikel.query.all()
    return jsonify([artikel_to_dict(a) for a in artikel]), 200


@artikel_bp.route("/api/artikel/<int:artikel_id>", methods=["GET"])
def get_artikel_by_id(artikel_id):
    artikel = Artikel.query.get(artikel_id)

    if artikel is None:
        return jsonify({"error": "Artikel nicht gefunden"}), 404

    return jsonify(artikel_to_dict(artikel)), 200


@artikel_bp.route("/api/artikel", methods=["POST"])
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
        neuer_artikel = create_artikel_from_json(data)
        db.session.add(neuer_artikel)
        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "preis, bestand oder lieferant_id haben ein ungültiges Format"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Artikel konnte nicht gespeichert werden"}), 500

    return jsonify(artikel_to_dict(neuer_artikel)), 201


@artikel_bp.route("/api/artikel/<int:artikel_id>", methods=["PUT"])
def update_artikel(artikel_id):
    artikel = Artikel.query.get(artikel_id)

    if artikel is None:
        return jsonify({"error": "Artikel nicht gefunden"}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type muss application/json sein"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ungültiges JSON"}), 400

    try:
        if "bezeichnung" in data:
            if not str(data["bezeichnung"]).strip():
                return jsonify({"error": "Bezeichnung darf nicht leer sein"}), 400
            artikel.Bezeichnung = str(data["bezeichnung"]).strip()

        if "preis" in data:
            artikel.Preis = float(data["preis"])

        if "bestand" in data:
            artikel.Bestand = int(data["bestand"])

        if "kategorie" in data:
            artikel.Kategorie = data["kategorie"]

        if "lieferant_id" in data:
            artikel.LieferantID = int(data["lieferant_id"]) if data["lieferant_id"] is not None else None

        db.session.commit()
    except ValueError:
        db.session.rollback()
        return jsonify({"error": "preis, bestand oder lieferant_id haben ein ungültiges Format"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Artikel konnte nicht aktualisiert werden"}), 500

    return jsonify(artikel_to_dict(artikel)), 200


@artikel_bp.route("/api/artikel/<int:artikel_id>", methods=["DELETE"])
def delete_artikel(artikel_id):
    artikel = Artikel.query.get(artikel_id)

    if artikel is None:
        return jsonify({"error": "Artikel nicht gefunden"}), 404

    try:
        db.session.delete(artikel)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Artikel konnte nicht gelöscht werden"}), 500

    return jsonify({"message": "Artikel gelöscht"}), 200