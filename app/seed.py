from app import app
from models import *
from datetime import datetime, date

with app.app_context ():
    from app import app
    from models import db, Lieferant, Mitarbeiter, Kunde, Artikel, Bestellung, Bestellposition, Lieferung
    from datetime import datetime, date

    with app.app_context():
        # Alte Daten löschen (Reihenfolge wichtig!)
        Lieferung.query.delete()
        Bestellposition.query.delete()
        Bestellung.query.delete()
        Artikel.query.delete()
        Kunde.query.delete()
        Mitarbeiter.query.delete()
        Lieferant.query.delete()

        # 1. Lieferanten
        l1 = Lieferant(Firmenname='FrischWare GmbH', Kontakt='Hans Müller', Email='hans@frischware.de',
                       Telefon='0221-111222')
        l2 = Lieferant(Firmenname='BioKiste AG', Kontakt='Anna Bauer', Email='anna@biokiste.de', Telefon='0211-333444')
        db.session.add_all([l1, l2])
        db.session.flush()  # IDs vergeben

        # 2. Mitarbeiter
        m1 = Mitarbeiter(Vorname='Maria', Nachname='Schmidt', Rolle='Verkauf', Email='maria@tante-emma.de')
        m2 = Mitarbeiter(Vorname='Klaus', Nachname='Wagner', Rolle='Lager', Email='klaus@tante-emma.de')
        db.session.add_all([m1, m2])
        db.session.flush()

        # 3. Kunden
        k1 = Kunde(Vorname='Peter', Nachname='Müller', Email='peter@mail.de', Telefon='0177-111222',
                   Adresse='Hauptstr. 1, Köln')
        k2 = Kunde(Vorname='Lisa', Nachname='Koch', Email='lisa@mail.de', Telefon='0178-333444',
                   Adresse='Nebenstr. 5, Köln')
        db.session.add_all([k1, k2])
        db.session.flush()

        # 4. Artikel
        a1 = Artikel(Bezeichnung='Äpfel 1kg', Preis=1.99, Bestand=50, Kategorie='Obst', LieferantID=l1.LieferantID)
        a2 = Artikel(Bezeichnung='Vollmilch 1L', Preis=0.99, Bestand=80, Kategorie='Milch', LieferantID=l1.LieferantID)
        a3 = Artikel(Bezeichnung='Bio-Eier 10 Stk', Preis=3.79, Bestand=25, Kategorie='Bio', LieferantID=l2.LieferantID)
        db.session.add_all([a1, a2, a3])
        db.session.flush()

        # 5. Bestellung
        b1 = Bestellung(KundeID=k1.KundeID, Status='offen', Wunschtermin=date(2026, 6, 10),
                        MitarbeiterID=m1.MitarbeiterID)
        db.session.add(b1)
        db.session.flush()

        # 6. Bestellpositionen
        bp1 = Bestellposition(BestellungID=b1.BestellungID, ArtikelID=a1.ArtikelID, Menge=3, Einzelpreis=a1.Preis)
        bp2 = Bestellposition(BestellungID=b1.BestellungID, ArtikelID=a2.ArtikelID, Menge=2, Einzelpreis=a2.Preis)
        db.session.add_all([bp1, bp2])
        db.session.flush()

        # 7. Lieferung
        lf1 = Lieferung(BestellungID=b1.BestellungID, MitarbeiterID=m2.MitarbeiterID,
                        Lieferdatum=datetime(2026, 6, 10, 10, 0), Status='geplant')
        db.session.add(lf1)

        # Alles speichern
        db.session.commit()
        print('Testdaten erfolgreich eingefügt!')

