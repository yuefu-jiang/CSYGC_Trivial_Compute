# Server

## Current Server Package and Layout

The game object classes are all under gameobject.py

* [server/](.): The parent server folder.
    * [README.md](README):
    * `__init__.py` 
    * `__main__.py`
    * `server.py`
    * `gameinstance.py` 
        This the highest level game instance object
    * `gamehelperfunct.py` 
        This is just some methods to help running the gameinstance objects
    * `gameobject.py` 
        This is the child class for the game instance class 

## game piece component and object class

* GameInstance
    * Trivialboard
        * Square
    * Wedge
    * Token 

Implemented class and their attributesfor now:

Wedge: This class implement a list of wedge, type of wedges are hard coded to 7 colors "red", "blue", "yellow", "green", "orange", "purple", "teal"

        chosen = chosen set
        size = number of colors used

Token: This class implement a token object, attributes:

       label = For storing name
        row = row number on the game board
        col = column number on the game board
        missing = Set of wedges pending collection
        collection = Set of wedges collected
        score = score number
        HqOk = Boolean, for condition checking
        CenterOk = Boolean, for condition checking
        full = Boolean, for condition checking 

Square: This class implement a square on a grid

        valid:True or False, for whether it is a legitiamte square
        cat:Type of squares:CT for center,HQ for headquarter,RA for roll again, general for other colored squares, invalid for valid=false
        color:color of the square, to be assigned by gameinstance

Trivialboard: This class implement a square gameboard represented in a n*n matrix, or a 2D-array

        CT = the Center of the gameboard
        board = the gameboard itself, in a 2D-array
            |0  |1  |...|n-1|
        |0  |
        |1  |
        |...|
        |n-1|

GameInstance: This class implement a game object containing all necessary instance and attributes of game

        gboard = the gameboard object
        gameid = an id
        boardsize = size of board, just the width, assume square shape
        playerno = number of players
        tokenlist = list of token objects
        wedgelist = the list of wedge to be used in each game

## Input and Output format:


### Example input and output

>Pending
> 
>example : `example`
