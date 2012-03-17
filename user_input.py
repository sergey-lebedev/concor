# -*- coding: utf-8 -*-
from settings import *
from draw import *

def vector_sort(vectors):
    result = []
    I_quadrant = []
    II_quadrant = []
    III_quadrant = []
    IV_quadrant = []
    for vector in vectors:
        (x, y) = vector
        if (x > 0) and (y >= 0):
            #I_quadrant
            counter = 0
            for items in I_quadrant:
                (a, b) = items
                if (b / a) > (y / x):
                    counter += 1    
            I_quadrant.insert(counter, vector)                
        elif (x <= 0) and (y > 0):
            #II_quadrant
            counter = 0
            for items in II_quadrant:
                (a, b) = items
                if (a / b) < (x / y):
                    counter += 1    
            II_quadrant.insert(counter, vector)  
        elif (x < 0) and (y <= 0):
            #III_quadrant
            counter = 0
            for items in III_quadrant:
                (a, b) = items
                if (b / a) < (y / x):
                    counter += 1    
            III_quadrant.insert(counter, vector)  
        elif (x >= 0) and (y < 0):
            #IV_quadrant
            counter = 0
            for items in IV_quadrant:
                (a, b) = items
                if (a / b) < (x / y):
                    counter += 1    
            IV_quadrant.insert(counter, vector) 
        else:
            pass
    result.extend(III_quadrant)
    result.extend(IV_quadrant)
    result.extend(I_quadrant)
    result.extend(II_quadrant)  
    return result

def w2p(wall_list):
    #print wall_list
    p = {}
    for i in range(1, width):
        for j in range(1, height):
            p.update({(i, j): set(['horizontal', 'vertical'])})
    for wall in wall_list:
        (x, y) = wall['location']
        p[(x, y)] = set([])
        if wall['type'] == 'horizontal':
            for direction in ['w', 'e']:
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if location in p:
                    p[location].difference_update(set(['horizontal']))
        elif wall['type'] == 'vertical':
            for direction in ['n', 's']:
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if location in p:
                    p[location].difference_update(set(['vertical']))
        else:
            pass
    #print p
    return p

def user_turn(player_list, player, wall_list, available_positions, players):
    (x, y) = player['location']
    loc = (x, y)

    #print available_positions[loc]
    neighbors = []
    for location in available_positions[loc]:
        neighbors.append(location)

    p = w2p(wall_list)
    #(X, Y) = wall['location']
    command_list = []
    command_dict = {}
    directions = []
    print neighbors
    for neighbor in neighbors:
        (a, b) = neighbor
        directions.append((a - x, b - y))
    print directions
    directions = vector_sort(directions)
    print directions
    neighbors = []
    for direction in directions:
        (a, b) = direction
        neighbors.append((x + a, y + b))
    print neighbors   
    for i in range(len(neighbors)):
        char = str(i + 1)
        command_list.append(char)
        command_dict[char] = i

    numbers[char] = char      
    ready = False
    second_stage = False
    while not ready:  
        while not ready and not second_stage:
            draw(player_list, wall_list, neighbors)
            command = raw_input()
            if command in command_list:
                players[x][y] = 0
                (x, y) = neighbors[command_dict[command]]
                player['location'] = (x, y)
                players[x][y] = 1
                ready = True
            else:
                ready = False
                second_stage = True

            if player['amount_of_walls'] == 0:
                ready = True

        walls_installed = 0
        while not ready and second_stage:
            #if first_symbol: 
            command = raw_input()
            #    first_symbol = False
            if (command == 'i'):
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]    
                    Y -= 1
                    Y = max(1, Y)
                    if (wall['type'] == 'vertical') & (Y <= 1):
                        wall['type'] = 'horizontal'
                    wall['location'] = (X, Y)
     
            elif (command == 'j'):
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]   
                    X -= 1
                    X = max(1, X)
                    if (wall['type'] == 'horizontal') & (X <= 1):
                        wall['type'] = 'vertical'
                    wall['location'] = (X, Y)

            elif (command == 'k'):
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]  
                    Y += 1
                    Y = min(height - wall_length + 1, Y)
                    if (wall['type'] == 'vertical') & (Y > height - wall_length):
                        wall['type'] = 'horizontal'
                    wall['location'] = (X, Y)

            elif (command == 'l'):
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]  
                    X += 1
                    X = min(width - wall_length + 1, X)
                    if (wall['type'] == 'horizontal') & (X > width - wall_length):
                        wall['type'] = 'vertical'
                    wall['location'] = (X, Y)

            elif (command == 'r'):
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    if (wall['type'] == 'horizontal'):
                        wall['type'] = 'vertical'   
                    elif (wall['type'] == 'vertical'):
                        wall['type'] = 'horizontal'   
        
            elif (command == 'n'):
                if (walls_installed == 0) and (player['amount_of_walls'] != 0):
                    wall = None
                    for i in range(1, width):
                        for j in range(1, height):
                            if p[(i, j)] != set([]):           
                                wall_type = list(p[(i, j)])
                                wall = {'type': wall_type[0], 'location': (i, j)}
                                break
                    if wall != None:
                        wall_list.append(wall)
                        walls_installed +=1
                        (X, Y) = wall['location']

            elif (command == 'd'):
                if walls_installed != 0:
                    removed_wall = wall_list.pop()
                    (X, Y) = removed_wall['location']
                    walls_installed -=1
            elif (command == 'b'):
                if walls_installed != 0:
                    if wall['type'] in p[(X, Y)]:
                        ready = True                  
                else:
                    ready = False
                player['amount_of_walls'] -= walls_installed    
            #elif (command == 'q'):
            #    end = True
            #elif (command == 'q!'):
            #    end = True
            #    win = True
            elif (command == 's'):
                if walls_installed != 0:
                    removed_wall = wall_list.pop()
                    (X, Y) = removed_wall['location']
                    walls_installed -=1
                ready = False
                second_stage = False
            else:
                pass
            draw(player_list, wall_list)
