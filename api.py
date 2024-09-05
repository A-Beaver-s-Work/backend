from flask import Blueprint
from flask import request
from flask import abort
import uuid
import pickle
import os
from tree import Tree

DB = './super-good-db.pkl'

api = Blueprint("api", __name__, template_folder="templates")

@api.route("/")
def index():
    return "<h1>index :)</h1>"
 

@api.route("trees", methods=['POST'])
def postTrees():
    json = request.get_json()
    try:
        myTree = Tree(json)
    except ValueError as e:
        print(f"Error {e} when reading tree")
        abort(415)

    # Maximum jank database solution
    treeID = str(myTree.treeID)
    if not os.path.exists(DB):
        database = dict()
    else:
        with open(DB, 'rb') as f:
            database = pickle.loads(f.read())

    database[treeID] = myTree.json
    with open(DB, 'wb') as f:
        f.write(pickle.dumps(database))

        
    return {"treeID": treeID}

@api.route("trees", methods=['GET'])
def getTrees():
    if not os.path.exists(DB):
        database = dict()
    else:
        with open(DB, 'rb') as f:
            database = pickle.loads(f.read())
    return database



