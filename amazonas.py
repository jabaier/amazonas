# -*- coding: utf-8 -*
import copy
import random
import signal

BLANK='--'
WHITE='W'
BLACK='B'
BLOCKED='XX'

class Board:
    def __init__(self,init_board=None):
        # create an initial board
        if init_board==None:
            self.board=[]
            for i in range(0,10):
                self.board.append([BLANK]*10)
            self.queens = [[3,0],[0,3],[0,6],[3,9],[6,0],[9,3],[9,6],[6,9]]
            num=0
            for q in self.queens:
                if num < 4:
                    ch = BLACK
                else:
                    ch = WHITE
                self.board[q[0]][q[1]] = ch+str(num%4)
                num += 1
        else:
            self.board  = copy.deepcopy(init_board.board)
            self.queens = copy.deepcopy(init_board.queens)

    def __repr__(self):
        s = "   "+"  ".join([str(i) for i in range(0,10)])+"\n"
        for i in range(0,10):
            s += str(i)+" "+" ".join(self.board[i]) + "\n"
        return s

    def succ(self,queen,xf,yf,xb,yb):
         # returns a new board like self but with queen moved to xf,yf and position xb,yb blocked
        bsucc=Board(self)
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        bsucc.queens[queen][0] = xf
        bsucc.queens[queen][1] = yf
        bsucc.board[xf][yf] = bsucc.board[xi][yi]
        bsucc.board[xi][yi] = BLANK
        bsucc.board[xb][yb] = BLOCKED
        return bsucc

    @staticmethod
    def queen2str(q):
        if q<4:
            return BLACK+str(q)
        return WHITE+str(q%4)

    @staticmethod
    def show_move(color,q,xf,yf,xb,yb):
        print("Jugador",color,"mueve reina",q%4,"hasta","("+str(xf)+","+str(yf)+")","bloqueando","("+str(xb)+","+str(yb)+")"+"\n")

    def is_legal_jump(self,q,xi,yi,xf,yf):
        q_str = Board.queen2str(q)
        dx = xf - xi
        dy = yf - yi
        if dx == dy == 0 or (abs(dx)!=abs(dy) and abs(dx)!=0 and abs(dy)!=0):
            return False
        if dx!=0:
            dx //= abs(dx)
        if dy!=0:
            dy //= abs(dy)
        x = xi + dx
        y = yi + dy
        while True:
            if self.board[x][y] != BLANK and self.board[x][y] != q_str:
                return False
            if (x,y) == (xf,yf):
                break
            x += dx
            y += dy

        return True


    def is_legal_move(self,queen,xf,yf):
        # true iff queen queen can move to xf to yf
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        return self.is_legal_jump(queen,xi,yi,xf,yf)

    def can_play(self,color):
        return self.moves(color,1)!=[]

    def moves(self,color,limit=100000):
        n = 0
        if color==BLACK:
            queens = range(0,4)
        else:
            queens = range(4,8)
        moves = []
        for q in queens:
            queen_str=color+str(q%4)
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx==dy==0:
                        continue
                    xf=self.queens[q][0]+dx
                    yf=self.queens[q][1]+dy
                    while 0<=xf<10 and 0<=yf<10:
                        if self.board[xf][yf] != BLANK:
                            break
                        for ddx in [-1,0,1]:
                            for ddy in [-1,0,1]:
                                if ddx==ddy==0:
                                    continue
                                xb=xf+ddx
                                yb=yf+ddy
                                while 0<=xb<10 and 0<=yb<10:
                                    if self.board[xb][yb] != BLANK and self.board[xb][yb] != queen_str:
                                        break
                                    moves.append((q,xf,yf,xb,yb))
                                    n += 1
                                    if n == limit:
                                        return moves
                                    xb += ddx
                                    yb += ddy
                        xf += dx
                        yf += dy
        return moves

class HumanPlayer:
    def __init__(self,color):
        self.color = color

    def play(self):
        while True:
            q = int(input("Jugador, "+self.color+" ingrese número de reina a mover (0-4): "))
            if q in range(0,5):
                break
            print("Input no válido")

        if self.color == WHITE:
            q += 4
        while True:
            inp = input("Jugador, "+self.color+" ingrese posición de destino (fila columna): ")
            l=inp.split()
            xf=int(l[0])
            yf=int(l[1])
            if not xf in range(0,10) or not yf in range(0,10):
                print("Posición fuera del tablero")
                continue
            if main_board.is_legal_move(q,xf,yf):
                break
            print("Movida ilegal")


        while True:
            inp = input("Jugador, "+self.color+" ingrese posición de bloqueo (fila columna): ")
            l=inp.split()
            xb=int(l[0])
            yb=int(l[1])
            if not xb in range(0,10) or not yb in range(0,10):
                print("Posición fuera del tablero")
                continue
            if main_board.is_legal_jump(q,xf,yf,xb,yb):
                break;
            print("Posición ilegal",xf,yf,xb,yb)
        return q,xf,yf,xb,yb

class RandomPlayer:
    def __init__(self,color,time=1):
        self.color = color
        self.time = time

    def play(self):
        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)

        try:  ## here we do the hard computation
            moves=main_board.moves(self.color)
            x=0
            while self.time!=0:  # pretend we are doing something unless time is 0
                x=x+1

        except IOError: ## Aqui se recibe la signal de que se nos acabo el tiempo.
            signal.alarm(0)

        # Aqui debieramos dejar la movida que decidimos hacer ahora que se nos acabo el tiempo.
        q,xf,yf,xb,yb = random.choice(moves)

        if not main_board.is_legal_move(q,xf,yf) or not main_board.is_legal_jump(q,xf,yf,xb,yb):
            print("--------------------movida ilegal!??!")
            input("")
        return q,xf,yf,xb,yb

class HeuristicSimulator:
    def __init__(self, board):
        self.board = board

    @staticmethod
    def invertColor(color):
        if(color == BLACK):
            return WHITE
        else:
            return BLACK

    @staticmethod
    def getHeuristic(board, myColor, opColor):

        my_moves = len(board.moves(myColor))
        opponent_moves = len(board.moves(opColor)) + 0.001

        return my_moves / opponent_moves

    @staticmethod
    def pickBestMove(board, color, moves):

        opponent_color = HeuristicSimulator.invertColor(color)
        maxH = 0;

        kMax = 50

        if (kMax > len(moves)):
            kMax = len(moves)

        rndMoves = random.sample(moves, kMax)

        q, xf, yf, xb, yb = rndMoves[0]

        for move in rndMoves:

            #print("Move: " + str(move))

            q_, xf_, yf_, xb_, yb_ = move

            aux_board = board.succ(q_, xf_, yf_, xb_, yb_)

            current_H = HeuristicSimulator.getHeuristic(aux_board, color, opponent_color)

            if(current_H > maxH):
                #print ("Superado maxH")
                maxH = current_H
                q, xf, yf, xb, yb = q_, xf_, yf_, xb_, yb_

        return q, xf, yf, xb, yb

    @staticmethod
    def pickRandomMove(board, color, moves):
        return random.choice(moves)

    # You use this to simulate a playthrough to the end with the heuristic.
    # It will return 1 if it won the playthrough, -1 if it lost.
    # The heuristic is stochastic, therefore it won't always win or lose.
    @staticmethod
    def simulate(board, movingColor):

        currentColor = movingColor

        currentMoves = board.moves(currentColor)

        doRandom = False

        while(len(currentMoves) > 0):

            if(doRandom):
                q, xf, yf, xb, yb = HeuristicSimulator.pickRandomMove(board, currentColor, currentMoves)
            else:
                q, xf, yf, xb, yb = HeuristicSimulator.pickBestMove(board, currentColor, currentMoves)
                #q, xf, yf, xb, yb = HeuristicSimulator.pickRandomMove(board, currentColor, currentMoves)

            board = board.succ(q, xf, yf, xb, yb)

            currentColor = HeuristicSimulator.invertColor(currentColor)

            currentMoves = board.moves(currentColor)

        if(currentColor == movingColor):
            return -1
        else:
            return 1


from math import sqrt, log


class Nodo:
    kOptions = 10

    def __init__(self, board, color, parent=None, action=None):
        self.N = 1;
        self.Q = 0;
        self.sons = []  # Futuro HEAP

        self.board = board
        self.color = color

        kOpt = 5  # = kOptions

        #self.moves = random.sample(self.moves, kOpt)
        self.moves = Nodo.buildGoodMoves(board, color, kOpt)

        self.parent = parent
        self.action = action

        #self.ID = globalID
        #globalID += 1

    @staticmethod
    def buildGoodMoves(board, color, kOpt):
        moves = board.moves(color)

        if (kOpt > len(moves)):
            kOpt = len(moves)

        beRandom = False

        if(beRandom):
            return random.sample(moves, kOpt)

        expansionRateOfKOpt = 10

        moves = random.sample(moves, min(expansionRateOfKOpt * kOpt, len(moves)))

        opColor = HeuristicSimulator.invertColor(color)

        movesHeap = []

        for move in moves:
            q, xf, yf, xb, yb = move

            moveBoard = board.succ(q, xf, yf, xb, yb)

            moveH = HeuristicSimulator.getHeuristic(moveBoard, color, opColor)

            #print("Heuristic of " + str(move) + " = " + str(moveH))

            MaxHeap.push(movesHeap, move, moveH)
            #heappush(movesHeap, (-moveH, move))

        bestMoves = []

        for i in range(0, min(kOpt, len(movesHeap))):
            moveIsH, moveI = MaxHeap.pop(movesHeap)#heappop(movesHeap)

            #print("Heuristica del mov #" + str(i) + ":" + str(-moveIsH))

            bestMoves = bestMoves + [moveI]

        return bestMoves

    def getMonteCarloValue(self):
        value1 = self.getRealValue()

        value2 = 2 * log(self.parent.N + 1)

        value2 /= self.N

        value2 = sqrt(value2)

        #C_p, sujeto a cambios segun conveniencia
        c_p = 1 / sqrt(2)

        return value1 + c_p * value2

    def getRealValue(self):
        return float(self.Q) / self.N

    def isNotTerminal(self):

        iHaveMoves = self.moves != [] or self.sons != []

        opHasMoves = self.board.moves(MCPlayer.invertColor(self.color), limit=1) != []

        return iHaveMoves and opHasMoves

    #def __str__(self):

        #tabs = self.tabs()

        #return self.parent.tabs() + "\n" + self.

    def tabs(self):
        if(self.parent == None):
            return " "
        else:
            return self.parent.tabs() + " "

from heapq import heappop, heappush

minusInfinity = -100000000
debugHeap = False
showHeaps = False

class MaxHeap:
    @staticmethod
    def push(heap, element, weight):
        heappush(heap, (-weight, element))
        if(debugHeap):
            print("Inserting " + str(element) + " in heap, with key = " + str(weight))
            if(showHeaps):
                print("Heap: " + str(heap))

    @staticmethod
    def pop(heap):
        if(showHeaps):
            print("Popping from Heap: " + str(heap))

        weightElement = heappop(heap)
        wEle = (-weightElement[0], weightElement[1])
        if(debugHeap):
            print("Popped " + str(wEle[1]) + " from heap, with key = " + str(wEle[0]))
        return wEle

class MCPlayer:
    def __init__(self, color, time=1):
        self.color = color
        self.time = time

    @staticmethod
    def invertColor(color):
        if (color == BLACK):
            return WHITE
        else:
            return BLACK

    @staticmethod
    def expand(v):
        q, xf, yf, xb, yb = v.moves[0]

        newBoard = v.board.succ(q,xf,yf,xb,yb)

        nuevo = Nodo(newBoard, MCPlayer.invertColor(v.color), parent=v, action = (q, xf, yf, xb, yb));

        v.moves.remove((q, xf, yf, xb, yb))

        newbieKey = 1000000000

        MaxHeap.push(v.sons, nuevo, newbieKey)
        #heappush(v.sons, (-minusInfinity, nuevo))

        return nuevo

    @staticmethod
    def backup(v, delta, k_sim):

        debugBackup = False

        parent = v.parent

        if(debugBackup):
            print("Fue simulado nodo " + str(v) + ", de color " + v.color)
            print("Puntaje obtenido: " + str(delta) + ". #Simulaciones: " + str(k_sim))

        while(parent != None):

            MaxHeap.pop(parent.sons)
            #heappop(parent.sons) #Sacamos a v del tope del heap
            v.N += k_sim
            v.Q += delta

            v_value = v.getMonteCarloValue()

            if(debugBackup):
                print("Nodo gano %2.2f" % delta + " de puntaje. Nuevo puntaje = %2.2f" % v_value)

            #print("Montecarlo value: " + str(v_value))

            MaxHeap.push(parent.sons, v, v_value)
            #heappush(parent.sons, (0 - v_value, v))
            #Volvemos a poner a v, pero con su valor actualizado
            #Como tenemos un minHeap, hay que invertir las prioridades.

            v = parent

            parent = v.parent

            delta = k_sim - delta
            #Negacion de delta. Delta va de 0 a k_sim. neg(delta) es lo que le falto, ie, las veces que perdio

    @staticmethod
    def TreePolicy(raiz):
        v = raiz

        while(v.isNotTerminal()):
            if(v.moves != []):
                #print("Expandiendo un nodo...")
                return MCPlayer.expand(v)
            else:
                #print("Tomando primer hijo de un nodo...")
                wot, v = v.sons[0] #Wot es la prioridad (no usada, v es el Nodo

        return v

    @staticmethod
    def worstAction(v):
        min_value = 2
        worst_action = None

        for mcValue, v_prime in v.sons:

            v_prime_value = v_prime.getRealValue()

            if(v_prime_value < min_value):
                worst_action = v_prime.action
                min_value = v_prime_value

        print("Min value: %2.2f" % min_value)
        print("Worst action: " + str(worst_action))

        return worst_action

    @staticmethod
    def bestSafeAction(v):
        min_higher_enemy_value = 2

        safest_action = None

        for mcValue, v_prime in v.sons:

            max_enemy_value_in_v_prime, best_enemy_move_in_v_prime = MCPlayer.bestActionAndValue(v_prime)

            if(best_enemy_move_in_v_prime != None and max_enemy_value_in_v_prime < min_higher_enemy_value):
                safest_action = v_prime.action
                min_higher_enemy_value = max_enemy_value_in_v_prime

        print("Min higher bound on enemy value: %2.2f" % min_higher_enemy_value)
        print("Safest action: " + str(safest_action))

        return safest_action

    @staticmethod
    def usingNInsteadOfRV():
        return False

    @staticmethod
    def bestActionAndValue(v):
        #return MCPlayer.worstAction(v)

        max_value = -1
        best_action = None

        useNInsteadOfRV = MCPlayer.usingNInsteadOfRV()

        for mcValue, v_prime in v.sons:

            if(useNInsteadOfRV):
                v_prime_value = v_prime.N
            else:
                v_prime_value = v_prime.getRealValue()


            if(v_prime_value > max_value):
                best_action = v_prime.action
                max_value = v_prime_value

        print("Max value: %2.2f" % max_value)
        print("Best action: " + str(best_action))

        return (max_value, best_action)

    @staticmethod
    def bestAction(v):
        #return MCPlayer.worstAction(v)
        #return MCPlayer.bestSafeAction(v)

        max_value = -1
        best_action = None

        useNInsteadOfRV = MCPlayer.usingNInsteadOfRV()

        for mcValue, v_prime in v.sons:

            if(useNInsteadOfRV):
                v_prime_value = v_prime.N
            else:
                v_prime_value = v_prime.getRealValue()


            if(v_prime_value > max_value):
                best_action = v_prime.action
                max_value = v_prime_value

        print("Max value: %2.2f" % max_value)
        print("Best action: " + str(best_action))

        return best_action

    def play(self):
        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)
        #signal.alarm(0)

        v0 = Nodo(main_board, self.color)

        welp = 0

        try:  ## here we do the hard computation

            j = 0

            k_sim = 1

            while(True):
                j += 1
                #print("It #" + str(j))

                v_next = MCPlayer.TreePolicy(v0)

                #print("V_next = " + str(v_next))

                delta = 0

                for i in range (0, k_sim):
                    delta += HeuristicSimulator.simulate(v_next.board, v_next.color)

                MCPlayer.backup(v_next, delta, k_sim)

                welp += 1

        except IOError: ## Aqui se recibe la signal de que se nos acabo el tiempo.
            signal.alarm(0)

        print("Did %d" % j + " iterations.")

        welpThresh = 3

        try:
            q,xf,yf,xb,yb = MCPlayer.bestAction(v0)
        except TypeError:
            print("Failed to pick a best action. Choosing at random!")
            q, xf, yf, xb, yb = random.choice(main_board.moves(self.color))

        if not main_board.is_legal_move(q,xf,yf) or not main_board.is_legal_jump(q,xf,yf,xb,yb):
            print("--------------------movida ilegal!??!")
            input("")
        return q,xf,yf,xb,yb


class HeuristicPlayer:
    def __init__(self, color, time=1, numLookAhead = 1):
        self.color = color
        self.time = time
        self.numLookAhead = numLookAhead

    @staticmethod
    def invertColor(color):
        if(color == BLACK):
            return WHITE
        else:
            return BLACK

    def play(self):
        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)

        try:
            moves = main_board.moves(self.color)
            q, xf, yf, xb, yb = q_, xf_, yf_, xb_, yb_ = random.choice(moves)

            opponent_color = HeuristicPlayer.invertColor(self.color)
            maxH = 0;

            kMax = self.numLookAhead

            if(kMax > len(moves) - 1):
                kMax = len(moves) - 1

            for i in range(0, kMax):

            #while(len(moves) > 1):
                #if(len(moves) <= 1):
                #    break;
                moves.remove((q_, xf_, yf_, xb_, yb_))

                aux_board = main_board.succ(q_, xf_, yf_, xb_, yb_)

                moves_opponent = aux_board.moves(opponent_color)

                moves_me = aux_board.moves(self.color)

                current_H = (len(moves_me)) / (len(moves_opponent) + 0.001)

                if(current_H > maxH):
                    #print("Bested maxH! New maxH: " + str(current_H))
                    maxH = current_H
                    q, xf, yf, xb, yb = q_, xf_, yf_, xb_, yb_

                q_, xf_, yf_, xb_, yb_ = random.choice(moves)


        except IOError:
            signal.alarm(0)

        if not main_board.is_legal_move(q, xf, yf) or not main_board.is_legal_jump(q, xf, yf, xb, yb):
            print("--------------------movida ilegal!??!")
            input("")

        return q,xf,yf,xb,yb


### Main Program

main_board=Board()

globalID = 10000

nWinsH = 0

for i in range(0, 0):
    print("Simulando instancia #" + str(i))
    nWinsH += HeuristicSimulator.simulate(main_board, BLACK)
    print("N Wins H: " + str(nWinsH))

print("Black gana " + str(nWinsH) + " veces usando la heuristica")

player_white = HeuristicPlayer(WHITE,60, numLookAhead=60)
#player_white = RandomPlayer(WHITE,60)
player_black = MCPlayer(BLACK, 120)
#HeuristicPlayer(BLACK,1, numLookAhead=10)

plays = 0

while True:
    print(main_board)
    if main_board.can_play(WHITE):
        q,xf,yf,xb,yb = player_white.play()
        Board.show_move(WHITE,q,xf,yf,xb,yb)
        plays += 1
    else:
        print("Jugador",BLACK,"ha ganado")
        break
    main_board = main_board.succ(q,xf,yf,xb,yb)
    print(main_board)
    if main_board.can_play(BLACK):
        q,xf,yf,xb,yb = player_black.play()
        Board.show_move(BLACK,q,xf,yf,xb,yb)
        plays += 1
    else:
        print("Jugador",WHITE,"ha ganado")
        break
    main_board = main_board.succ(q,xf,yf,xb,yb)

print("Fin del juego en",plays,"jugadas.")
