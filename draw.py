# -*- coding: utf-8 -*-
from patterns import *
from turn import *

#pattern = compact
pattern = box_drawing
#pattern = classic

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

plist = []
for i in range(amount_of_players):
    plist.append(max(AMOUNT_OF_PLAYERS)/amount_of_players*i)
print plist
player_list = []
for i in plist:
    (x, y) = PLAYERS[i]['location']
    player_list.append({'id': i, 'location': (x, y)})

for player in player_list:
    (x, y) = player['location']
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

wall_list = []
#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
#wall_list = [{'type': 'horizontal', 'location': (X, Y)}]
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

        #occupied cells
        loc = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location']
        (col, row) = loc        
        #print available_positions[loc]
        for direction in DIRECTIONS:
            (dx, dy) = DIRECTIONS[direction]                    
            for player in player_list:
                a_loc = player['location']
                if a_loc == (col + dx, row + dy):
                    print a_loc
                    (a_col, a_row) = a_loc
                    for neighbors in available_positions[a_loc]:
                        available_positions[neighbors].difference_update(set([a_loc]))
                    
                    b_loc = (a_col + dx, a_row + dy) 
                    if b_loc in available_positions[a_loc]:                            
                        available_positions[b_loc].update(set([loc]))
                        available_positions[loc].update(set([b_loc]))
                    available_positions.update({a_loc: set([])})
        #print available_positions[loc]

        if PLAYERS[p]['owner'] == 'user':
            user_turn(player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players, walls)
        else:
            print p
            bot_turn(PLAYERS[p], player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players)

        if player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location'] in PLAYERS[p]['target_loc']:
            win = True
            end = True
            print "Player %d '%s' win"% (p, PLAYERS[p]['owner']) 
        if end:
            break
        p += max(AMOUNT_OF_PLAYERS)/amount_of_players
        p %= max(AMOUNT_OF_PLAYERS)
