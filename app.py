from flask import Flask, render_template, request, redirect, url_for, session

import smtplib
from email.mime.text import MIMEText
from google.cloud import storage
import datetime
import os

app = Flask(__name__)

# Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\djeki\\OneDrive\\Desktop\\programiranje\\Filipov_Projekat_prvi_deo\\smooth-unison-428617-e2-ea4e4fc24cda.json"

templates = {
    "template-9": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "phase56": {
        "name": "Business Template",
        "gcs_path": "data_forex.zip",
        "price":15.00
    },
    "youtube": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "designer": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-10": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-8": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-7": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-6": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-5": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-4": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-3": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-2": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    },
    "template-1": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":10.00  
    }
}
app.secret_key = "tajni_kljuc_123"  # Ovo mora biti nešto random

GCS_BUCKET_NAME = "moj-sajt-bucket"
gcs_client = storage.Client()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'djekicn05@gmail.com'
SMTP_PASS = 'myku tbyv botm rrov'  # OVDE OBAVEZNO UBACI PRAVI PASSWORD AKO TESTIRAŠ

# NOVA RUTA
@app.route("/templates")
def list_templates():
    return render_template("templates.html", templates=templates)

@app.route("/")
def checkout():
    template_id = request.args.get("template_id")
    if template_id not in templates:
        return "Template not found", 404

    price = templates[template_id]["price"]
    return render_template("checkout.html", template_id=template_id, price=price)

@app.route("/pay", methods=["POST"])
def pay():
    email = request.form.get("email")
    cart = session.get('cart', [])

    if not email or not cart:
        return "Invalid request", 400

    download_links = []
    for template_id in cart:
        if template_id in templates:
            blob = gcs_client.bucket(GCS_BUCKET_NAME).blob(templates[template_id]["gcs_path"])
            expiration = datetime.timedelta(hours=24)
            signed_url = blob.generate_signed_url(expiration=expiration, method='GET')
            download_links.append((templates[template_id]['name'], signed_url))

    send_email(email, download_links)

    # Očisti korpu
    session['cart'] = []
    return redirect(url_for("success", email=email))

@app.route("/success")
def success():
    email = request.args.get("email")
    return render_template("success.html", email=email)

def send_email(to_email, download_links):
    subject = "Hvala na kupovini!"
    body = "Pozdrav,\n\nHvala što ste kupili naše templejte!\n\n"

    for name, link in download_links:
        body += f"{name}: {link}\n"

    body += "\nPozdrav,\nVaš tim."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


# Dodavanje u korpu
@app.route("/add_to_cart/<template_id>")
def add_to_cart(template_id):
    if template_id not in templates:
        return "Template not found", 404

    cart = session.get('cart', [])
    cart.append(template_id)
    session['cart'] = cart
    return redirect("/cart")

@app.route("/cart")
def view_cart():
    cart = session.get('cart', [])
    items = [templates[tid] for tid in cart]
    total = sum(float(t['price']) for t in items)
    return render_template("cart.html", items=items, total=total)


if __name__ == "__main__":
    app.run(debug=True)
