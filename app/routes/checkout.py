from flask import request, jsonify

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Ungültiges JSON"}), 400

    kunde_id = data.get("kunde_id")
    artikel = data.get("artikel", [])

    if not kunde_id or not artikel:
        return jsonify({"error": "kunde_id und artikel sind erforderlich"}), 400

    kunde = Kunde.query.get(kunde_id)
    if not kunde:
        return jsonify({"error": "Kunde nicht gefunden"}), 404

    try:
        neue_bestellung = Bestellung(
            KundeID=kunde.KundeID,
            Status="Offen"
        )
        db.session.add(neue_bestellung)
        db.session.flush()

        for eintrag in artikel:
            artikel_id = int(eintrag["artikel_id"])
            menge = int(eintrag["menge"])

            db_artikel = Artikel.query.get(artikel_id)
            if not db_artikel:
                continue

            position = Bestellposition(
                BestellungID=neue_bestellung.BestellungID,
                ArtikelID=db_artikel.ArtikelID,
                Menge=menge
            )
            db.session.add(position)

        db.session.commit()

        return jsonify({
            "message": "Bestellung gespeichert",
            "bestellung_id": neue_bestellung.BestellungID
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Bestellung konnte nicht gespeichert werden"}), 500