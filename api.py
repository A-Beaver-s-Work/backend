import os
import time

from flask import Blueprint, request, url_for, current_app, redirect
from werkzeug.utils import secure_filename

api = Blueprint("api", __name__, template_folder="templates")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# This doesn't actually check to be sure the file is the type it says it is... it just checks the extension
# Security people should know why this is bad :)
# But at the very least your browser shouldn't auto execute arbitrary code as long as the user doesn't do something wrong
def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route("/images", methods=["POST"])
def upload_image():
    if 'image_upload' not in request.files:
        return "No file part", 400

    image = request.files['image_upload']
    
    if image.filename == '':
        return "No selected file"

    if image and allowed_file(image.filename):
        filename = str(int(time.time())) + "_" + secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return {"url": url_for("api.download_image", name=filename, _external=True)} 
 
@api.route("/images/<name>", methods=["GET"])
def download_image(name):
    return 418
