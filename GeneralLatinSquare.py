"""
Python code to generate a General Latin Square, implementation by NPO-119
Mathematics of method to generate General Latin Square by Keith Ziss
"""
from random import choice, shuffle
from copy import deepcopy
import sys

#function to generate a random latin square (might want to replace with the jacobson-matthews method)
def rls(n):
    if n <= 0:
        return []
    else:
        symbols = list(range(n))
        square = _rls(symbols)
        return _shuffle_transpose_shuffle(square)


def _shuffle_transpose_shuffle(matrix):
    square = deepcopy(matrix)
    shuffle(square)
    trans = list(zip(*square))
    shuffle(trans)
    return trans


def _rls(symbols):
    n = len(symbols)
    if n == 1:
        return [symbols]
    else:
        sym = choice(symbols)
        symbols.remove(sym)
        square = _rls(symbols)
        square.append(square[0].copy())
        for i in range(n):
            square[i].insert(i, sym)
        return square
# function to return a matrix / square as a string
def _to_text(square):
    if square:
        width = max(len(str(sym)) for row in square for sym in row)
        txt = '\n'.join(' '.join(f"{sym:>{width}}" for sym in row)
                        for row in square)
    else:
        txt = ''
    return txt

def _check(square):
    transpose = list(zip(*square))
    assert _check_rows(square) and _check_rows(transpose), \
        "Not a Latin square"

def _check_rows(square):
    if not square:
        return True
    set_row0 = set(square[0])
    return all(len(row) == len(set(row)) and set(row) == set_row0
               for row in square)

#function to return a '0' filled list of size n where the i'th entry is '1'
    #Example ithzero(3,5) returns [0,0,0,1,0]
def ithzero(i,n):
    zero = [0]*n
    zero[i] = 1
    return zero
def sumup(array):
    sum = 0
    for i in array:
        sum = sum + i
    return sum


#function to generate a RANDOM sm given a cm and size n
def SwapMatrix(cm,n):
    for i in range(len(cm[2])):
        if cm[2][i] > n:
            cm[2][i] = n
        if cm[1][i] < 0:
            cm[1][i] = 0
    summin = sumup(cm[1])
    summax = sumup(cm[2])
    #we have to first check if a SwapMatrix can be generated for a square of size n given the constraint matrix
    if summax<summin:
        raise ValueError('summax < summin\n The sum of the maximums is greater then the size of the Gls')
    if summax < n:
        raise ValueError('summax < n\n The sum of the maximums is less the the size of the Gls')
    if n < summin:
        raise ValueError('n < summin\n The size of the Gls is less then the sum of the minimums')
    #since the inequalities hold true we can generate a swap matrix
    #init the bsm so we can append rows to it as needed
    bsm = []
    # first add to the bsm the minimum number of ithzero rows for each symbol to garuntee that said symbol in cm apears in the gls the minimum number of times as defined by the cm
        #this ensures that in every row and column of the gls each symbol apears the minimum number of times
            #since summin<=n we can do this without problem
    for i in range(len(cm[1])):
        for j in range(cm[1][i]):
            bsm.append(ithzero(i,len(cm[1])))
    #Second step we create a temp matrix which we will eventually append to the bsm
    bsmtemp = [ [ 0 for i in range(len(cm[0])) ] for j in range(n-len(bsm)) ]
    #We create a buffer that keeps track of how many of each symbol we have remaining to assign to each column
        #we use this to make sure we dont go over the limit for each symbol
    r_symbols = []
    for i in range(len(cm[2])):
        r_symbols.append(cm[2][i]-cm[1][i])
    #for each row in bsmtemp we pick one of the symbols that still have some remaining and assign one of them to that row
        # this is possible since summax>=n
    for i in range(len(bsmtemp)):
        r = choice([x for x in range(len(r_symbols)) if r_symbols[x] != 0])
        r_symbols[r] = r_symbols[r]-1
        bsmtemp[i][r] = 1

    # if we have any symbols left over assign them randomly to their column in any spaces that are still 0
        # this step ensures it is possible to generate as many gls as can be generated using this method
    for r in range(len(r_symbols)):
        for i in range(min(r_symbols[r],len(bsmtemp))):
            column = []
            for x in range(len(bsmtemp)):
                column.append(bsmtemp[x][r])
            if len([p for p in range(len(column)) if column[p] == 0]) > 0:
                pick = choice([p for p in range(len(column)) if column[p] == 0])
                bsmtemp[pick][r] = 1
    #append bsmtemp to bsm
    for i in bsmtemp:
        bsm.append(i)
    #convert our bsm into a swap matrix (which is what Gls() is expecting)
    for i in range(len(bsm)):
        for j in range(len(bsm[0])):
            if bsm[i][j] == 1:
                bsm[i][j] = j+1

    return bsm

#functinon to generate a General Latin Square
def Gls(square,cm,sm,n):
    gls = [[0 for i in range(n)]for j in range(n)]
    for x in range(n):
        for y in range(n):
            #ls is the symbol in our latin square at x,y
            ls = square[x][y]
            #we 'swap' ls with a symbol from the first row of the constraint matrix based on the swap matrix
                #we only swap with symbol cm[0][i] iff sm[ls][i] != 0
                #for any 'ls' ther is a non 0 element somewhere in sm[ls]
                #for any 'i' there are at least cm[1][i] 'ls' where sm[ls][i]!=0 and no more then cm[2][i] 'ls' where sm[ls][i]!=0
                #thus the resulting square is a gls that satifies the cm
            gls[x][y] = cm[0][choice([i for i in sm[ls] if i != 0])-1]
    return gls

#function to generate a random general latin square given a constraint matrix 'cm' and size 'n'
def RandGls(cm,n):
    square = rls(n)
    sm = SwapMatrix(cm,n)
    if sm[0] == 'error':
        print(sm[1])
        return sm[1]
    return Gls(square,cm,sm,n)

if __name__ == '__main__':
        n = 17
        cm = [['A','B','C','D'],[0,0,0,0],[8,8,8,8]]
        print(_to_text(cm))
        print()
        for i in range(1):
            print(i+1)
            try:
                print(_to_text(RandGls(cm,n)))
            except:
                print('Cannot generate Gls with given cm')
            print()
