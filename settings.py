# -*- coding: utf-8 -*-
import __builtin__
__builtin__.DIRECTIONS = {'n': (0, -1),
             'e': (1, 0),
             's': (0, 1),
             'w': (-1, 0)}
__builtin__.LEFT = {'n': 'w',
        'w': 's',
        's': 'e',
        'e': 'n'}
__builtin__.RIGHT = {'n': 'e',
         'e': 's',
         's': 'w',
         'w': 'n'}

__builtin__.AMOUNT_OF_WALLS= 20
__builtin__.AMOUNT_OF_PLAYERS = (2, 4)
__builtin__.COLORS = [{'color': 'red'},
           {'color': 'green'},
           {'color': 'blue'},
           {'color': 'yellow'}
]

__builtin__.amount_of_players = AMOUNT_OF_PLAYERS[0]
__builtin__.width = 9
__builtin__.height = 9
__builtin__.width_aspect = 4
__builtin__.height_aspect = 2
__builtin__.wall_length = 2

__builtin__.enable_curses = True
__builtin__.enable_colors = True
__builtin__.enable_color_players = True
__builtin__.enable_color_walls = True
__builtin__.enable_draw = True
__builtin__.turn_time_limit = 0
