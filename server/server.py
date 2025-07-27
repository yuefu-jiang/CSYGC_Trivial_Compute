# need work for API
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
import json
import random

from gameinstance import GameInstance
from gamehelperfunct import poskeyTolist

# TODO: import more py modules
# it is propably a good idea to implement actual game functions in separate scripts and import them here.
gameSession = {}

QUESTION_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')


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

        self.app.add_url_rule(
            "/initializegametest", "initializegametest", self.initializegametest, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getboardcolor", "getboardcolor", self.getboardcolor, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getnames", "getnames", self.getnames, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getallpos", "getallpos", self.getallpos, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getqtype", "getqtype", self.getqtype, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getvalidmove", "getvalidmove", self.getvalidmove, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getallWedge", "getallWedge", self.getallWedge, methods=["POST"]
        )

        self.app.add_url_rule(
            "/moveToDes", "moveToDes", self.moveToDes, methods=["POST"]
        )

        self.app.add_url_rule(
            "/addwedge", "addwedge", self.addwedge, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getSquareType", "getSquareType", self.getSquareType, methods=["POST"]
        )

        self.app.add_url_rule(
            "/getCurrentCat", "getCurrentCat", self.getCurrentCat, methods=["POST"]
        )

        self.app.add_url_rule(
            "/anyoneWin", "anyoneWin", self.anyoneWin, methods=["POST"]
        )        

        self.app.add_url_rule(
            "/roll", "roll", self.roll, methods=["POST"]
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

    def anyoneWin(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        win_list = temp.getWinlist()
        print(f'{type(win_list)}, {win_list}',flush=True)
        Iswin = False
        if win_list:
            Iswin = True
        return jsonify(
            {
                'win_list': win_list,
                'Winstatus': Iswin,
            }
        )
    
    def roll(self):
        roll_result = random.randint(1, 6)
        # Stub: random coordinate and category
        coordinate = [random.randint(0, 7), random.randint(0, 7)]
        categories = ["Science", "History", "Art", "Sports", "Geography", "Entertainment"]
        category = random.choice(categories)
        return jsonify({
            'roll': roll_result,
            'coordinate': coordinate,
            'category': category
        })
    
    def initializegametest(self):
        content = request.get_json()
        gameid = content.get('gameid')
        namelist = content.get('namelist',[])
        q_cat = content.get('q_cat')
        q_type = len(q_cat)
        b_size = content.get('b_size')
        self.app.logger.info(content)
        newgame=GameInstance()
        newgame.initialize(gameid,namelist,q_cat)
        gameSession.update({gameid:newgame})
        print(gameSession, flush=True)
        return jsonify(
            {
                'list': [0,1],
                'data': 'game initialize success',
            }
        )    

    def getvalidmove(self):
        content = request.get_json()
        gameid = content.get('gameid')
        tid = content.get('tid')
        steps = content.get('steps')
        temp = gameSession.get(gameid)
        valid_list = temp.getValidChoices(tid,steps)
        print(f'{type(valid_list)}, {valid_list}',flush=True)
        return jsonify(
            {
                'valid_list': valid_list,
                'msg': 'get valid square success',
            }
        )    
    
    def moveToDes(self):
        content = request.get_json()
        gameid = content.get('gameid')
        tid = content.get('tid')
        locationKey = content.get('locationKey')
        tokenPos = poskeyTolist(locationKey)
        temp = gameSession.get(gameid)
        print(f'{type(locationKey)}, {locationKey}',flush=True)
        temp.movePlayer(tid,tokenPos[0],tokenPos[1])
        return jsonify(
            {
                'msg': 'player move success',
            }
        )
    
    def addwedge(self):
        content = request.get_json()
        gameid = content.get('gameid')
        tid = content.get('tid')
        qtype = content.get('qtype')
        temp = gameSession.get(gameid)
        print(f'!!!!!!!!!!!!!!!!!adding this wedge for this:{qtype}!!!!!!!!!!!!!!!!!!!!!!!',flush=True)
        temp.updatePlayerWedge(tid,qtype)
        return jsonify(
            {
                'msg': 'player wedge updated',
            }
        )

    def getallWedge(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        temp_wedgeDict = temp.getallWedges()
        return jsonify(
            {
                'allwedge': temp_wedgeDict,
                'msg': 'all player wedge updated',
            }
        )

    def getboardcolor(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        color_dict = temp.colordict()
        return jsonify(
            {
                'color': color_dict,
                'msg': 'get color success',
            }
        )    

    def getallpos(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        pos_dict = temp.allcurrentpos()
        return jsonify(
            {
                'pos': pos_dict,
                'msg': 'get coordinates success',
            }
        )    

    def getnames(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        name_list = temp.allnames()
        return jsonify(
            {
                'name': name_list,
                'msg': 'get names success',
            }
        )    
    
    def getqtype(self):
        content = request.get_json()
        gameid = content.get('gameid')
        temp = gameSession.get(gameid)
        q_list = temp.q_cat
        return jsonify(
            {
                'qtype': q_list,
                'msg': 'get question type success',
            }
        )         

    def getSquareType(self):
        content = request.get_json()
        gameid = content.get('gameid')
        tid = content.get('tid')
        temp = gameSession.get(gameid)
        squaretype = temp.getSquareType(tid)
        print(f'current square type: -----------------{squaretype}',flush=True)
        return jsonify(
            {
                'sqtype': squaretype,
                'msg': 'get square type success',
            }
        ) 

    def getCurrentCat(self):
        content = request.get_json()
        gameid = content.get('gameid')
        tid = content.get('tid')
        temp = gameSession.get(gameid)
        Cat = temp.getCat(tid)
        print(f'current question type: -----------------{Cat}',flush=True)
        return jsonify(
            {
                'category': Cat,
                'msg': 'get question type success',
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
    print(f"Starting Flask server on port {port}...")
    server.app.run(host="127.0.0.1", port=port, debug=True)