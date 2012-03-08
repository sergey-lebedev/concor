# -*- coding: utf-8 -*-
from settings import *
from draw import *

def w2p(wall_list):
    print wall_list
    p = {}
    for i in range(1, width):
        for j in range(1, height):
            p.update({(i, j): ['vertical', 'horizontal']})
    for wall in wall_list:
        (x, y) = wall['location']
        p[(x, y)] = []
        if wall['type'] == 'horizontal':
            for direction in ['w', 'e']:
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if location in p:
                    p[location].remove('horizontal')
        elif wall['type'] == 'vertical':
            for direction in ['n', 's']:
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if location in p:
                    p[location].remove('vertical')
        else:
            pass
    print p
    return p

def user_turn(player_list, player, wall_list, available_positions, players):
    (x, y) = player['location']
    loc = (x, y)
    walls_installed = 0
    #print available_positions[loc]
    neighbors = []
    for location in available_positions[loc]:
        neighbors.append(location)

    p = w2p(wall_list)
    draw(player_list, wall_list, neighbors)
    ready = True
    command = raw_input()
    first_symbol = False
    #(X, Y) = wall['location']
    command_list = []
    command_dict = {}
    for i in range(len(neighbors)):
        char = str(i + 1)
        command_list.append(char)
        command_dict[char] = i

    numbers[char] = char        
    if command in command_list:
        players[x][y] = 0
        (x, y) = neighbors[command_dict[command]]
        player['location'] = (x, y)
        players[x][y] = 1  
    else:
        ready = False
        first_symbol = True

    while not ready:
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
            if walls_installed == 0:
                wall = {'type': 'horizontal', 'location': (1, 1)}
                wall_list.append(wall)
                walls_installed +=1
                (X, Y) = wall['location']

        elif (command == 'd'):
            if walls_installed != 0:
                removed_wall = wall_list.pop()
                (X, Y) = removed_wall['location']
                walls_installed -=1
        elif (command == 'b'):
            if wall['type'] in p[(X, Y)]:
                ready = True    
            else:
                ready = False     
        #elif (command == 'q'):
        #    end = True
        #elif (command == 'q!'):
        #    end = True
        #    win = True
        else:
            pass
        draw(player_list, wall_list)
