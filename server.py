from flask import Flask, render_template, request, redirect, send_from_directory, abort
import csv
import os

app = Flask(__name__)

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
    return render_template(page_name)

def write_to_file(data):
    with open("database.txt", mode="a") as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        database.write(f"\n{email},{subject},{message}")

def write_to_csv(data):
    with open("database.csv", mode="a", newline="") as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect("/thankyou.html")
        except Exception:
            return "Did not save to database"
    return "Something went wrong. Try again!"

if __name__ == "__main__":
    app.run(debug=True)
