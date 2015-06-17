from flask import request

from app import app, tools
from api import json_tools, tools


@app.route("/buscar_json", methods=['POST', 'GET'])
def search_json():
    if request.method == 'GET':
        return json_tools.search_json(request.args.get("search"))

@app.route("/search_for_universities", methods=['POST', 'GET'])
def search_for_universities():
    return json_tools.university_json()

@app.route("/knowledge_area_json", methods=['POST', 'GET'])
def search_knowledge_area():
    return json_tools.knowledge_area_json(tools.if_none(request.args.get("question")))

