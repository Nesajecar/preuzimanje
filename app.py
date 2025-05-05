from flask import Flask, render_template, request, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
from google.cloud import storage
from google.oauth2 import service_account
import datetime
import os
import json

app = Flask(__name__)
app.secret_key = "tajni_kljuc_123"

# GCS kredencijali
creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/etc/secrets/fileenv')
if not creds_json:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS nije postavljen")

credentials_info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(credentials_info)
gcs_client = storage.Client(credentials=credentials)

GCS_BUCKET_NAME = "moj-sajt-bucket"

# Email podešavanja
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'djekicn05@gmail.com'  # zameni stvarnim
SMTP_PASS = 'myku tbyv botm rrov'         # zameni stvarnim

# Lista dostupnih templejta
templates = {
    "template-9": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "phase56": {
        "name": "Business Template",
        "gcs_path": "data_forex.zip",
        "price":49.99
    },
    "youtube": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99 
    },
    "designer": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99
    },
    "template-10": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-8": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-7": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99 
    },
    "template-6": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-5": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-4": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-3": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-2": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    },
    "template-1": {
        "name": "Portfolio Template",
        "gcs_path": "templates.zip",
        "price":49.99  
    }
}
# Prikaz svih templejta
@app.route("/templates")
def list_templates():
    return render_template("templates.html", templates=templates)

# Checkout stranica
@app.route("/")
def checkout():
    template_id = request.args.get("template_id")
    if template_id not in templates:
        return "Template ne postoji", 404
    price = templates[template_id]["price"]
    return render_template("checkout.html", template_id=template_id, price=price)

# Dodavanje u korpu
@app.route("/add_to_cart/<template_id>")
def add_to_cart(template_id):
    if template_id not in templates:
        return "Template ne postoji", 404
    cart = session.get('cart', [])
    cart.append(template_id)
    session['cart'] = cart
    return redirect("/cart")

# Prikaz korpe
@app.route("/cart")
def view_cart():
    cart = session.get('cart', [])
    items = [templates[tid] for tid in cart]
    total = sum(t['price'] for t in items)
    return render_template("cart.html", items=items, total=total)

# Plaćanje
@app.route("/pay", methods=["POST"])
def pay():
    email = request.form.get("email")
    cart = session.get("cart", [])

    if not email or not cart:
        return "Email ili korpa nisu validni", 400

    download_links = []
    bucket = gcs_client.bucket(GCS_BUCKET_NAME)

    for template_id in cart:
        if template_id in templates:
            blob = bucket.blob(templates[template_id]["gcs_path"])
            signed_url = blob.generate_signed_url(
                expiration=datetime.timedelta(hours=24),
                method="GET"
            )
            download_links.append((templates[template_id]['name'], signed_url))

    send_email(email, download_links)
    session['cart'] = []
    return redirect(url_for("success", email=email))

# Stranica uspeha
@app.route("/success")
def success():
    email = request.args.get("email")
    return render_template("success.html", email=email)

# Slanje emaila
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

# Pokretanje aplikacije
if __name__ == "__main__":
    app.run(debug=True)

