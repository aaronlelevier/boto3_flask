# import boto3
# from flask import Flask

# app = Flask(__name__)

# @app.route("/<service>/<method>/")
# def entrypoint(service, method):
#     return getattr(boto3.client(service), method)()


import multiprocessing
from werkzeug import Request, Response, run_simple

def get_token(q: multiprocessing.Queue) -> None:
    @Request.application
    def app(request: Request) -> Response:
        q.put(request.args["token"])
        return Response("", 204)

    run_simple("localhost", 5000, app)

if __name__ == "__main__":
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=get_token, args=(q,))
    p.start()
    print("waiting")
    token = q.get(block=True)
    p.terminate()
    print(token)
