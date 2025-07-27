from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
import json
from pathlib import Path

QUESTION_FILE = Path(__file__).resolve().parents[2] / "questions.json"

def setup_server(*args, **kwargs):
    return Server(*args, **kwargs)

class Server:
    def __init__(self, *args, **kwargs):
        self.app = Flask(__name__)
        CORS(self.app)

        # Routes
        self.app.add_url_rule("/rule", "rule", self.rule, methods=["POST"])
        self.app.add_url_rule("/question", "get_question", self.get_question, methods=["GET"])
        self.app.add_url_rule("/init_questions", "init_questions", self.return_all_questions, methods=["POST"])
        self.app.add_url_rule("/replace_questions_file", "replace_questions_file", self.replace_questions_file, methods=["POST"])
        self.app.add_url_rule("/add_to_questions_file", "add_to_questions_file", self.add_to_questions_file, methods=["POST"])

        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s  %(message)s'
        )
        self.app.logger.setLevel(logging.DEBUG)
        self.app.logger.info("Server initialized.")

    def rule(self):
        return jsonify({
            'data': 'Message in a bottle: \nHello from Python!',
            'action': True,
        })

    def return_question(self, category, qid, mark_used=False):
        try:
            with open(QUESTION_FILE, 'r') as f:
                data = json.load(f)
            self.app.logger.info('Loaded questions.')

            question_data = data.get(category, {}).get(qid)
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
        if not category or not qid:
            return jsonify({'error': 'Missing parameters'}), 400

        question = self.return_question(category, qid, mark_used=False)

        if question:
            return jsonify({'category': category, 'qid': qid, 'data': question})
        else:
            return jsonify({'error': 'Question not found'}), 404

    def is_valid_questions_object(self, data):
        if not isinstance(data, dict):
            return False
        
        for category, questions in data.items():
            if not isinstance(questions, dict):
                self.app.logger.warning(f"Category '{category}' is not a dict")
                return False

            for qid, qdata in questions.items():
                if not isinstance(qdata, dict):
                    self.app.logger.warning(f"Question '{qid}' in category '{category}' is not a dict")
                    return False

                if "question" not in qdata or "answer" not in qdata or "used" not in qdata:
                    self.app.logger.warning(f"Question '{qid}' missing required fields")
                    return False

                if not isinstance(qdata["question"], str):
                    self.app.logger.warning(f"'question' field in '{qid}' is not a string")
                    return False

                if not isinstance(qdata["used"], bool):
                    self.app.logger.warning(f"'used' field in '{qid}' is not a boolean")
                    return False

        return True

    
    def replace_questions_file(self):
        try:
            new_data = request.get_json()
            if not new_data or not isinstance(new_data, dict):
                return jsonify({'error': 'Invalid JSON payload'}), 400

            if not self.is_valid_questions_object(new_data):
                return jsonify({'error': 'Invalid question format'}), 400

            with open(QUESTION_FILE, 'w') as f:
                json.dump(new_data, f, indent=2)

            self.app.logger.info('Questions file replaced successfully.')
            return jsonify({'status': 'Questions file replaced successfully'}), 200

        except Exception as e:
            self.app.logger.error(f"Error replacing questions file: {e}")
            return jsonify({'error': 'Failed to replace questions file'}), 500


    def add_to_questions_file(self):
        try:
            new_data = request.get_json()
            if not new_data or not isinstance(new_data, dict):
                return jsonify({'error': 'Invalid JSON payload'}), 400

            if not self.is_valid_questions_object(new_data):
                return jsonify({'error': 'Invalid question format'}), 400

            if QUESTION_FILE.exists():
                with open(QUESTION_FILE, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = {}

            for category, questions in new_data.items():
                if category not in existing_data:
                    existing_data[category] = {}
                existing_data[category].update(questions)

            with open(QUESTION_FILE, 'w') as f:
                json.dump(existing_data, f, indent=2)

            self.app.logger.info('Questions file updated (merged) successfully.')
            return jsonify({'status': 'Questions merged successfully'}), 200

        except Exception as e:
            self.app.logger.error(f"Error merging questions file: {e}")
            return jsonify({'error': 'Failed to merge questions file'}), 500

    def return_all_questions(self):
        try:
            with open(QUESTION_FILE, 'r') as f:
                data = json.load(f)

            aq_dict = {cat: list(data[cat].keys()) for cat in data}
            self.app.logger.info('Returning all questions.')
            return jsonify({'data': aq_dict})

        except Exception as e:
            self.app.logger.error(f"Error reading questions file: {e}")
            return jsonify({'error': 'Failed to read questions file'}), 500

# Start server
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    server = Server()
    print(f"🚀 Starting Flask server on port {port}...")
    server.app.run(host="127.0.0.1", port=port, debug=True)
