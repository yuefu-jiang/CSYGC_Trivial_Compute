import time
from gameobject import Trivialboard
from gameobject import Wedge
from gameobject import Token
from gamehelperfunct import destination
from gamehelperfunct import rolldice

class GameInstance:
    def __init__(self):
        """
        This class implement a game object containing all necessary instance and attributes of game
        :param width: width of the game board
        :parem players: number of players
        :parem wedge: the list of wedge
        """
        self.gboard = None
        self.gameid = None
        self.boardsize: int
        self.playerno: int
        self.tokenlist = []
        #in format of [['red', '#d62728', 'Geography'],...]
        self.wedgelist = None
        self.wedgeset = ["red", "blue", "orange", "green", "yellow", "purple", "teal"]
        self.wedgecolor = ["#d62728","#1f77b4","#ff7f0e","#2ca02c","#ffff00","#cc00cc","#00cccc"]
        self.q_cat = None

    def initialize(self, gameid:str, playerlist:list , q_cat:list, b_size=9):
        """
        game initialization
        """
        #cleanup existing list
        self.tokenlist.clear()
        self.wedgelist = None
        #get/generate a game id
        self.gameid=gameid
        print(f"started game with ID:{self.gameid}", flush=True)
        #store all game paremeters
        #board size
        self.boardsize = b_size
        #number of player
        self.playerno = len(playerlist)
        #question categories
        self.q_cat = q_cat[:]
        print(self.q_cat)
        #choose number of color according to total types of Question Categories
        self.choosewedege(len(q_cat))
        print(f"Total no. of players:{self.playerno}", flush=True)
        print(self.wedgelist)
        #generate the game board
        self.gboard = Trivialboard(self.boardsize)
        #assign color to squares
        self.coloring()
        self.gboard.print_b()
        #add a token for all players
        i = 0
        while i < self.playerno:
            self.tokenlist.append(Token(self.wedgelist))
            i+=1
        #initialize all tokens, store name, put all token at center
        i = 0
        while i < len(self.tokenlist):
            self.tokenlist[i].label = playerlist[i]
            self.tokenlist[i].row = self.gboard.CT[0]
            self.tokenlist[i].col = self.gboard.CT[1]
            print(f"player {i}: name: {self.tokenlist[i].label} location: [{self.tokenlist[i].row},{self.tokenlist[i].col}]", flush=True)
            i+=1

    def choosewedege(self, q_type:int):
        self.wedgelist = list()
        i = 0
        for i in range(q_type):
            self.wedgelist.append([self.wedgeset[i],self.wedgecolor[i],self.q_cat[i]])

    def coloring(self):
        """
        assign color to each squares
        """
        temp_l = len(self.wedgelist)
        temp_hq = 0
        t = 0
        i = 0
        j = 0
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                temp_cat = self.gboard.board[i][j].cat
                match temp_cat:
                    case "CT":
                        self.gboard.board[i][j].color = "#ffffff"
                    case "RA":
                        self.gboard.board[i][j].color = "#ffffff"
                    case "HQ":
                        self.gboard.board[i][j].color = self.wedgelist[temp_hq][1]
                        temp_hq=(temp_hq+1)%temp_l
                    case "NL":
                        self.gboard.board[i][j].color = self.wedgelist[t][1]
                        t = (t+1)%temp_l
                j+=1
            i+=1
    
    def colordict(self)->dict:
        """return a dict of colors for board coloring"""
        temp = dict()
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                temp.update({str(i)+","+str(j):self.gboard.board[i][j].color})
                j+=1
            i+=1
        return temp
    
    def tidOf(self,name:str)->int:
        """
        :param name: label of player
        :return: token id of the player
        """
        i=0
        while i<self.playerno:
            if self.tokenlist[i].label == name:
                return i
            i+=1
        return -1
    
    def catIdof(self, cat:str)->int:
        """
        :param cat: category of question
        :return: category id of the question
        """
        i=0
        while i < len(self.q_cat):
            if self.q_cat[i] == cat:
                return i
            i+=1
        return -1

    def currentpos(self,tid:int)->list:
        """
        :param tid: token id of player
        :return: coordinates of the current position of the token in a list of [i,j]
        """
        return self.tokenlist[tid].position()

    def getValidChoices(self, tid: int, steps:int)->list:
        """
        :param tid: id number of player (0/1/2....)
        :parem steps: how many steps to take
        """
        return destination(self.tokenlist[tid].row,self.tokenlist[tid].col,steps,self.gboard.board)

    def movePlayer(self, tid: int, i:int, j:int):
        """
        :param tid: id number of player (0/1/2....)
        :parem i: row number of the destination
        :parem j: col number of the destination
        """
        self.tokenlist[tid].moveto(i,j)
        
    def correctAnswer(self, tid: int, cat:str):
        """
        :param tid: id number of player (0/1/2....)
        :parem cat: category of question
        """
        