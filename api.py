import os
import time

from flask import Blueprint, request, url_for, current_app, redirect, send_from_directory
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
        return "Request must include file with label 'image_upload', but none found.", 400

    image = request.files['image_upload']
    
    if image.filename == '':
        return "Request must include file, but empty filename found.", 400

    if image and allowed_file(image.filename):
        filename = str(int(time.time())) + "_" + secure_filename(image.filename)
        image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        return {"url": url_for("api.download_image", name=filename, _external=True)}, 200 

    return "Invalid file type. Allowed are: [png, jpg, jpeg, webp].", 415
 
@api.route("/images/<name>", methods=["GET"])
def download_image(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)

@api.route("/trees/<uid>", methods=["PUT", 'DELETE'])
def update(uid):
    if request.method == "PUT":
        if request.headers.get("Content-Type") != "application/json":
            return "Unsupported Media Type: format all requests using JSON", 415

        body = request.get_json()

        expected_attrs = ["type", "owner", "age", "visits", "images"]
        for attr in expected_attrs:
            if body.get(attr) == None:
                return f"invalid tree: expected `{attr}` attribute", 400

        if body.get("location") != None:
            location = body.get("location")
            if not {"latitude", "longitude"}.issubset(location.keys()):
                return "invalid location data: expected latitude and longitude or neither", 400

            if not (-180 <= location.get("longitude") <= 180) or not (-90 <= location.get("longitude") <= 90):
                return "longitude should be in range [-180, 180] and latitude should be in range [-90, 90]", 400

        if not (isinstance(body.get("visits"), int) and isinstance(body.get("age"), int)):
            return "visits and age should be positive integers", 400

        if not isinstance(body.get("images"), list):
            return "images must be a list", 400

        if body.get("age") < 0 or body.get("visits") < 0:
            return "visits and age should be positive", 400 
        
        ### TODO: Actually update data ###
        return "Ok", 200 

    if request.method == "DELETE":
        ### TODO: Actually delete data ###
        return "Ok", 200
