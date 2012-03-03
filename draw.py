# -*- coding: utf-8 -*-
from patterns import *

DIRECTIONS = {'n': (-1, 0),
             'e': (0, 1),
             's': (1, 0),
             'w': (0, -1)
             }
             
AMOUNT_OF_WALLS = 20
AMOUNT_OF_PLAYERS = (2, 4)

amount_of_players = AMOUNT_OF_PLAYERS[0]
pattern = compact
#pattern = box_drawing
pattern = classic
width = 11
height = 9
width_aspect = 4
height_aspect = 2
wall_length = 2

PLAYERS = [{'color': 'red', 'location': (width/2, height - 1), 'target_loc': [], 'owner': 'user'},
           {'color': 'blue', 'location': (width/2, 0), 'target_loc': [], 'owner': 'bot'},
           {'color': 'yellow', 'location': (0, height/2), 'target_loc': [], 'owner': 'bot'},
           {'color': 'green', 'location': (width - 1, height/2), 'target_loc': [], 'owner': 'bot'}]

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

#players setup
players = [None]*width
for i in range(len(players)):
    players[i] = [0]*height

player_list = []
for i in range(amount_of_players):
    (x, y) = PLAYERS[i]['location']
    player_list.append({'id': i, 'location': (x, y)})

for i in range(amount_of_players):
    (x, y) = PLAYERS[i]['location']
    target_loc = []
    if (x == 0) or (x == (width - 1)):
        for j in range(height):
            target_loc.append((width - 1 - x, j))
    elif (y == 0) or (y == (height - 1)):
        for j in range(width):
            target_loc.append((j, height - 1 - y))
    PLAYERS[i]['target_loc'] = target_loc
    print target_loc

for player in player_list:
    players[x][y] =  player['id']      

#player picture
player_positions = width_aspect - 1
player_pic = ['player']*player_positions
cutoff = (player_positions - 1) / 2
player_pic[:cutoff] = ['blank']*cutoff
if cutoff != 0:
    player_pic[-cutoff:] = ['blank']*cutoff

#walls
X = 1
Y = 1
walls = [None]*width
for i in range(len(walls)):
    walls[i] = [0]*height

#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
wall_list = [{'type': 'horizontal', 'location': (X, Y)}]
for wall in wall_list:
    walls[x][y] =  1

#adjacency_list
adjacency_list = {}
for i in range(width):
    for j in range(height):
        link_list = set([])
        for direction in DIRECTIONS:
            (row, col) = DIRECTIONS[direction]
            if ((col + j) >= 0) & ((col + j) < height) &\
               ((row + i) >= 0) & ((row + i) < width): 
                link_list.add((row + i, col + j))
        adjacency_list.update({(i, j): link_list})

vertical_wall = ['heavy_vertical']*(height_aspect*wall_length - 1)
horizontal_wall = ['heavy_horizontal']*(width_aspect*wall_length - 1)
#player_positions = width_aspect - 1
#player_pic = ['player']*player_positions
#cutoff = (player_positions - 1) / 2
#player_pic[:cutoff] = ['blank']*cutoff

end = False
win = False
p = 0
while not win:
    while True:
        #draw field
        temp_field = []
        for lines in field:
            temp_field.append(lines[:])
        
        for player in player_list:
            (row, col) = player['location']   
            for i in range(len(player_pic)):
                temp_field[col*height_aspect + 1][row*width_aspect + 1 + i] = player_pic[i]
        
        for wall in wall_list:
            (row, col) = wall['location']
            if wall['type'] == 'vertical':
                for i in range(len(vertical_wall)):
                    temp_field[(col - 1)*height_aspect + 1 + i][row*width_aspect] = vertical_wall[i]
            elif wall['type'] == 'horizontal':
                for i in range(len(horizontal_wall)):
                    temp_field[col*height_aspect][(row - 1)*width_aspect + 1 + i] = horizontal_wall[i]
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
            (row, col) = wall['location']
            left_top = (row - 1, col - 1)  
            right_top = (row, col - 1) 
            left_bottom = (row - 1, col) 
            right_bottom = (row, col) 

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

        if PLAYERS[p]['owner'] == 'user':
            command = raw_input()
            (x, y) = player_list[p]['location']
            loc = (x, y)
            (X, Y) = wall_list[0]['location']        
            if (command == 'i'):
                if (x, y - 1) in available_positions[loc]:
                    players[x][y] = 0
                    y -= 1
                    y = max(0, y)
                    player_list[p]['location'] = (x, y)
                    players[x][y] = 1  
            elif (command == 'j'):
                if (x - 1, y) in available_positions[loc]:
                    players[x][y] = 0    
                    x -= 1
                    x = max(0, x)
                    player_list[p]['location'] = (x, y)
                    players[x][y] = 1 
            elif (command == 'k'):
                if (x, y + 1) in available_positions[loc]:
                    players[x][y] = 0    
                    y += 1
                    y = min(height-1, y)
                    player_list[p]['location'] = (x, y)
                    players[x][y] = 1 
            elif (command == 'l'):
                if (x + 1, y) in available_positions[loc]:
                    players[x][y] = 0    
                    x += 1
                    x = min(width-1, x)
                    player_list[p]['location'] = (x, y)
                    players[x][y] = 1
            elif (command == 'I'):
                walls[X][Y] = 0    
                Y -= 1
                Y = max(1, Y)
                if (wall_list[0]['type'] == 'vertical') & (Y <= 1):
                    wall_list[0]['type'] = 'horizontal'
                wall_list[0]['location'] = (X, Y)
                walls[X][Y] = 1 
            elif (command == 'J'):
                walls[X][Y] = 0    
                X -= 1
                X = max(1, X)
                if (wall_list[0]['type'] == 'horizontal') & (X <= 1):
                    wall_list[0]['type'] = 'vertical'
                wall_list[0]['location'] = (X, Y)
                walls[X][Y] = 1 
            elif (command == 'K'):
                walls[X][Y] = 0    
                Y += 1
                Y = min(height - wall_length + 1, Y)
                if (wall_list[0]['type'] == 'vertical') & (Y > height - wall_length):
                    wall_list[0]['type'] = 'horizontal'
                wall_list[0]['location'] = (X, Y)
                walls[X][Y] = 1 
            elif (command == 'L'):
                walls[X][Y] = 0    
                X += 1
                X = min(width - wall_length + 1, X)
                if (wall_list[0]['type'] == 'horizontal') & (X > width - wall_length):
                    wall_list[0]['type'] = 'vertical'
                wall_list[0]['location'] = (X, Y)
                walls[X][Y] = 1
            elif (command == 'R'):
                if (wall_list[0]['type'] == 'horizontal'):
                    wall_list[0]['type'] = 'vertical'   
                elif (wall_list[0]['type'] == 'vertical'):
                    wall_list[0]['type'] = 'horizontal'       
            elif (command == 'N'):
                wall_list.insert(0, {'type': 'horizontal', 'location': (1, 1)})                
            elif (command == 'q'):
                end = True
                break
            elif (command == 'q!'):
                end = True
                win = True
                break
            else:
                pass
        if player_list[p]['location'] in PLAYERS[p]['target_loc']:
            win = True
            end = True
            print 'win!'
            break
        p += 1
        p %= amount_of_players
