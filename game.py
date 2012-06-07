# -*- coding: utf-8 -*-
import time
from turn import *
from draw import *

# challenge mode
challenge = not False
if challenge:
    enable_draw = False
    turn_time_limit = 0
else:
    enable_draw = True
    turn_time_limit = 0.25

def play(player_list):
    end = False
    win = False
    p = 0
    
    # players setup
    players = [None] * width
    for i in range(len(players)):
        players[i] = [0] * height

    for player in player_list:
        (x, y) = player['location']
        players[x][y] =  player['id']      

    wall_list = []

    # init draw
    if enable_draw:
        curscr = init_draw() 
        draw(player_list, wall_list, curscr)

    while not end:
        while True:
            # occupied cells
            loc = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location']
            available_positions = available_positions_generator(loc, wall_list, player_list)

            owner = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['owner']
            if owner == 'user':
                end = user_turn(player_list, player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, players, curscr)
            else:
                #print p
                tic = time.time()
                bot_turn(PLAYERS[p], player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], player_list, wall_list, available_positions, players)
                toc = time.time()
                turn_time = toc - tic
                time.sleep(max(0, turn_time_limit - turn_time))
            if enable_draw:
                draw(player_list, wall_list, curscr)

            if player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location'] in PLAYERS[p]['target_loc']:
                end = True
                win = True
     
            if end:
                if enable_curses and enable_draw:
                    curses.endwin()
                break

            p += max(AMOUNT_OF_PLAYERS)/amount_of_players
            p %= max(AMOUNT_OF_PLAYERS)

    return p

if not challenge:
    # players setup
    plist = []
    for i in range(amount_of_players):
        plist.append(max(AMOUNT_OF_PLAYERS) / amount_of_players * i)
    # print plist
    player_list = []
    for i in plist:
        player_list.append({'id': i, 
                            'location': PLAYERS[i]['location'], 
                            'amount_of_walls': AMOUNT_OF_WALLS/amount_of_players,
                            'target_loc': PLAYERS[i]['target_loc'],
                            'owner': PLAYERS[i]['owner']
        })

    # play
    p = play(player_list)
    print "Player %d '%s' win"% (p, PLAYERS[p]['owner'])
else:
    botlist = ['simple_bot', 'simple_bot']
    counter = [0] * len(botlist)
    numbers = range(len(botlist))
    rounds = 1000
    for r in range(rounds):
        print '%d / %d' % (r + 1, rounds)
        for i in numbers:
            challenger = botlist[i]
            opponents = set(numbers) - set([i])       
            for j in opponents:
                opponent = botlist[j]
                # print ('%s versus %s') % (challenger, opponent)
                amount_of_players = 2
                player_list = []
                for k in (0, 2):
                    player_list.append({'id': k, 
                                        'location': PLAYERS[k]['location'], 
                                        'amount_of_walls': AMOUNT_OF_WALLS/amount_of_players,
                                        'target_loc': PLAYERS[k]['target_loc']
                    })
                player_list[0].update({'owner': challenger})               
                player_list[1].update({'owner': opponent}) 

                # play           
                winner_id = play(player_list)
                if winner_id == 0:
                    counter[i] += 1
                if winner_id == 2:
                    counter[j] += 1

    print botlist
    string = ''
    for i in numbers:
        string += counter[i]
        string += ':'
    print string    
