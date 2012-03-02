# -*- coding: utf-8 -*-
from patterns import *

DIRECTION = {'n': (-1, 0),
            'e': (0, 1),
            's': (1, 0),
            'w': (0, -1)}

pattern = compact
#pattern = box_drawing
pattern = classic
width = 11
height = 11
width_aspect = 4
height_aspect = 2
wall_length = 2

#field
field = []
for i in range(height_aspect*height + 1):
    field.append([])
    for j in range(width_aspect*width + 1):
        if (i % height_aspect):
            if (j % width_aspect):
                char = 'blank' 
            else:
                char = 'light_vertical'                    
        else:
            if (j % width_aspect):
                char = 'light_horizontal'
            else:
                char = 'light_vertical_and_horizontal'

        field[i].append(char)

#players
x = 0
y = 0
players = [None]*height
for i in range(len(players)):
    players[i] = [0]*width

player_list = [{'id': 1, 'x': x, 'y': y}]
for player in player_list:
    players[y][x] =  player['id']      

player_positions = width_aspect - 1
player_pic = ['player']*player_positions
cutoff = (player_positions - 1) / 2
player_pic[:cutoff] = ['blank']*cutoff
if cutoff != 0:
    player_pic[-cutoff:] = ['blank']*cutoff

#walls
X = 1
Y = 1
walls = [None]*height
for i in range(len(walls)):
    walls[i] = [0]*width

#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
wall_list = [{'type': 'horizontal', 'x': X, 'y': Y}]
for wall in wall_list:
    walls[y][x] =  1

#adjacency_list
adjacency_list = {}
for i in range(height):
    for j in range(width):
        link_list = set([])
        for direction in DIRECTION:
            (row, col) = DIRECTION[direction]
            if ((row + i) >= 0) & ((row + i) < height) &\
               ((col + j) >= 0) & ((col + j) < width): 
                link_list.add((row + i)*width + (col + j))
        adjacency_list.update({i*width + j: link_list})  

vertical_wall = ['heavy_vertical']*(height_aspect*wall_length - 1)
horizontal_wall = ['heavy_horizontal']*(width_aspect*wall_length - 1)
#player_positions = width_aspect - 1
#player_pic = ['player']*player_positions
#cutoff = (player_positions - 1) / 2
#player_pic[:cutoff] = ['blank']*cutoff

while True:
    #draw field
    temp_field = []
    for lines in field:
        temp_field.append(lines[:])
    
    for player in player_list:   
        for i in range(len(player_pic)):
            temp_field[player['y']*height_aspect + 1][player['x']*width_aspect + 1 + i] = player_pic[i]
    
    for wall in wall_list:
        if wall['type'] == 'vertical':
            for i in range(len(vertical_wall)):
                temp_field[(wall['y'] - 1)*height_aspect + 1 + i][wall['x']*width_aspect] = vertical_wall[i]
        elif wall['type'] == 'horizontal':
            for i in range(len(horizontal_wall)):
                temp_field[wall['y']*height_aspect][(wall['x'] - 1)*width_aspect + 1 + i] = horizontal_wall[i]
        else:
            pass  

    for i in range(height_aspect*height + 1):
        string = ''
        for j in range(width_aspect*width + 1):
                string += pattern[temp_field[i][j]]
        print string

    #calculate available positions
    available_positions = {}
    for positions in adjacency_list:
        #print positions
        available_positions.update({positions: adjacency_list[positions].copy()})
    #available_positions = adjacency_list.copy()
    #print available_positions
    for wall in wall_list:
        left_top = (wall['y'] - 1)*width + wall['x'] - 1 
        right_top = (wall['y'] - 1)*width + wall['x']
        left_bottom = wall['y']*width + wall['x'] - 1
        right_bottom = wall['y']*width + wall['x']

        #print left_top, right_top,left_bottom, right_bottom
        if (wall['type'] == 'horizontal'):
            available_positions[left_top].difference_update(set([left_bottom]))
            available_positions[left_bottom].difference_update(set([left_top])) 
            available_positions[right_top].difference_update(set([right_bottom]))    
            available_positions[right_bottom].difference_update(set([right_top]))         
        elif (wall['type'] == 'vertical'):        
            available_positions[left_top].difference_update(set([right_top]))
            available_positions[left_bottom].difference_update(set([right_bottom])) 
            available_positions[right_top].difference_update(set([left_top]))    
            available_positions[right_bottom].difference_update(set([left_bottom]))

    command = raw_input()
    if (command == 'i'):
        if ((y-1)*width + x) in available_positions[y*width + x]:
            players[y][x] = 0
            y -= 1
            y = max(0, y)
            player_list[0]['y'] = y
            players[y][x] = 1  
    elif (command == 'j'):
        if (y*width + x - 1) in available_positions[y*width + x]:
            players[y][x] = 0    
            x -= 1
            x = max(0, x)
            player_list[0]['x'] = x
            players[y][x] = 1 
    elif (command == 'k'):
        if ((y+1)*width + x) in available_positions[y*width + x]:
            players[y][x] = 0    
            y += 1
            y = min(height-1, y)
            player_list[0]['y'] = y
            players[y][x] = 1 
    elif (command == 'l'):
        if (y*width + x + 1) in available_positions[y*width + x]:
            players[y][x] = 0    
            x += 1
            x = min(width-1, x)
            player_list[0]['x'] = x
            players[y][x] = 1
    elif (command == 'I'):
        walls[Y][X] = 0    
        Y -= 1
        Y = max(1, Y)
        if (wall_list[0]['type'] == 'vertical') & (Y <= 1):
            wall_list[0]['type'] = 'horizontal'
        wall_list[0]['y'] = Y
        walls[Y][X] = 1 
    elif (command == 'J'):
        walls[Y][X] = 0    
        X -= 1
        X = max(1, X)
        if (wall_list[0]['type'] == 'horizontal') & (X <= 1):
            wall_list[0]['type'] = 'vertical'
        wall_list[0]['x'] = X
        walls[Y][X] = 1 
    elif (command == 'K'):
        walls[Y][X] = 0    
        Y += 1
        Y = min(height - wall_length + 1, Y)
        if (wall_list[0]['type'] == 'vertical') & (Y > height - wall_length):
            wall_list[0]['type'] = 'horizontal'
        wall_list[0]['y'] = Y
        walls[Y][X] = 1 
    elif (command == 'L'):
        walls[Y][X] = 0    
        X += 1
        X = min(width - wall_length + 1, X)
        if (wall_list[0]['type'] == 'horizontal') & (X > width - wall_length):
            wall_list[0]['type'] = 'vertical'
        wall_list[0]['x'] = X
        walls[Y][X] = 1
    elif (command == 'R'):
        if (wall_list[0]['type'] == 'horizontal'):
            wall_list[0]['type'] = 'vertical'   
        elif (wall_list[0]['type'] == 'vertical'):
            wall_list[0]['type'] = 'horizontal'       
    elif (command == 'N'):
        wall_list.insert(0, {'type': 'horizontal', 'x': 1, 'y': 1})
            
    elif (command == 'q'):
        break
    else:
        pass
