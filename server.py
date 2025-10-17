from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from jinja2 import TemplateNotFound
import csv
import os

app = Flask(__name__)
BASE_DIR = app.root_path  # absolute path to the project folder (where this file lives)

# 1) Serve the home page on "/"
@app.route("/")
def home():
    return render_template("index.html")

# 2) Explicit route for the favicon file under /static
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

# 3) Only render real HTML templates, not arbitrary paths like favicon.ico
@app.route("/<string:page_name>")
def html_page(page_name):
    if not page_name.endswith(".html"):
        abort(404)
    try:
        return render_template(page_name)
    except TemplateNotFound:
        abort(404)

# ---- Persistence helpers ----
def write_to_file(data):
    txt_path = os.path.join(BASE_DIR, "database.txt")
    email = data.get("email", "")
    subject = data.get("subject", "")
    message = data.get("message", "")
    with open(txt_path, mode="a", encoding="utf-8") as database:
        database.write(f"\n{email},{subject},{message}")

def write_to_csv(data):
    csv_path = os.path.join(BASE_DIR, "database.csv")
    email = data.get("email", "")
    subject = data.get("subject", "")
    message = data.get("message", "")
    with open(csv_path, mode="a", newline="", encoding="utf-8") as database2:
        csv_writer = csv.writer(database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

# ---- Contact form handler ----
@app.route("/submit_form", methods=["POST"])
def submit_form():
    try:
        data = request.form.to_dict()
        # minimal validation
        if not data.get("email") or not data.get("message"):
            return "Email and message are required.", 400
        write_to_csv(data)
        # redirect to your existing wildcard template route
        return redirect(url_for("html_page", page_name="thankyou.html"))
    except Exception:
        return "Did not save to database", 500

# ---- Project pages ----
PROJECTS = {
    "datacom": {
        "title": "DATACOM — Web Portal & Android App",
        "hero": "assets/images/work001-01.jpg",
        "images": ["assets/images/work001-02.jpg", "assets/images/work001-03.jpg", "assets/images/work001-04.jpg"],
        "summary": "Backend with Python/FastAPI, web portal, Android app, and automations.",
        "role": "Python & Android Developer",
    },
    "printify": {
        "title": "Printify — Automations & API",
        "hero": "assets/images/work001-01.jpg",
        "images": ["assets/images/work001-02.jpg", "assets/images/work001-03.jpg", "assets/images/work001-04.jpg"],
        "summary": "Shipping & tracking setup, REST integrations (Postman), logic & data analysis.",
        "role": "Automations Engineer",
    },
    "dynatech": {
        "title": "Dynatech — Web Components & SEO",
        "hero": "assets/images/work001-01.jpg",
        "images": ["assets/images/work001-02.jpg", "assets/images/work001-03.jpg", "assets/images/work001-04.jpg"],
        "summary": "Reusable components, gamification module, analytics & SEO improvements.",
        "role": "Web Developer",
    },
}

@app.route("/work/<slug>")
def work(slug):
    """
    Prefer static per-project templates if they exist:
      templates/work-<slug>.html
    Otherwise, fall back to a single dynamic template 'work.html' with project data.
    """
    # Try work-<slug>.html first (since you created those)
    specific_template = f"work-{slug}.html"
    try:
        return render_template(specific_template)
    except TemplateNotFound:
        pass

    # Fallback: dynamic single-template approach (work.html) if present
    p = PROJECTS.get(slug)
    if not p:
        abort(404)
    try:
        return render_template("work.html", p=p)
    except TemplateNotFound:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
