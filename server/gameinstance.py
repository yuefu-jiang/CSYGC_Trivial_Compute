import time
from gameobject import Trivialboard
from gameobject import Wedge
from gameobject import Token
from gamehelperfunct import destination
from gamehelperfunct import rolldice

class GameInstance:
    def __init__(self, width: int, players: int, wedge: Wedge):
        """
        This class implement a game object containing all necessary instance and attributes of game
        :param width: width of the game board
        :parem players: number of players
        :parem wedge: the list of wedge
        """
        self.gboard = None
        self.gameid = None
        self.boardsize = width
        self.playerno = players
        self.tokenlist = []
        self.wedgelist = wedge
        self.initialize()

    def initialize(self):
        """
        game initialization
        """
        #generate a game id
        self.gameid=self.genid()
        #generate the game board
        self.gboard = Trivialboard(self.boardsize)
        #add a token for all players
        i = 0
        while i < self.playerno:
            self.tokenlist.append(Token(self.wedgelist))
            i+=1
        #assign color to squares
        self.coloring()
        #assign name
        #put all token at center
        i = 0
        while i < len(self.tokenlist):
            self.tokenlist[i].row = self.gboard.CT[0]
            self.tokenlist[i].col = self.gboard.CT[1]
            i+=1

    def coloring(self):
        """
        assign color to each squares
        """
        temp_hq = list(self.wedgelist.chosen.copy())
        temp_square = temp_hq[:]
        t = 0
        i = 0
        j = 0
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                temp_cat = self.gboard.board[i][j].cat
                match temp_cat:
                    case "CT":
                        self.gboard.board[i][j].color = "white"
                    case "RA":
                        self.gboard.board[i][j].color = "white"
                    case "HQ":
                        self.gboard.board[i][j].color = temp_hq.pop()
                    case "general":
                        self.gboard.board[i][j].color = temp_square[t]
                        t = (t+1)%len(temp_square)
                j+=1
            i+=1

    def genid(self)->str:
        return time.strftime("%Y" + "%b" + "%d" + "%H" + "%M" + "%S").upper()

    def showdest(self, tid: int, steps:int)->list:
        return destination(self.tokenlist[tid].row,self.tokenlist[tid].col,steps,self.gboard.board)
    