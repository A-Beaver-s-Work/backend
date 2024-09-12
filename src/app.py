from flask import Flask
from api import api

import mysql.connector
from mysql.connector import errorcode

#cnx = mysql.connector.connect(user='root', password='secretrootpass', host='db', database='abw', port=3306)
#if cnx and cnx.is_connected():
#    with cnx.cursor() as cursor:
#        result = cursor.execute("DESCRIBE tree;")
#        rows = cursor.fetchall()
#        for row in rows:
#            print(rows)
#        print("done")
#    cnx.close()
#else:
#    print("couldn't connect")

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "/usr/local/app/uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000 # 5 mb

app.register_blueprint(api, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
