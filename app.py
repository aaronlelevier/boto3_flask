import boto3
from flask import Flask


app = Flask(__name__)

@app.route("/<service>/<method>/")
def entrypoint(service, method):
    return getattr(boto3.client(service), method)()
