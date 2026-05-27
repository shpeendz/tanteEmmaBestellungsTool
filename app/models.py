from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lieferant(db.Model):
    __tablename__ = 'Lieferant'
    LieferantID   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firmenname    = db.Column(db.String(100), nullable=False)
    Kontakt       = db.Column(db.String(100))
    Email         = db.Column(db.String(100))
    Telefon       = db.Column(db.String(20))
    artikel       = db.relationship('Artikel', backref='lieferant', lazy=True)

class Mitarbeiter(db.Model):
    __tablename__ = 'Mitarbeiter'
    MitarbeiterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vorname       = db.Column(db.String(50), nullable=False)
    Nachname      = db.Column(db.String(50), nullable=False)
    Rolle         = db.Column(db.String(50))
    Email         = db.Column(db.String(100))

class Kunde(db.Model):
    __tablename__ = 'Kunde'
    KundeID    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vorname    = db.Column(db.String(50), nullable=False)
    Nachname   = db.Column(db.String(50), nullable=False)
    Email      = db.Column(db.String(100), unique=True, nullable=False)
    Telefon    = db.Column(db.String(20))
    Adresse    = db.Column(db.String(200))
    bestellungen = db.relationship('Bestellung', backref='kunde', lazy=True)

class Artikel(db.Model):
    __tablename__ = 'Artikel'
    ArtikelID   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Bezeichnung = db.Column(db.String(100), nullable=False)
    Preis       = db.Column(db.Numeric(10, 2), nullable=False)
    Bestand     = db.Column(db.Integer, default=0)
    Kategorie   = db.Column(db.String(50))
    LieferantID = db.Column(db.Integer, db.ForeignKey('Lieferant.LieferantID'))

class Bestellung(db.Model):
    __tablename__ = 'Bestellung'
    BestellungID  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    KundeID       = db.Column(db.Integer, db.ForeignKey('Kunde.KundeID'), nullable=False)
    Bestelldatum  = db.Column(db.DateTime, default=db.func.now())
    Status        = db.Column(db.String(30), default='offen')
    Wunschtermin  = db.Column(db.Date)
    MitarbeiterID = db.Column(db.Integer, db.ForeignKey('Mitarbeiter.MitarbeiterID'))
    positionen    = db.relationship('Bestellposition', backref='bestellung', lazy=True)
    mitarbeiter   = db.relationship('Mitarbeiter', backref='bestellungen')

class Bestellposition(db.Model):
    __tablename__ = 'Bestellposition'
    PositionID   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BestellungID = db.Column(db.Integer, db.ForeignKey('Bestellung.BestellungID'), nullable=False)
    ArtikelID    = db.Column(db.Integer, db.ForeignKey('Artikel.ArtikelID'), nullable=False)
    Menge        = db.Column(db.Integer, nullable=False)
    Einzelpreis  = db.Column(db.Numeric(10, 2), nullable=False)
    artikel      = db.relationship('Artikel')

class Lieferung(db.Model):
    __tablename__ = 'Lieferung'
    LieferungID   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BestellungID  = db.Column(db.Integer, db.ForeignKey('Bestellung.BestellungID'))
    MitarbeiterID = db.Column(db.Integer, db.ForeignKey('Mitarbeiter.MitarbeiterID'))
    Lieferdatum   = db.Column(db.DateTime)
    Status        = db.Column(db.String(30), default='geplant')
    mitarbeiter   = db.relationship('Mitarbeiter', backref='lieferungen')