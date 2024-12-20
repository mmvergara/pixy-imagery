import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
import random
from io import BytesIO
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY")

if API_KEY == "":
    API_KEY = None

if API_KEY == None:
    print("INFO: API Key is not set, no api key is needed to access the service")
    print("INFO: API Key is not set, no api key is needed to access the service")
    print("INFO: API Key is not set, no api key is needed to access the service")
else:
    print("INFO: API Key is set, api key is needed to access the service")
    print("INFO: API Key is set, api key is needed to access the service")
    print("INFO: API Key is set, api key is needed to access the service")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["API_KEY"] = API_KEY


def validate_api_key(api_key):
    if API_KEY == None:
        return True
    return api_key == API_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload-image", methods=["POST"])
def upload_image():
    api_key = request.args.get("api_key", type=str)
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    if "images" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_files = request.files.getlist("images")
    image_info = []

    for file in uploaded_files:
        if file.filename == "":
            continue

        file_ext = os.path.splitext(file.filename)[1]
        image_id = str(uuid.uuid4())
        filename = f"{image_id}{file_ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        with Image.open(filepath) as img:
            img.save(filepath, optimize=True, quality=85)

        # Create URL using request.host_url
        image_url = f"{request.host_url}{image_id}"
        image_info.append({"image_id": image_id, "url": image_url})

    return jsonify({"images": image_info})


@app.route("/<image_id>")
def serve_image(image_id):
    api_key = request.args.get("api_key", type=str)
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    matching_files = [
        f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.startswith(image_id)
    ]

    if not matching_files:
        return jsonify({"error": "Image not found"}), 404

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], matching_files[0])

    # Optional query parameters
    width = request.args.get("w", type=int)
    height = request.args.get("h", type=int)
    maintain_aspect_ratio = request.args.get("maintain_aspect_ratio", type=bool)

    with Image.open(filepath) as img:
        # Resize if width and height are specified
        if width or height:
            if maintain_aspect_ratio:
                img.thumbnail((width or img.width, height or img.height), Image.LANCZOS)
            else:
                img = img.resize(
                    (width or img.width, height or img.height), Image.LANCZOS
                )

        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")


@app.route("/random")
def random_image():
    api_key = request.args.get("api_key", type=str)
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    uploaded_images = os.listdir(app.config["UPLOAD_FOLDER"])

    if not uploaded_images:
        return jsonify({"error": "No images available"}), 404

    random_image_filename = random.choice(uploaded_images)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], random_image_filename)

    # Optional query parameters
    width = request.args.get("w", type=int)
    height = request.args.get("h", type=int)
    maintain_aspect_ratio = request.args.get("maintain_aspect_ratio", type=bool)

    with Image.open(filepath) as img:
        if width or height:
            if maintain_aspect_ratio:
                img.thumbnail((width or img.width, height or img.height), Image.LANCZOS)
            else:
                img = img.resize(
                    (width or img.width, height or img.height), Image.LANCZOS
                )

        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
