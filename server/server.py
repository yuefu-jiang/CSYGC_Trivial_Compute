# need work for API
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys


def setup_server(*args, **kwargs):
    return Server(*args, **kwargs)

class Server:
    def __init__(self, *args, **kwargs):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.add_url_rule(
            "/rule", "rule", self.rule, methods = ["POST"]
        )  

    def rule(self):
        return jsonify(
            {
                'data': 'Message in a bottle: \nHello from Python! ',
                'action': True,
            }
        )


if __name__ == "__main__":
    # Get the port number passed from Electron
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    server = Server()
    print(f"🚀 Starting Flask server on port {port}...")
    server.app.run(host="127.0.0.1", port=port, debug=True)