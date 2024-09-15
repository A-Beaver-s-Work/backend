import os
import uuid
import time

from flask import Blueprint, request, url_for, current_app, redirect, send_from_directory
from werkzeug.utils import secure_filename

from tree import Tree
from logger import logger
from connection import execute_sql

api = Blueprint("api", __name__, template_folder="templates")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# This doesn't actually check to be sure the file is the type it says it is... it just checks the extension
# Security people should know why this is bad :)
# But at the very least your browser shouldn't auto execute arbitrary code as long as the user doesn't do something wrong
def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route("/trees", methods=['POST'])
def add_tree():
    if request.headers.get("Content-Type") != "application/json":
        return "Unsupported Media Type: format all requests using JSON", 415

    json = request.get_json()

    try:
        parsed_tree = Tree(json)
    except Exception as e:
        # Security?
        return str(e), 400

    return {"uid": parsed_tree.uid}, 200

@api.route("/trees", methods=['GET'])
def getTrees():
    # TODO: query for trees from MySQL database
    return [], 200

@api.route("/trees/<uid>", methods=["PUT", 'DELETE'])
def update(uid):
    if request.method == "PUT":
        if request.headers.get("Content-Type") != "application/json":
            return "Unsupported Media Type: format all requests using JSON", 415

        body = request.get_json()

        try:
            parsed_tree = Tree(body, uid=uid)
        except Exception as e:
            # ref post req
            return str(e), 400

        return "Ok", 200 

    if request.method == "DELETE":
        try:
            execute_sql("DELETE from tree WHERE tree_id=(%(uid)s)", {"uid": uid})
        except:
            return "Internal Server Error", 500

        logger.info(f"Deleted tree_id {uid} from 'tree' table.")

        return "Ok", 200

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
        
        try:
            execute_sql("INSERT INTO `images` (filename) VALUES (%(filename)s)", {'filename': filename})
        except:
            return "Internal Server Error", 500

        logger.info(f"Inserted {filename} into images table")
    
        return {"url": url_for("api.download_image", name=filename, _external=True)}, 200 

    return "Invalid file type. Allowed are: [png, jpg, jpeg, webp].", 415
 
@api.route("/images/<name>", methods=["GET"])
def download_image(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)
