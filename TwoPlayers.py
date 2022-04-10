NULL = 0
import copy
from re import I
from numpy import Inf
import pygame
import sys
import interface2
import math
import time
import pickle

SEARCH_DEPTH = 2
OPENING_DEPTH = 9
MOVE_COUNT = 0

class MoveNode:
    def __init__(self, piece, target):
        self.piece = piece # the piece that is moved
        self.target = target # the space the piece is moved to
        self.occurrences = 0
        self.winrate = 0
        self.children = [] # stored as moveNodes

    def getChildren(self):
        return self.children

    def getOccurrences(self):
        return self.occurrences
 
    def getWinRate(self):
        return self.winrate

    def __str__(self):
        return("MoveNMode: " + str(self.piece) + "->"+ str(self.target))

    def updateWin(self):
        self.occurrences += 1
        self.winrate = self.winrate + ((1 - self.winrate) / self.occurrences)

    def updateLose(self):
        self.occurrences += 1
        self.winrate = self.winrate + ((0 - self.winrate) / self.occurrences)

    def addChild(self, newNode):
        self.children.append(newNode)

    def equals(self, compare):
        if self.piece == compare.piece and self.target == compare.target:
            return True
        return False

# make an opening tree, that is just a root node
opening_winrates = MoveNode("root", "root") 
print("made opening tree " + str(opening_winrates))

# load the opening tree if there is one saved
winrate_file = open('opening_tree.txt', 'rb')
opening_winrates = pickle.load(winrate_file)
winrate_file.close()

def saveOpeningTree():
    print("saving opening Tree")

    # just print the tree as we're saving it for information's sake
    print("here are the moves in the tree :")
    for openingMove in opening_winrates.children:
        print(str(openingMove) + " wr = " + str(openingMove.getWinRate()) + " K = " + str(openingMove.getOccurrences()))

    winrate_file = open('opening_tree.txt', 'wb')
    pickle.dump(opening_winrates, winrate_file) # this will just save the opening winrates object generated at startup :)
    winrate_file.close()

print("here are the moves in the tree :")
for openingMove in opening_winrates.children:
    print(str(openingMove) + " wr = " + str(openingMove.getWinRate()) + " K = " + str(openingMove.getOccurrences()))


# make a list of all the moves played throughout the game so far
played_moves = []

currentMove = opening_winrates
print("====currentMove is " + str(currentMove))
print(currentMove is opening_winrates)

def findOpeningCandidate():
    print("finding a candidate for current move = " + str(currentMove))
    bestCandidate = False
    bestValuation = False
    for candidate in currentMove.children:
        print("looking at candidate: " + str(candidate))
        if candidate.occurrences == 0:
            print("returning" + str(candidate) + " because it has no occurrences..." )
            return candidate # we need *some* data on this opening!
        # exploration vs exploitation. 
        # c = math.sqrt(2) # this is the recommended value but while I'm exploring I will use the following
        c = 2
        valuation = (candidate.winrate + (c * (math.log(currentMove.occurrences)/candidate.occurrences)))
        print("valuation is: " + str(valuation))
        if valuation > bestValuation:
            bestCandidate = candidate
            bestValuation = valuation

    return bestCandidate


def updateWinrateTree(i):
    print("winner was player " + str(i))
    tracer = opening_winrates
    index = (i - 1) #0 for a player 1 win, 1 for a player 2 win
    for pMove in played_moves:
        for stat in tracer.children:
            if pMove.equals(stat):
                if (index % 2):
                    stat.updateLose()
                    print("adding a Loss to " + str(stat))
                    print("now it has wr = " + str(stat.winrate) + " and k = "+ str(stat.occurrences))
                else:
                    stat.updateWin()
                    print("adding a win to " + str(stat))
                    print("now it has wr = " + str(stat.winrate) + " and k = "+ str(stat.occurrences))
                index += 1
                tracer = stat
                break
    saveOpeningTree()



color_light = (202, 203, 213 )
color_dark = (2, 6, 145)
def TwoPlayers(p1, p2):
    global currentMove
    pygame.init()
    import numpy

    last_jumped = [-1, -1]

    # remplir la matrice avec des 1
    matrix = numpy.ones((17, 25))
    # remplir la matrice avec des -1
    matrix *= -1
    # les positions des pions dans la matrice pour chaque joueur

    first_player = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    second_player = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
    # des indexs pour le deplacement
    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]

    #modification de la matrice
    #changer des -1 par des 0 pour les cases de l'etoile
    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                matrix[i][j] = matrix[16 - i][j] = 0

                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 - i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    # modification matrice : 1 pour joueur numero 1 ,2 pour joueur numero 2....
    def add_player(index):
        if index == 1:
            for i in range(len(first_player)):
                matrix[first_player[i][0]][first_player[i][1]] = index
        if index == 2:
            for i in range(len(second_player)):
                matrix[second_player[i][0]][second_player[i][1]] = index

    # l'ajout des pions de chaque joueur
    class remplissage:
        def __init__(self):
            self_x = 0
            self_y = 0

        def pion(self):
            colors = [(240, 230, 230), "red", "green"]
            for i in range(0, 17):
                for j in range(0, 25):
                    if matrix[i][j] >= 0:
                        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))

    # les pas possibles

    def valid_moves(coor):
        valid_index = []
        for i in range(len(move_index)):
            x = coor[0] + move_index[i][0]
            y = coor[1] + move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    check_path(move_index[i], x, y, valid_index)
        return valid_index

    # les sauts possibles
    def check_path(path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(move_index)):
                        x3 = x2 + move_index[j][0]
                        y3 = y2 + move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    check_path(move_index[j], x3, y3, moves_array)

    # pour faire le mouvement
    def move(pos, target):
        global MOVE_COUNT
        MOVE_COUNT += 1
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    # les coordonnees parraport a la grille
    def get_token_coor(x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor

    # l'annimation des deplasssements possibles
    def animation(moves=[], clicked_token=None):
        colors = [(240, 230, 230), "red", "green"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_cercle = pygame.image.load('./imgs/cercle.png')
                    test_cercle = pygame.transform.scale(test_cercle, (CELL_SIZE, CELL_SIZE))
                    screen.blit(test_cercle, (j * CELL_SIZE, i * CELL_SIZE))
    #la grille
    def show_grille():
        for i in range(0, nb_col):
            for j in range(0, nb_ligne):
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)

    # fonction pour ajouter un text a l'ecran
    def WriteText(text, text_pos_x, text_pos_y, text_size, col):
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        screen.blit(text_render, (text_pos_x, text_pos_y))

    # afficher le gagnant
    def winner():
        first = True
        second= True
        for i in range(len(first_player)):
            if matrix[first_player[i][0]][first_player[i][1]] != 2:
                second= False
                break
        for i in range(len(second_player)):
            if matrix[second_player[i][0]][second_player[i][1]] != 1:
                first = False
                break
        if second == True:
            WriteText('Player 2 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 130, 50, 'green')
            updateWinrateTree(2)
            saveOpeningTree()
            print("FINAL MOVE COUNT: " + str(MOVE_COUNT))
            return True

        elif first == True :
            WriteText('Player 1 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 130, 50,'red')
            updateWinrateTree(1)
            saveOpeningTree()
            print("FINAL MOVE COUNT: " + str(MOVE_COUNT))
            return True
        else:
            return False

    add_player(1)
    add_player(2)
    # l'affichage de la fenetre du jeu
    nb_col = 25
    nb_ligne = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(size=(nb_col * CELL_SIZE, nb_ligne * CELL_SIZE))
    timer = pygame.time.Clock()
    game_on = True
    pions_rect = []

    players = remplissage()

    player_1_goals = [(16,12), (15,11), (15,13), (14,10), (14,12), (14,14), (13,9), (13,11), (13,13), (13,15)] # goals hard-coded for easier access -- it's not like they will change
    player_2_goals = [(0,12), (1,11), (1,13), (2,10), (2,12), (2,14), (3,9), (3,11), (3,13), (3,15)] 

    screen.fill(pygame.Color("white"))
    players.pion()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []



    def distance(target, destination):
        # literally just pythagorean theorem :)
        return math.sqrt((target[0] - destination[0])**2 + (target[1] - destination[1])**2)

    def heuristic(state, players):
        heuristic_value = 0
        player_1_pawns = []
        player_2_pawns = []

        # go through the whole board and get each player's pawns
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 1:
                    bigTuple = (i,j)
                    player_1_pawns.append(bigTuple)
                elif state[i][j] == 2:
                    bigTuple = (i,j)
                    player_2_pawns.append(bigTuple)
        #now the pawns arrays have all known pawns

        #update for player1
        
        for goal in player_1_goals:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_1_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            heuristic_value += lowestDistance
            player_1_pawns.remove(closestPawn)


        player2Val = 0
        #update for player2
        for goal in player_2_goals:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_2_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player2Val -= lowestDistance
            player_2_pawns.remove(closestPawn)


        # re-stock pawns arrays
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 1:
                    bigTuple = (i,j)
                    player_1_pawns.append(bigTuple)
                elif state[i][j] == 2:
                    bigTuple = (i,j)
                    player_2_pawns.append(bigTuple)

        alternate_heuristic = 0
        #update for player1
        player_1_goals_inverse = [(16,12), (15,13), (15,11), (14,14), (14,12), (14,10), (13,15), (13,13), (13,11), (13,9)]
        for goal in player_1_goals_inverse:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_1_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            alternate_heuristic += lowestDistance
            player_1_pawns.remove(closestPawn)

        
        if alternate_heuristic > heuristic_value:
            heuristic_value = alternate_heuristic

        alternate_heuristic = 0
        #update for player2
        player_2_goals_inverse = [(0,12), (1,13), (1,11), (2,14), (2,12), (2,10), (3,15), (3,13), (3,11), (3,9)] 
        for goal in player_2_goals_inverse:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_2_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            alternate_heuristic += lowestDistance
            player_2_pawns.remove(closestPawn)



        if alternate_heuristic > abs(player2Val):
            player2Val = 0 - alternate_heuristic
        heuristic_value = heuristic_value + player2Val

        # print("current Heuristic: " + (-heuristic_value)
        return (-heuristic_value)

    def alpha_beta_reg(state1, toMoveId):
        global currentMove #look I'm just gonna use this globally I don't wanna write getters and setters


        playerMoves = []
        for i in range(len(state1)):
            for j in range(len(state1[i])):
                if state1[i][j] == toMoveId:
                    playerMoves.append([i, j])
        v = -Inf
        move = [-1, -1]
        initial = [-1, -1]
        for i in playerMoves:
            player_valid_moves = valid_moves(i)
            for a in player_valid_moves:
                #add this move to the move list
                if (len(played_moves) < OPENING_DEPTH):
                    newMoveNode = MoveNode(i, a)
                    candidateFound = False
                    for child in currentMove.children:
                        if newMoveNode.equals(child):
                            candidateFound = True
                    if not candidateFound:
                        currentMove.addChild(newMoveNode)
                        print("ADDING A NEW NODE")




        if(len(played_moves) < OPENING_DEPTH):
            bestCandidate = findOpeningCandidate()

            if bestCandidate != False:
                return[bestCandidate.target, bestCandidate.piece]


        state = copy.deepcopy(state1)
        if (toMoveId == 1):
            value = max_value(state, -Inf, Inf, 1)
        elif (toMoveId == 2):
            value = min_value(state, -Inf, Inf, 1)
        return [value[1], value[2]]

    def max_value(state, alpha, beta, depth):
        p1 = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 1:
                    p1.append([i, j])
        if (depth >= SEARCH_DEPTH):
            return [heuristic(state, [[1, [16, 12]], [2, [0, 12]]]), NULL, NULL]
        v = -Inf
        move = [-1, -1]
        initial = [-1, -1]
        for i in p1:
            player_valid_moves = valid_moves(i)
            for a in player_valid_moves:
                #add this move to the move list
                if (len(played_moves) < OPENING_DEPTH):
                    newMoveNode = MoveNode(i, a)
                    candidateFound = False
                    for child in currentMove.children:
                        if newMoveNode.equals(child):
                            candidateFound = True
                    if not candidateFound:
                        currentMove.addChild(newMoveNode)
                        print("ADDING A NEW NODE")


                v2 = min_value(move2(state, i, a), alpha, beta, depth+1)
                if (v2[0] > v):
                    v = v2[0]
                    move = a
                    initial = i
                    if (v > alpha): alpha = v
                if (v >= beta):
                    return [v, move, initial]
        return [v, move, initial]

    def min_value(state, alpha, beta, depth):
        p2 = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 2:
                    p2.append([i, j])
        if (depth >= SEARCH_DEPTH):
            return [heuristic(state, [[1, [16, 12]], [2, [0, 12]]]), NULL, NULL]
        v = +Inf
        move = [-1, -1]
        initial = [-1, -1]
        for i in p2:
            player_valid_moves = valid_moves(i)
            for a in player_valid_moves:
                v2 = max_value(move2(state, i, a), alpha, beta, depth+1)
                if (v2[0] < v):
                    v = v2[0]
                    move = a
                    initial = i
                    if (v < beta): beta = v
                if (v <= alpha): 
                    return [v, move, initial]
        return [v, move, initial]

    def move2(mx, pos, target):
        matrix = copy.deepcopy(mx)
        if(matrix[target[0]][target[1]] == 0):
            matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
            matrix[pos[0]][pos[1]] = 0
            return matrix
        else:
            return mx
    
    # fonction boutton pour le retour a la fenetre precedente
    def text_objects(text, font):
        textsurface =font.render(text,True , "white")
        return textsurface , textsurface.get_rect()
    def button(msg, x, y, w, h, ic, ac, action=None):

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)

    while game_on:
        # player turn
        if player_index == 2: col = 'green'
        if player_index == 1: col = 'red'
        if (winner() == False):
            WriteText('Player ' + str(player_index) + '\'s Turn', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, col)

            if (MOVE_COUNT > 180): # the game probably stalled out
                print("-------- game stalled out -------------")
                heur = heuristic(matrix, [[1, [16, 12]], [2, [0, 12]]])
                print("heuristic is " + str(heur))
                if heur  > 0:
                    WriteText('Player 1 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 130, 50, 'green')
                    updateWinrateTree(1)
                    saveOpeningTree()
                    print("FINAL MOVE COUNT: " + str(MOVE_COUNT))
                    return True
                else:
                    WriteText('Player 2 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 130, 50, 'green')
                    updateWinrateTree(2)
                    saveOpeningTree()
                    print("FINAL MOVE COUNT: " + str(MOVE_COUNT))
                    return True

        else:
            #time.sleep(5) TODO: Add this back :)
            return()
        
        if (player_index == 1 and p1 == "ai"):
            print("<< Player 1")
            print("current heuristic is")
            print(heuristic(matrix, [[1, [16, 12]], [2, [0, 12]]]))
            temp = alpha_beta_reg(matrix, 1)
            print("chose the move: ")
            #print(temp)

            # add the move to played moves
            if len(played_moves) < OPENING_DEPTH:
                playedMoveNode = MoveNode(temp[1], temp[0])
                played_moves.append(playedMoveNode)

                newMove = False
                for child in currentMove.children:
                    if child.equals(playedMoveNode):
                        newMove = child
                if newMove == False:
                    currentMove.addChild(playedMoveNode)
                    newMove = playedMoveNode

                currentMove = newMove

            move(temp[1], temp[0])
            #print(heuristic(matrix, [[1, [16, 12]], [2, [0, 12]]]))
            player_index = (player_index+1) % 3
            if player_index == 0:
                player_index += 1
            screen.fill(pygame.Color("white"))
            animation()
        elif (player_index == 2 and p2 == "ai"):
            print(">> Player 2")
            print("current heuristic is")
            print(heuristic(matrix, [[1, [16, 12]], [2, [0, 12]]]))
            temp = alpha_beta_reg(matrix, 2)
            print("chose the move: ")
            print(temp)

            # add the move to played moves
            if len(played_moves) < OPENING_DEPTH:
                playedMoveNode = MoveNode(temp[1], temp[0])
                played_moves.append(playedMoveNode)

                newMove = False
                for child in currentMove.children:
                    if child.equals(playedMoveNode):
                        newMove = child
                if newMove == False:
                    currentMove.addChild(playedMoveNode)
                    newMove = playedMoveNode

                currentMove = newMove

            move(temp[1], temp[0])
            #print(heuristic(matrix, [[1, [16, 12]], [2, [0, 12]]]))
            player_index = (player_index+1) % 3
            if player_index == 0:
                player_index += 1
            screen.fill(pygame.Color("white"))
            animation()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if (pos[0] >= 300 and pos[0] <= 390 and pos[1] > 430 and pos[1] < 470):
                        last_jumped = [-1, -1]
                        player_index = (player_index+1) % 3
                        if player_index == 0:
                            player_index += 1
                        last_selected_token = []
                        player_valid_moves = []
                        screen.fill(pygame.Color("white"))
                        animation()

                    else:
                        # get a list of all sprites that are under the mouse cursor
                        clicked_sprites = [s for s in pions_rect if s.collidepoint(pos)]

                        if clicked_sprites:
                            clicked_token = get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                            if matrix[clicked_token[0], clicked_token[1]] == player_index:
                                if clicked_token == last_selected_token:
                                    is_selecting = False
                                    last_selected_token = []
                                    player_valid_moves = []
                                    screen.fill(pygame.Color("white"))
                                    animation()
                                else:
                                    player_valid_moves = valid_moves(clicked_token)
                                    last_selected_token = clicked_token
                                    is_selecting = True
                                    screen.fill(pygame.Color("white"))
                                    animation(player_valid_moves,last_selected_token)
                            elif clicked_token in player_valid_moves:



                                # update played moves array
                                if len(played_moves) < OPENING_DEPTH:
                                    playedMoveNode = MoveNode(last_selected_token, clicked_token)
                                    played_moves.append(playedMoveNode)
                                    newMove = False
                                    for child in currentMove.children:
                                        if child.equals(playedMoveNode):
                                            newMove = child
                                    if newMove == False:
                                        currentMove.addChild(playedMoveNode)
                                        newMove = playedMoveNode
                                    
                                    currentMove = newMove

                                move(last_selected_token, clicked_token)
                                #winner() TODO: was this necessary??
                                player_index = (player_index+1) % 3
                                if player_index == 0:
                                    player_index += 1
                                is_selecting = False
                                last_selected_token = []
                                player_valid_moves = []
                                screen.fill(pygame.Color("white"))
                                
                                animation()

            button("back",400, 430, 70, 30, color_dark, color_light, interface2.window2)
            button("End turn",300, 430, 90, 40, color_dark, color_light)
            rect2 = pygame.draw.rect(screen, color_dark, pygame.Rect(394, 424, 82, 42), 6, 20)


        pygame.display.update()
        timer.tick(60)
