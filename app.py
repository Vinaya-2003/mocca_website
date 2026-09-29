"""
MOCCA — Men's Wear & Wedding
Flask backend

Run with:
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000
"""
import json
import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "products.json")
MESSAGES_FILE = os.path.join(BASE_DIR, "data", "messages.json")

app = Flask(__name__)

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def find_static_image(*relative_parts):
    """Look for an image at static/<relative_parts...>.<ext> for each known
    extension and return its static-relative path if found, or None.
    Lets templates render an <img> automatically the moment a file is
    dropped into the right folder with the right name."""
    base = os.path.join(app.static_folder, *relative_parts)
    for ext in IMAGE_EXTENSIONS:
        candidate = base + ext
        if os.path.exists(candidate):
            return "/".join(relative_parts) + ext
    return None


def static_exists(relative_path):
    """True if static/<relative_path> exists as-is (already has an extension,
    e.g. a path stored directly in products.json like 'products/cs-01.jpg')."""
    return os.path.exists(os.path.join(app.static_folder, relative_path))


def load_data():
    """Load the full catalog from disk."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_message(entry):
    """Append a contact-form / enquiry submission to messages.json.
    Simple file-based store — swap for a real database before production."""
    messages = []
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    messages.append(entry)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


@app.context_processor
def inject_globals():
    """Available in every template: logo_url, and aggregate rating info
    for the "reviews at the end of the page" section."""
    data = load_data()
    stores = data["stores"]
    total_reviews = sum(s.get("reviews", 0) for s in stores)
    avg_rating = round(sum(s["rating"] * max(s.get("reviews", 0), 1) for s in stores) /
                        sum(max(s.get("reviews", 0), 1) for s in stores), 1)
    return {
        "logo_url": find_static_image("images", "logo"),
        "brand": data["brand"],
        "aggregate_rating": avg_rating,
        "aggregate_reviews": total_reviews,
        "store_count": len(stores),
    }


# ---------------------------------------------------------------- pages ----

@app.route("/")
def landing():
    """Gateway page: choose MOCCA Men's Wear or MOCCA Wedding."""
    data = load_data()
    return render_template(
        "landing.html",
        menswear=data["sections"]["menswear"],
        wedding=data["sections"]["wedding"],
    )


@app.route("/menswear")
def menswear():
    data = load_data()
    section = data["sections"]["menswear"]
    for c in section["collections"]:
        for p in c["products"]:
            p["image_url"] = p["image"] if static_exists(p["image"]) else None
    return render_template("menswear.html", section=section, stores=data["stores"])


@app.route("/menswear/collections")
@app.route("/menswear/collections/<slug>")
def menswear_collection(slug=None):
    data = load_data()
    section = data["sections"]["menswear"]
    active = slug or section["collections"][0]["slug"]
    if active not in [c["slug"] for c in section["collections"]]:
        abort(404)
    for c in section["collections"]:
        for p in c["products"]:
            p["image_url"] = p["image"] if static_exists(p["image"]) else None
    return render_template("menswear_collections.html", section=section, active_slug=active)


@app.route("/wedding")
def wedding():
    data = load_data()
    section = data["sections"]["wedding"]
    for look in section["looks"]:
        look["image_url"] = look["image"] if static_exists(look["image"]) else None
    return render_template("wedding.html", section=section, stores=data["stores"])


@app.route("/stores")
def stores():
    data = load_data()
    for s in data["stores"]:
        s["image_url"] = find_static_image("images", "stores", s["id"])
    return render_template("stores.html", stores=data["stores"])


@app.route("/contact", methods=["GET", "POST"])
def contact():
    data = load_data()
    submitted = False
    if request.method == "POST":
        entry = {
            "name": request.form.get("name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "message": request.form.get("message", "").strip(),
            "store": request.form.get("store", "").strip(),
            "interest": request.form.get("interest", "").strip(),
            "submitted_at": datetime.utcnow().isoformat() + "Z",
        }
        if entry["name"] and entry["phone"]:
            save_message(entry)
            submitted = True
    return render_template("contact.html", stores=data["stores"], submitted=submitted)


# ------------------------------------------------------------------ API ----

@app.route("/api/menswear")
def api_menswear():
    data = load_data()
    return jsonify(data["sections"]["menswear"])


@app.route("/api/wedding")
def api_wedding():
    data = load_data()
    return jsonify(data["sections"]["wedding"])


@app.route("/api/stores")
def api_stores():
    data = load_data()
    return jsonify(data["stores"])


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
