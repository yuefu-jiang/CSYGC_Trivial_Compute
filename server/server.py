# need work for API
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

# TODO: import more py modules
# it is propably a good idea to implement actual game functions in separate scripts and import them here.
from gameinstance import GameInstance

def setup_server(*args, **kwargs):
    return Server(*args, **kwargs)

# server class
# to add a new rule, add a line in self.app.add_url_rule.
# Then, add a corresponding method to the class as well.
# Imported methods can be called in the added rule method from ext. modules.
class Server:
    def __init__(self, *args, **kwargs):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.add_url_rule(
            "/rule", "rule", self.rule, methods = ["POST"]
        )  

    # an example rule method. only returns json to front.
    def rule(self):
        return jsonify(
            {
                'data': 'Message in a bottle: \nHello from Python! ',
                'action': True,
            }
        )

# fire up server upon init
if __name__ == "__main__":
    # Get the port number passed from Electron
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    # start server
    server = Server()
    # print start up on console too
    print(f"Starting Flask server on port {port}...")
    server.app.run(host="127.0.0.1", port=port, debug=True)