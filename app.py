from flask import Flask
from api import api

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"

app.register_blueprint(api, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
