import os
from flask import Flask, request, jsonify
from google.cloud import storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

auth_json_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/etc/secrets/auth1')
print(f"Pokušavam da učitam fajl sa kredencijalima sa: {auth_json_path}")

if auth_json_path and os.path.exists(auth_json_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_json_path
    print(f"Kredencijali su postavljeni sa: {auth_json_path}")
else:
    print(f"Greška: Fajl sa kredencijalima nije pronađen na {auth_json_path}")
    print("Sadržaj direktorijuma /etc/secrets:")
    print(os.listdir("/etc/secrets"))

BUCKET_NAME = "moj-sajt-bucket"

def upload_to_gcs(file, destination_path):
    try:
        client = storage.Client()  # Povezivanje sa Google Cloud-om
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(destination_path)
        blob.upload_from_file(file)
        return True
    except Exception as e:
        print(f"Greška pri uploadu fajla: {e}")
        return False

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file' not in request.files or 'path' not in request.form:
        return jsonify({"message": "Fajl ili putanja nisu poslati!"}), 400

    file = request.files['file']
    relative_path = request.form['path']
    destination_path = f"uploads/{relative_path}"

    if upload_to_gcs(file, destination_path):
        return jsonify({"message": f"Fajl uspešno uploadovan na {destination_path}"}), 200
    else:
        return jsonify({"message": "Greška pri uploadu!"}), 500

if __name__ == '__main__':
    app.run(debug=True)

