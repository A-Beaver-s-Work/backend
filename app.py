from flask import Flask
from api import api

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000 # 5 mb

app.register_blueprint(api, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    