# -*- coding: utf-8 -*-
import sys
import getopt
import copy
import time
import __builtin__
from settings import *

__builtin__.enable_curses = True
__builtin__.challenge = False
#__builtin__.width = 5
#__builtin__.height = 5
#__builtin__.AMOUNT_OF_WALLS = 6

from turn import *

PLAYERS = [{'color': 'red', 'location': (width/2, height - 1), 'target_loc': [], 'owner': 'user'},
           {'color': 'green', 'location': (0, height/2), 'target_loc': [], 'owner': 'multiplayer_bot'},
           {'color': 'blue', 'location': (width/2, 0), 'target_loc': [], 'owner': 'greedy_bot'},
           {'color': 'yellow', 'location': (width - 1, height/2), 'target_loc': [], 'owner': 'multiplayer_bot'}]

for i in range(amount_of_players):
    index = i*max(AMOUNT_OF_PLAYERS)/amount_of_players
    (x, y) = PLAYERS[index]['location']
    target_loc = {}
    if (x == 0) or (x == (width - 1)):
        PLAYERS[index]['line'] = (width - 1) - x
        for j in range(height):
            target_loc[(width - 1 - x, j)] = True
    elif (y == 0) or (y == (height - 1)):
        PLAYERS[index]['line'] = (height - 1) - y
        for j in range(width):
            target_loc[(j, height - 1 - y)] = True
    PLAYERS[index]['target_loc'] = target_loc
    PLAYERS[index]['axis'] = (index + 1) % 2
    #print target_loc

# challenge mode
if challenge:
    enable_turn_limit = True
    enable_draw = False
    turn_time_limit = 0
else:
    enable_turn_limit = False
    enable_draw = True
    turn_time_limit = 0.25

def play(player_list):
    turn_limit = 200
    counter = 0
    end = False
    win = False
    p = 0  

    wall_list = []

    # adjacency_list pre-calculation
    adjacency_list = adjacency_list_generator()

    # init draw
    if enable_draw:
        curscr = init_draw() 
        draw(player_list, wall_list, curscr)

    game_state = []
    while not end:
        while True:
            # user turn rollback
            if not challenge:
                current_game_state = (p, copy.deepcopy(player_list), copy.deepcopy(wall_list))
                if not __builtin__.rollback:
                    game_state.append(current_game_state)
                else:
                    game_state_index = max(1, len(game_state) - amount_of_players)
                    game_state = game_state[:game_state_index]
                    current_game_state = game_state[-1]
                    [p, player_list, wall_list] = copy.deepcopy(current_game_state)
                    __builtin__.rollback = False

            # occupied cells  
            loc = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location']
            owner = player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['owner']
            available_positions = available_positions_generator(loc, wall_list, player_list, adjacency_list)       
      
            if owner == 'user':
                end = user_turn(player_list, player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], wall_list, available_positions, curscr)
            else:
                #print p
                tic = time.time()
                bot_turn(PLAYERS[p], player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)], player_list, wall_list, available_positions, adjacency_list)
                toc = time.time()
                turn_time = toc - tic
                #print owner
                #print turn_time
                time.sleep(max(0, turn_time_limit - turn_time))
            counter += 1

            if enable_draw:
                draw(player_list, wall_list, curscr)

            if player_list[p*amount_of_players/max(AMOUNT_OF_PLAYERS)]['location'] in PLAYERS[p]['target_loc']:
                end = True
                win = True
    
            if enable_turn_limit and (counter >= turn_limit):
                end = True
                win = False

            if end:
                if enable_curses and enable_draw:
                    curses.endwin()
                break

            p += max(AMOUNT_OF_PLAYERS)/amount_of_players
            p %= max(AMOUNT_OF_PLAYERS)
    if win:
        return p, counter
    else:
        return -1, counter

if not challenge:
    # players setup
    plist = list()
    for i in range(amount_of_players):
        plist.append(max(AMOUNT_OF_PLAYERS) / amount_of_players * i)
    # print plist
    player_list = list()
    for i in plist:
        player_list.append({'id': i, 
                            'location': PLAYERS[i]['location'], 
                            'amount_of_walls': AMOUNT_OF_WALLS/amount_of_players,
                            'target_loc': PLAYERS[i]['target_loc'],
                            'owner': PLAYERS[i]['owner'],
                            'axis': PLAYERS[i]['axis'],
                            'line': PLAYERS[i]['line']
        })

    # play
    [p, counter] = play(player_list)
    print "Player %d '%s' win"% (p, PLAYERS[p]['owner'])
    print "Number of turns: %d"% (counter)
else:
    botlist = ['mindful_bot', 'greedy_bot']
    counter = [0] * len(botlist)
    numbers = range(len(botlist))
    rounds = 100
    tic = time.time()
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
                                        'target_loc': PLAYERS[k]['target_loc'],
                                        'axis': PLAYERS[k]['axis'],
                                        'line': PLAYERS[k]['line']
                    })
                player_list[0]['owner'] = challenger               
                player_list[1]['owner'] = opponent 

                # play           
                [winner_id, turn_counter] = play(player_list)
                print "Player %d '%s' win"% (winner_id, player_list[winner_id/amount_of_players]['owner'])
                if winner_id == 0:
                    counter[i] += 1
                elif winner_id == 2:
                    counter[j] += 1
                else:
                    counter[i] += 0.5
                    counter[j] += 0.5
    toc = time.time()
    challenge_time = toc - tic
    print challenge_time
    print botlist
    string = ''
    for i in numbers:
        if i!=0:
            string += ':'
        string += str(counter[i] / 2.0 / rounds)
    print string    
