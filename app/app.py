import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_cors import CORS

from models import db, AdminUser, Artikel, Kunde, Bestellung, Lieferung, Lieferant, Mitarbeiter, Bestellposition
from routes.artikel import artikel_bp
from routes.kunden import kunden_bp
from routes.bestellungen import bestellungen_bp
from routes.lieferungen import lieferungen_bp

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://emma:emmapasswort@db/tanteemma"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tante-emma-dev")

db.init_app(app)

app.register_blueprint(artikel_bp)
app.register_blueprint(kunden_bp)
app.register_blueprint(bestellungen_bp)
app.register_blueprint(lieferungen_bp)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_admin:
            session["user_id"] = user.id
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Login fehlgeschlagen")

    return render_template("admin_login.html")


@app.route("/admin")
@admin_required
def admin_dashboard():
    artikel_anzahl = Artikel.query.count()
    kunden_anzahl = Kunde.query.count()
    bestellungen_anzahl = Bestellung.query.count()
    lieferungen_anzahl = Lieferung.query.count()

    letzte_bestellungen = Bestellung.query.order_by(Bestellung.BestellungID.desc()).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        artikel_anzahl=artikel_anzahl,
        kunden_anzahl=kunden_anzahl,
        bestellungen_anzahl=bestellungen_anzahl,
        lieferungen_anzahl=lieferungen_anzahl,
        letzte_bestellungen=letzte_bestellungen
    )


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tabellen erstellt!")

        if Lieferant.query.count() == 0:
            from seed import seed_daten
            seed_daten()
            print("Testdaten eingefügt!")

        admin = AdminUser.query.filter_by(username="admin").first()
        if not admin:
            admin = AdminUser(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Admin-User erstellt: admin / admin123")

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)