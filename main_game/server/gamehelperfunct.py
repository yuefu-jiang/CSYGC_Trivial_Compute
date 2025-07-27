import random

def rolldice(x=1)->int:
    return x*random.randint(1,6)

def printlist(plist: list):
    i = 0
    j = 0
    while i < len(plist):
        while j < len(plist[i]):
            print(plist[i][j].row,plist[i][j].col,plist[i][j].valid,plist[i][j].cat,",", end="")
            j += 1
        j=0
        print()
        i += 1

def destination(row_now:int, col_now, steps:int, blist: list, row_bef=None, col_bef=None)->list:
    """input current coordinates, steps, gameboard object and output list of possible destinations
    :param row_now:current row
    :param col_now:current col
    :param steps:number of steps
    :param blist: list object of gameboard
    :param row_bef:previous row value, not for caller
    :param col_bef:previous col value, not for caller
    output format in [[1,2],[3,4]]
    """
    dlist = []
    #base case
    if steps == 0:
        #dlist.append([row_now,col_now])
        dlist.append(posConvert([row_now,col_now]))
    #recursive case
    elif steps > 0:
        if row_bef is None and col_bef is None:
            row_bef=row_now
            col_bef=col_now
        for i in [1, -1]:
            j =0
            if 0<=row_now+i < len(blist) and 0<=col_now+j < len(blist):
                if blist[row_now+i][col_now+j].valid and [row_now+i,col_now+j] != [row_bef,col_bef] :
                    dlist = dlist + destination(row_now+i,col_now+j, steps - 1, blist, row_now, col_now)
        for j in [1, -1]:
            i = 0
            if 0<=row_now+i < len(blist) and 0<=col_now+j < len(blist):
                if blist[row_now+i][col_now+j].valid and [row_now+i,col_now+j] != [row_bef,col_bef] :
                    dlist = dlist + destination(row_now+i,col_now+j, steps - 1, blist, row_now, col_now)
    return dlist

def posConvert(pos:list)->str:
    return str(pos[0])+","+str(pos[1])

def poskeyTolist(input:str)->list:
    #input format is string : "1,99"
    temp = list()
    temp.append(int(input[:input.find(",")]))
    temp.append(int(input[input.find(",")+1:]))
    return temp