from crypt import methods
import os
import json
from urllib import request
import jwt
from flask import Flask , send_file, request , Response
from flask_cors import CORS

host = "http://0.0.0.0:8080"
jwt_key = "123mysecretpassword123"
cores_dir = os.path.abspath(__file__).replace("Flask.py","core")
json_dir = os.path.abspath(__file__).replace("Flask.py","json")
dir_files = os.listdir(cores_dir)

#Temp values
token = "123213123123123"

app = Flask(__name__)
CORS(app, supports_credentials=True)

def downloadUrl(versionname):
    return host + "/version/" + versionname + "/download/"

@app.route("/auth",methods=["POST"])
def auth():
    values = dict(request.form)
    if len(values) == 0:
        return Response("Empty request" , status=400)
    if "token" in values.keys():
        if int(values["token"]) == token:
            return Response("OK",status=200)
    if ("login" in values.keys()) and ("password" in values.keys()):
        resp = Response('{"token":' + token + '}',status=200)
        return resp
    return Response("Bad request" , status=400)

@app.route("/version/<path:versionname>/download/core",methods=["GET"])
def download_core(versionname):
    path = cores_dir + "/" + versionname + ".jar"
    return send_file(path, as_attachment=True)

@app.route("/version/<path:versionname>/download/json",methods=["GET"])
def download_json(versionname):
    path = json_dir + "/" + versionname + ".json"
    return send_file(path, as_attachment=True)

@app.route("/version/<path:versionname>/download" , methods=["GET"])
def download(versionname):
    available_url = {}
    available_url["Core"] = downloadUrl(versionname) + "core"
    available_url["Json"] = downloadUrl(versionname) + "json"
    return available_url

@app.route("/version/<path:versionname>/info",methods=["GET"])
def info(versionname): 
    version_info = {}
    version_info["Version"] = versionname
    with open(json_dir + "/" + versionname + ".json", 'r') as f:
        data = json.load(f)
    version_info["Index"] = data["assetIndex"]["id"]
    version_info["Core"] = downloadUrl(versionname) + "core"
    version_info["Json"] = downloadUrl(versionname) + "json"
    return version_info

@app.route("/version/<path:versionname>" , methods=["GET"])
def version(versionname):
    available_url = {}
    available_url["Download"] = downloadUrl(versionname)[:-1:]
    available_url["Info"] = host + "/version/" + versionname + "/info"
    return available_url

@app.route("/versions" , methods=["GET"])
def versions():
    return send_file(os.path.abspath(__file__).replace("Flask.py","minecraft_versions.json"), as_attachment=False)

app.run(host="0.0.0.0",port=8080)
