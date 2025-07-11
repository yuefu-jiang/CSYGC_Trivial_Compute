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
        self.wedgelist: Wedge

    def initialize(self, gameid:str, playerlist:list , q_type = 4, b_size=9):
        """
        game initialization
        """
        #cleanup existing list
        self.tokenlist.clear()
        self.wedgelist = None
        #get/generate a game id
        self.gameid=gameid
        #store all game paremeters
        self.boardsize = b_size
        self.playerno = len(playerlist)
        self.wedgelist = Wedge(q_type)
        #generate the game board
        self.gboard = Trivialboard(self.boardsize)
        self.gboard.print_b()
        #assign color to squares
        self.coloring()
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
            print(self.tokenlist[i].label,self.tokenlist[i].row,self.tokenlist[i].col)
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
                    case "NL":
                        self.gboard.board[i][j].color = temp_square[t]
                        t = (t+1)%len(temp_square)
                j+=1
            i+=1

    def showdest(self, tid: int, steps:int)->list:
        """
        :param tid: id number of player (0/1/2....)
        :parem steps: how many steps to take
        """
        return destination(self.tokenlist[tid].row,self.tokenlist[tid].col,steps,self.gboard.board)

    def movetoken(self, tid: int, location:list):
        """
        :param tid: id number of player (0/1/2....)
        :parem location: coordinates of the destination, [i,j]
        """
        self.tokenlist[tid].row = location[0]
        self.tokenlist[tid].col = location[1]
        