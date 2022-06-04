import json

import boto3
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response


class App:

    def __init__(self):
        self.url_map = Map([
            Rule('/<service>/<method>', endpoint='boto_request'),
        ])

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        """
        Dispatcher with 'on_<endpoint>' which can match any endpoint
        configured in 'self.url_map'
        """
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as e:
            return e

    def on_boto_request(self, _request, service, method):
        resp = getattr(boto3.client(service), method)()
        return Response(
            json.dumps(resp, default=str)
        )


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, App(), use_debugger=True, use_reloader=True)
