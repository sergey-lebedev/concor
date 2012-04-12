# -*- coding: utf-8 -*-
import time
from turn import *
from draw import *

#players setup
players = [None]*width
for i in range(len(players)):
    players[i] = [0]*height

plist = []
for i in range(amount_of_players):
    plist.append(max(AMOUNT_OF_PLAYERS)/amount_of_players*i)
#print plist
player_list = []
for i in plist:
    player_list.append({'id': i, 
                        'location': PLAYERS[i]['location'], 
                        'amount_of_walls': AMOUNT_OF_WALLS/amount_of_players,
                        'target_loc': PLAYERS[i]['target_loc']
    })

for player in player_list:
    (x, y) = player['location']
    players[x][y] =  player['id']      

wall_list = []
#wall_list = [{'type': 'vertical', 'x': X, 'y': Y}]
#wall_list = [{'type': 'horizontal', 'location': (X, Y)}]

turn_time_limit = 0.25

end = False
win = False
p = 0

curscr = init_draw() 
draw(player_list, wall_list, curscr)

while not end:
    while True:
        #occupied cells
        loc = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location']
        available_positions = available_positions_generator(loc, wall_list, player_list)

        if PLAYERS[p]['owner'] == 'user':
            end = user_turn(player_list, player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players, curscr)
        else:
            #print p
            tic = time.time()
            bot_turn(PLAYERS[p], player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], player_list, wall_list, available_positions, players)
            toc = time.time()
            turn_time = toc - tic
            time.sleep(max(0, turn_time_limit - turn_time))
        draw(player_list, wall_list, curscr)

        if player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location'] in PLAYERS[p]['target_loc']:
            end = True
            win = True
 
        if end:
            if enable_curses:
                curses.endwin()
            break

        p += max(AMOUNT_OF_PLAYERS)/amount_of_players
        p %= max(AMOUNT_OF_PLAYERS)

if win:
    print "Player %d '%s' win"% (p, PLAYERS[p]['owner'])
