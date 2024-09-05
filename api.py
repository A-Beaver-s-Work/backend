from flask import Blueprint, request, abort
import uuid
import os
from tree import Tree

api = Blueprint("api", __name__, template_folder="templates")

@api.route("/trees", methods=['POST'])
def add_tree():
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


