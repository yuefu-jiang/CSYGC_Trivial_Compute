# need work for API
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
import json
from pathlib import Path


# TODO: import more py modules
# it is propably a good idea to implement actual game functions in separate scripts and import them here.

QUESTION_FILE = Path(__file__).resolve().parents[2] / "questions.json"


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
        self.app.add_url_rule(
            "/question", "get_question", self.get_question, methods=["GET"]
        )

        self.app.add_url_rule(
            "/init_questions", "init_questions", self.return_all_questions, methods=["POST"]
        )
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s  %(message)s'
        )

        self.app.logger.setLevel(logging.DEBUG)
        self.app.logger.info("This is an informational message.")


    # an example rule method. only returns json to front.
    def rule(self):
        return jsonify(
            {
                'data': 'Message in a bottle: \nHello from Python! ',
                'action': True,
            }
        )
    
    def return_question(self, category, qid, mark_used=False):
        try:
            with open(QUESTION_FILE, 'r') as f:
                data = json.load(f)
            self.app.logger.info('Loaded questions.')
            question_data = data.get(category, {}).get(qid, None)
            if question_data is None:
                return None

            if mark_used:
                question_data['used'] = True
                data[category][qid]['used'] = True
                with open(QUESTION_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

            return question_data

        except Exception as e:
            print(f"Error reading questions file: {e}")
            return None

    def get_question(self):
        qid = request.args.get('qid')
        category = request.args.get('category')
        self.app.logger.info(category)
        if not category or not qid:
            return jsonify({'error': 'Missing parameters'}), 400

        question = self.return_question(category, qid, mark_used=False)  # set to True if write enabled

        if question:
            self.app.logger.info(f'Returned QID #{qid} to frontend.')
            return jsonify({'category': category, 'qid': qid, 'data': question})
        else:
            return jsonify({'error': 'Question not found'}), 404

    def return_all_questions(self):
        try:
            with open(QUESTION_FILE, 'r') as f:
                data = json.load(f)

            self.app.logger.info('Started Game server and loaded question database.')
            aq_dict = {}
            for cat in data.keys():
                aq_dict[cat] = list(data[cat].keys())
                self.app.logger.info(data[cat].keys())

            self.app.logger.info(aq_dict)

            return jsonify(
                {
                    'data': aq_dict,
                }
            )

        except Exception as e:
            print(f"Error reading questions file: {e}")
            return None
          
# fire up server upon init
if __name__ == "__main__":
    # Get the port number passed from Electron
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    # start server
    server = Server()
    # print start up on console too
    print(f"🚀 Starting Flask server on port {port}...")
    server.app.run(host="127.0.0.1", port=port, debug=True)