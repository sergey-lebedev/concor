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
    player_list.append({'id': i, 'location': (x, y), 'amount_of_walls': AMOUNT_OF_WALLS/amount_of_players})

for player in player_list:
    (x, y) = player['location']
    players[x][y] =  player['id']      

wall_list = []
#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
#wall_list = [{'type': 'horizontal', 'location': (X, Y)}]

end = False
win = False
p = 0
draw(player_list, wall_list)
while not win:
    while True:
        #occupied cells
        loc = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location']
        available_positions = available_positions_generator(loc, wall_list, player_list)

        if PLAYERS[p]['owner'] == 'user':
            user_turn(player_list, player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players)
        else:
            #print p
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
