# -*- coding: utf-8 -*-
from turn import *
from draw import *

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

wall_list = []
#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
#wall_list = [{'type': 'horizontal', 'location': (X, Y)}]

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

end = False
win = False
p = 0
draw(player_list, wall_list)
while not win:
    while True:
        #draw field

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
                    #print a_loc
                    (a_col, a_row) = a_loc
                    for neighbors in available_positions[a_loc]:
                        available_positions[neighbors].difference_update(set([a_loc]))
                    
                    b_loc = (a_col + dx, a_row + dy) 
                    if b_loc in available_positions[a_loc]:                            
                        available_positions[b_loc].update(set([loc]))
                        available_positions[loc].update(set([b_loc]))
                    else:
                        #sideway jump
                        (ldx, ldy) = DIRECTIONS[LEFT[direction]]
                        c_loc = (a_col + ldx, a_row + ldy)
                        if c_loc in available_positions[a_loc]:
                            available_positions[c_loc].update(set([loc]))
                            available_positions[loc].update(set([c_loc]))
                        (rdx, rdy) = DIRECTIONS[RIGHT[direction]]
                        d_loc = (a_col + rdx, a_row + rdy)
                        if d_loc in available_positions[a_loc]:
                            available_positions[d_loc].update(set([loc]))
                            available_positions[loc].update(set([d_loc]))        
                    available_positions.update({a_loc: set([])})
        #print available_positions[loc]

        if PLAYERS[p]['owner'] == 'user':
            user_turn(player_list, player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players)
        else:
            print p
            bot_turn(PLAYERS[p], player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players)

        draw(player_list, wall_list)

        if player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location'] in PLAYERS[p]['target_loc']:
            win = True
            end = True
            print "Player %d '%s' win"% (p, PLAYERS[p]['owner'])
 
        if end:
            break
        p += max(AMOUNT_OF_PLAYERS)/amount_of_players
        p %= max(AMOUNT_OF_PLAYERS)
