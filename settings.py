# -*- coding: utf-8 -*-
DIRECTIONS = {'n': (-1, 0),
             'e': (0, 1),
             's': (1, 0),
             'w': (0, -1)}
LEFT = {'n': 'w',
        'w': 's',
        's': 'e',
        'e': 'n'}
RIGHT = {'n': 'e',
         'e': 's',
         's': 'w',
         'w': 'n'}
AMOUNT_OF_WALLS = 20
AMOUNT_OF_PLAYERS = (2, 4)

amount_of_players = AMOUNT_OF_PLAYERS[0]
width = 11
height = 11
width_aspect = 4
height_aspect = 2
wall_length = 2

PLAYERS = [{'color': 'red', 'location': (width/2, height - 1), 'target_loc': [], 'owner': 'straight_bot'},
           {'color': 'yellow', 'location': (0, height/2), 'target_loc': [], 'owner': 'straight_bot'},
           {'color': 'blue', 'location': (width/2, 0), 'target_loc': [], 'owner': 'user'},
           {'color': 'green', 'location': (width - 1, height/2), 'target_loc': [], 'owner': 'straight_bot'}]

for i in range(amount_of_players):
    (x, y) = PLAYERS[i*max(AMOUNT_OF_PLAYERS)/amount_of_players]['location']
    target_loc = []
    if (x == 0) or (x == (width - 1)):
        for j in range(height):
            target_loc.append((width - 1 - x, j))
    elif (y == 0) or (y == (height - 1)):
        for j in range(width):
            target_loc.append((j, height - 1 - y))
    PLAYERS[i*max(AMOUNT_OF_PLAYERS)/amount_of_players]['target_loc'] = target_loc
    #print target_loc
