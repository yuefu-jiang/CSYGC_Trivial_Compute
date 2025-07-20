class Wedge:
    def __init__(self, in_size: int):
        """
        This class implement a list of wedge, type of wedges are hard coded to 7 colors
        :param size:total number of types of wedges
        """
        wedgeset = ["red", "blue", "yellow", "green", "orange", "purple", "teal"]
        self.chosen = set()
        self.size = in_size
        for i in range(in_size):
            self.chosen.add(wedgeset[i])

class Token:
    def __init__(self, wedge: Wedge):
        """
        This class implement a token object
        """
        self.label =""
        self.row = -1
        self.col = -1
        self.missing = wedge.chosen.copy()
        self.collection = set()
        self.score = 0
        self.HqOk = True
        self.CenterOk = True
        self.full = False

    def addw(self, item: str):
        self.missing.discard(item)
        self.collection.add(item)
        if len(self.missing) == 0:
            self.full = True

class Square:
    def __init__(self, valid:bool, cat:str):
        """
        This class implement a square on a grid
        :param valid:True or False, for whether it is a legitiamte square
        :param cat:Type of squares:CT for center,HQ for headquarter,RA for roll again, general for other colored squares, invalid for valid=false
        """
        self.valid = valid
        self.cat = cat
        self.color = None

class Trivialboard:
    def __init__(self, size_in:int):
        """
        This class implement a square gameboard represented in a n*n matrix, or a 2D-array
        """
        self.CT = None
        self.board = self.createboard(size_in)

    def createboard(self, size: int)->list:
        #input an integer as size and return a 2-D list
        temp = []
        row = 0
        mid = size // 2
        while row<size:
            temprow=[]
            temp.append(temprow)
            col = 0
            while col<size:
                if row in [0,mid,size-1] or col in [0,mid,size-1]:
                    #center
                    if col == mid and row == mid:
                        temp[row].append(Square(True, "CT"))
                        self.CT = [row,col]
                    #headqarter
                    elif (col + row) % mid == 0 and (col + row) % (size - 1) != 0:
                        temp[row].append(Square(True, "HQ"))
                    #roll again
                    elif (col + row) % (size - 1) == 0 and row != mid:
                        temp[row].append(Square(True, "RA"))
                    #normal
                    else:
                        temp[row].append(Square(True, "NL"))
                else:
                    #invalid squares
                    temp[row].append(Square(False,"IV"))
                col += 1
            row += 1
        return temp
    
    def print_b(self):
        i = 0
        j = 0
        while i < len(self.board):
            while j < len(self.board[i]):
                if self.board[i][j].valid:
                    print(f"[{self.board[i][j].cat}]", end="", flush=True)
                else:
                    print(f"[  ]", end="", flush=True)
                j += 1
            j=0
            print()
            i += 1
    