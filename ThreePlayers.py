NULL = 0
import copy
from re import I
from numpy import Inf
import pygame
import sys
import interface2
import math

SEARCH_DEPTH = 2
pygame.init()

color_light = (202, 203, 213)
color_dark = (2, 6, 145)
import numpy
def TreePlayers(p1, p2, p3):
    # remplir la matrice avec des 1
    matrix = numpy.ones((17, 25))
    # remplir la matrice avec des -1
    matrix *= -1

    # les positions des pions dans la matrice pour chaque joueur
    first_player = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    first_aim = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13],[13, 15]]
    second_player = [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]]
    second_aim = [[4, 0], [4, 2], [5, 1], [4, 4], [5, 3], [6, 2], [4, 6], [5, 5], [6, 4], [7, 3]]
    third_player = [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]]
    third_aim = [[4, 24], [5, 23], [4, 22], [6, 22], [5, 21], [4, 20], [7, 21], [6, 20], [5, 19], [4, 18]]
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
                # print(i,j)
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
        if index == 3:
            for i in range(len(third_player)):
                matrix[third_player[i][0]][third_player[i][1]] = index

    # l'ajout des pions de chaque joueur
    class remplissage:
        def __init__(self):
            self_x = 0
            self_y = 0

        def pion(self):
            colors = [(240, 230, 230), "red", "yellow", "orange"]
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
        # print('before:', x, y)
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
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    # les coordonnees parraport a la grille
    def get_token_coor(x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor

    # l'annimation des deplasssements possibles
    def animation(moves=[],clicked_token = None):
        colors = [(240, 230, 230), "red", "yellow", "orange"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_cercle = pygame.image.load('./imgs/cercle.png')
                    test_cercle = pygame.transform.scale(test_cercle, (CELL_SIZE ,CELL_SIZE))
                    screen.blit(test_cercle,(j * CELL_SIZE,  i * CELL_SIZE) )
    #grille
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
        second = True
        first = True
        third = True
        for i in range(len(first_aim)):
            if matrix[first_aim[i][0]][first_aim[i][1]] != 1:
                first = False
                break
        for i in range(len(second_aim)):
            if matrix[second_aim[i][0]][second_aim[i][1]] != 2:
                second = False
                break
        for i in range(len(third_aim)):
            if matrix[third_aim[i][0]][third_aim[i][1]] != 3:
                third = False
                break

        if first == True:
            WriteText('Player 1 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'red')
            return True
        elif (second == True):
            WriteText('Player 2 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'yellow')
            return True
        elif (third == True):
            WriteText('Player 3 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'orange')
            return True
        else:
            return False

    add_player(1)
    add_player(2)
    add_player(3)

    # l'affichage de la fenetre du jeu
    nb_col = 25
    nb_ligne = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(size=(nb_col * CELL_SIZE, nb_ligne * CELL_SIZE))
    timer = pygame.time.Clock()
    game_on = True
    pions_rect = []

    players = remplissage()


    screen.fill(pygame.Color("white"))
    players.pion()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []

    def distance(target, destination):
        # literally just pythagorean theorem :)
        return math.sqrt((target[0] - destination[0])**2 + (target[1] - destination[1])**2)
        # return ((target[0] - destination[0]) + (target[1] - destination[1]))

    def heuristic(state, pid):
        heuristic_value = 0
        player_1_pawns = []
        player_2_pawns = []
        player_3_pawns = []

        players = [[1],[2],[3]]
        # go through the whole board and get each player's pawns
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 1:
                    bigTuple = (i,j)
                    player_1_pawns.append(bigTuple)
                elif state[i][j] == 2:
                    bigTuple = (i,j)
                    player_2_pawns.append(bigTuple)
                elif state[i][j] == 3:
                    bigTuple = (i,j)
                    player_3_pawns.append(bigTuple)
        #now the pawns arrays have all known pawns

        #update for player1
        
        for goal in first_aim:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_1_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            heuristic_value += lowestDistance
            #print(str(goal),str(closestPawn))
            player_1_pawns.remove(closestPawn)

        #print("heuristic value is " + str(heuristic_value))

        player2Val = 0
        #update for player2
        for goal in second_aim:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_2_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player2Val += lowestDistance
            player_2_pawns.remove(closestPawn)

        
        player2Val = (player2Val/1.6)
        #print("player2Val value is " + str(player2Val))

        player3Val = 0
        #update for player2
        for goal in third_aim:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_3_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player3Val += lowestDistance
            player_3_pawns.remove(closestPawn)
        
        player3Val = (player3Val/1.6)
        #print("player3Val value is " + str(player3Val))
        # re-stock pawns arrays

        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 1:
                    bigTuple = (i,j)
                    player_1_pawns.append(bigTuple)
                elif state[i][j] == 2:
                    bigTuple = (i,j)
                    player_2_pawns.append(bigTuple)
                elif state[i][j] == 3:
                    bigTuple = (i,j)
                    player_3_pawns.append(bigTuple)

        player1_inverse = [[16, 12], [15, 13], [15, 11], [14, 14], [14, 12], [14, 10], [13, 15], [13, 13], [13, 11],[13, 9]]
        player2_inverse = [[4, 0], [5, 1], [4, 2], [6, 2], [5, 3], [4, 4], [7, 3], [6, 4], [5, 5], [4, 6]]
        player3_inverse = [[4, 24], [4, 22], [5, 23], [4, 20], [5, 21], [6, 22], [4, 18], [5, 19], [6, 20], [7, 21]]

        
        player1Val_a = 0
        for goal in player1_inverse:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_1_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player1Val_a += lowestDistance
            player_1_pawns.remove(closestPawn)

        if(player1Val_a > heuristic_value):
           heuristic_value = player1Val_a

        player2Val_a = 0
        for goal in player2_inverse:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_2_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player2Val_a += lowestDistance
            player_2_pawns.remove(closestPawn)

        player2Val_a = player2Val_a/1.6

        if(abs(player2Val_a) > abs(player2Val)):
            player2Val = player2Val_a

        player3Val_a = 0
        for goal in player3_inverse:
            closestPawn = (0,0)
            lowestDistance = 100000 #lazy way to represent positive infinity
            for pawn in player_3_pawns:
                dist = distance(pawn, goal) 
                if dist < lowestDistance:
                    closestPawn = pawn
                    lowestDistance = dist
            player3Val_a += lowestDistance
            player_3_pawns.remove(closestPawn)

        player3Val_a = player3Val_a/1.6

        
        if(abs(player3Val_a) > abs(player3Val)):
            player3Val = player3Val_a
        

        if(pid == 1):
            return (2*heuristic_value) - player2Val - player3Val
        elif(pid == 2):
            return (2*player2Val) - heuristic_value - player3Val
        elif(pid == 3):
            return (2*player3Val) - heuristic_value - player2Val


    def alpha_beta_reg(state1, toMoveId):
        state = copy.deepcopy(state1)
        if (toMoveId == 1):
            value = max_value(state, 1, -Inf, Inf, 1)
        elif (toMoveId == 2):
            value = max_value(state, 2, -Inf, Inf, 1)
        elif (toMoveId == 3):
            value = max_value(state, 3, -Inf, Inf, 1)
        return [value[1], value[2]]
    
    def max_value(state, player, alpha, beta, depth):
        p = []
        temp = player
        temp = (temp) % 4
        if(temp == 0):
            temp = 1
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == temp:
                    p.append([i, j])
        if (depth >= SEARCH_DEPTH):
            return [heuristic(state, temp), NULL, NULL]
        v = -Inf
        move = [-1, -1]
        initial = [-1, -1]
        for i in p:
            player_valid_moves = valid_moves(i)
            for a in player_valid_moves:
                v2 = max_value(move2(state, i, a), temp + 1, alpha, beta, depth+1)
                if (v2[0] > v):
                    v = v2[0]
                    move = a
                    initial = i
                    if (v > alpha): alpha = v
                if (v >= beta):
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
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

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
        if player_index == 1: col = 'red'
        if player_index == 2: col = 'yellow'
        if player_index == 3: col = 'orange'
        # player turn
        if (winner() == False):
            WriteText('Player ' + str(player_index) + '\'s Turn', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100,
                      50, col)
        else:
            screen.fill(pygame.Color("white"))
            animation()
            pygame.time.wait(9999999)
        if (player_index == 1 and p1 == "ai"):
            #print(heuristic(matrix, 1))
            temp = alpha_beta_reg(matrix, 1)
            #print(temp)
            move(temp[1], temp[0])
            #print(heuristic(matrix, 1))
            player_index = (player_index+1) % 4
            if player_index == 0:
                player_index += 1
            screen.fill(pygame.Color("white"))
            animation()
        elif (player_index == 2 and p2 == "ai"):
            #print(heuristic(matrix, 2))
            temp = alpha_beta_reg(matrix, 2)
            #print(temp)
            move(temp[1], temp[0])
            #print(heuristic(matrix, 2))
            player_index = (player_index+1) % 4
            if player_index == 0:
                player_index += 1
            screen.fill(pygame.Color("white"))
            animation()
        elif (player_index == 3 and p3 == "ai"):
            #print(heuristic(matrix, 3))
            temp = alpha_beta_reg(matrix, 3)
            #print(temp)
            move(temp[1], temp[0])
            #print(heuristic(matrix, 3))
            player_index = (player_index+1) % 4
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
                            move(last_selected_token, clicked_token)
                            if winner() == True:
                                animation()
                                pygame.time.wait(9999999)
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            screen.fill(pygame.Color("white"))
                            player_index = (player_index+1) % 4
                            if player_index == 0:
                                player_index += 1
                            animation()
                button("back", 400, 430, 70, 30, color_dark, color_light, interface2.window2)
                rect2 = pygame.draw.rect(screen, color_dark, pygame.Rect(394, 424, 82, 42), 6, 20)

        pygame.display.update()
        timer.tick(60)
