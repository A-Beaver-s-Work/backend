from flask import Blueprint, request

api = Blueprint("api", __name__, template_folder="templates")

@api.route("/")
def index():
    return "<h1>index :)</h1>"


@api.route("/trees/<uid>", methods=["PUT", 'DELETE'])
def update(uid):
    if uid and request.form["tree type"] and request.form["owner"] and request.form["age"] and request.form["visit counter"] and request.form["picture URL"]:
        if request.form["latitude"] and not request.form["longitude"] or not request.form["latitude"] and request.form["longitude"]:
            return 415
        
        if not(type(request.form["tree type"]) == str and type(request.form["owner"]) == str and type(request.form["age"]) == int and type(request.form["visit counter"]) == int \
               and type(request.form["picture URL"]) == str):
            return 415
        
        if request.form["age"] < 0 or request.form["visit counter"] < 0:
            return 415
        
        if request.form["latitude"] and request.form["longitude"]:
            if not (type(request.form["latitude"]) == str and type(request.form["longitude"]) == str):
                return 415

    else:
        return 415


    if request.method == "PUT":
        ### TODO: Actually update data ###
        pass

    if request.method == "DELETE":
        ### TODO: Actually delete data ###
        pass
    
    
    return 200