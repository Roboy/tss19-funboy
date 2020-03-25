import json
import os
import logging as logger

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

from gptwrapper import GPTWrapper


MODEL = '774A'
PATH = f'{os.path.dirname(__file__)}/models'

responder = GPTWrapper(model_name=MODEL, path=PATH)


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.send_header('x-dino', 'dinos are great')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        for key in query_components:
            query_components[key] = ''.join(query_components[key])
        types = " ".join([f"<|{x}|>" for x in query_components.pop("types").split(",")])
        utterance = query_components.pop("utterance")
        if utterance != " ":
            response = responder.render(f"{types}{utterance}")
        else:
            response = responder.render(types)
        json_payload = json.dumps({"response": response})
        self.wfile.write(bytes(json_payload, encoding="utf-8"))

    def do_HEAD(self):
        self._set_headers()


def run(port=5050):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    logger.info(f'Started the server')
    httpd.serve_forever()
