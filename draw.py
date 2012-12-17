# -*- coding: utf-8 -*-
from patterns import *
import locale

locale.setlocale(locale.LC_ALL,"")
code = locale.getpreferredencoding()

#pattern = compact
#pattern = box_drawing
pattern = classic
#pattern = multicolored

if enable_curses:
    try:
        import curses
    except:
        enable_curses = False

#colorwalls
if enable_color_players or enable_color_walls:
    enable_colors = True
    pattern = multicolored
    pattern['default'] = ''

def init_draw():
    curscr = None
    if enable_curses:
        curscr = curses.initscr()
        curses.curs_set(0)

    if enable_curses: # and enable_colors:
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
        else:
            enable_colors = False
            enable_color_players = False
            enable_color_walls = False
            pattern = classic

    if enable_curses: #and enable_colors:
        pair_number = 15
        for color in ('red', 'yellow', 'blue', 'green', 'default'):
            if color == 'red':
                fg = curses.COLOR_RED
            elif color == 'yellow':
                fg = curses.COLOR_YELLOW
            elif color == 'blue':
                fg = curses.COLOR_BLUE
            elif color == 'green':
                fg = curses.COLOR_GREEN
            else:
                fg = -1
            pair_number += 1
            curses.init_pair(pair_number, fg, -1)
    return curscr

#field
field = []
for i in range(height_aspect * height + 1):
    field.append([])
    for j in range(width_aspect * width + 1):
        if i % height_aspect:
            if j % width_aspect:
                char = 'blank'
            else:
                char = 'light_vertical'
        else:
            if j % width_aspect:
                char = 'light_horizontal'
            else:
                char = 'light_vertical_and_horizontal'

        field[i].append({'char': char, 'color': 'default', 'modificators': []})

dummy = {'char': 'blank', 'color': 'default', 'modificators': []}

#player picture
player_positions = width_aspect - 1
player_pic = []
for i in range(amount_of_players):
    player_pic.append([])
    color_template = 'default'
    player_template = 'player_%d' % (i * max(AMOUNT_OF_PLAYERS) / amount_of_players)
    modificators = []
    if enable_color_players:
        color_template = COLORS[i * max(AMOUNT_OF_PLAYERS) / amount_of_players]['color']
        modificators = ['bold', 'inverted']
    player_element =  {'char': player_template, 'color': color_template, 'modificators': modificators}
    for j in range(player_positions):
        cutoff = (player_positions - 1) / 2
        if cutoff <= j < (player_positions - cutoff):
            player_pic[i].append(player_element)
        else:
            player_pic[i].append(dummy)

#digits
digit_positions = width_aspect - 1
digit = ['blank'] * digit_positions
numbers={}
for i in range(10):
    char = str(i)
    numbers[char] = char
pattern.update(numbers)

#additional symbols
pattern.update({'left_square_bracket': '['})
pattern.update({'right_square_bracket': ']'})

#wall picture
vertical_wall = ['heavy_vertical'] * (height_aspect * wall_length - 1)
horizontal_wall = ['heavy_horizontal'] * (width_aspect * wall_length - 1)

#corner_polish
def corner_polish(field):
    for (i, field_i) in enumerate(field):
        vertical_min = 0
        vertical_max = len(field) - 1
        vertical_minimax = [vertical_min, vertical_max]
        for (j, field_ij) in enumerate(field_i):
            horizontal_min = 0
            horizontal_max = len(field_i) - 1
            horizontal_minimax = [horizontal_min, horizontal_max]
            char = field_ij['char']
            if char == 'light_vertical_and_horizontal':
                if (i == vertical_min) and (j not in horizontal_minimax):
                    field_ij['char'] = 'light_down_and_horizontal'
                if (i == vertical_max) and (j not in horizontal_minimax):
                    field_ij['char'] = 'light_up_and_horizontal'
                if (j == horizontal_min) and (i not in vertical_minimax):
                    field_ij['char'] = 'light_vertical_and_right'
                if (j == horizontal_max) and (i not in vertical_minimax):
                    field_ij['char'] = 'light_vertical_and_left'
                if (i == vertical_min) and (j == horizontal_min):
                    field_ij['char'] = 'light_down_and_right'
                elif (i == vertical_min) and (j == horizontal_max):
                    field_ij['char'] = 'light_down_and_left'
                elif (i == vertical_max) and (j == horizontal_max):
                    field_ij['char'] = 'light_up_and_left'
                elif (i == vertical_max) and (j == horizontal_min):
                    field_ij['char'] = 'light_up_and_right'

corner_polish(field)

def septum_polish(field):
    pass

def info(player_list):
    info_template = []
    for player in player_list:
        i = player['id']
        player_template = 'player_%d'%i
        color_template = 'default'
        modificators = []
        if enable_color_players:
            color_template = COLORS[i]['color']
            modificators = ['bold', 'inverted']
        info_template.append(dummy)
        info_template.append({'char': player_template, 'color': color_template, 'modificators': modificators})
        info_template.append({'char': 'left_square_bracket', 'color': 'default', 'modificators': []})
        for char in str(player['amount_of_walls']):
            info_template.append({'char': char, 'color': 'default', 'modificators': []})
        info_template.append({'char': 'right_square_bracket', 'color': 'default', 'modificators': []})
    return info_template

def render_for_print(element):
    char = element['char']
    color = element['color']
    if enable_colors and (color != 'default'):
        left_modificator = pattern[color]
        for modificator in element['modificators']:
            if modificator == 'bold':
                left_modificator += u'\033[01m'
            elif modificator == 'inverted':
                left_modificator += u'\033[07m'
        right_modificator = u'\033[0m'
    else:
        left_modificator = ''
        right_modificator = ''

    return left_modificator + pattern[char] + right_modificator

def render_for_curses(element):
    char = element['char']
    color = element['color']
    if color == 'red':
        pair_number = 16
    elif color == 'yellow':
        pair_number = 17
    elif color == 'blue':
        pair_number = 18
    elif color == 'green':
        pair_number = 19
    else:
        pair_number = 20
    attr = curses.color_pair(pair_number)
    for modificator in element['modificators']:
        if modificator == 'bold':
            attr += curses.A_BOLD
        elif modificator == 'inverted':
            attr += curses.A_REVERSE

    string = pattern[char]
    return string, attr

def draw(player_list, wall_list, curscr, additional=[]):
    temp_field = []
    for (i, field_i) in enumerate(field):
        temp_field.append([])
        for field_ij in field_i:
            temp_field[i].append(field_ij.copy())

    for (i, player) in enumerate(player_list):
        (row, col) = player['location']
        for j in range(len(player_pic[i])):
            temp_field[col * height_aspect + 1][row * width_aspect + 1 + j] = player_pic[i][j]

    for wall in wall_list:
        (row, col) = wall['location']
        color_template = COLORS[wall['player_id']]['color']
        if wall['type'] == 'vertical':
            vertical_wall_template = 'heavy_vertical'
            if enable_color_walls:
                #vertical_wall_template = '%s_%s'%(color_template, vertical_wall_template)
                for i in range(len(vertical_wall)):
                    temp_field[(col - 1) * height_aspect + 1 + i][row * width_aspect]['color'] = color_template
            for i in range(len(vertical_wall)):
                temp_field[(col - 1) * height_aspect + 1 + i][row * width_aspect]['char'] = vertical_wall_template

        elif wall['type'] == 'horizontal':
            horizontal_wall_template = 'heavy_horizontal'
            if enable_color_walls:
                #horizontal_wall_template = '%s_%s'%(color_template, horizontal_wall_template)
                for i in range(len(horizontal_wall)):
                    temp_field[col * height_aspect][(row - 1) * width_aspect + 1 + i]['color'] = color_template
            for i in range(len(horizontal_wall)):
                temp_field[col * height_aspect][(row - 1) * width_aspect + 1 + i]['char'] = horizontal_wall_template
        else:
            pass

    for (i, (row, col)) in enumerate(additional):
        digit[digit_positions/2] = str(i + 1)
        for j in range(digit_positions):
            temp_field[col*height_aspect + 1][row * width_aspect + 1 + j]['char'] = digit[j]

    if enable_curses:
        [MAX_Y, MAX_X] = curscr.getmaxyx()
        vertical_offset = (MAX_Y - (height * height_aspect + 1 + 3))/2
        horizontal_offset = (MAX_X - (width * width_aspect + 1))/2
        try:
            curscr.move(vertical_offset, 0)
        except curses.error:
            curses.endwin()
        [cur_y, cur_x] = curscr.getyx()
        for i in range(height_aspect * height + 1):
            string = ''
            try:
                curscr.move(cur_y + 1, horizontal_offset)
            except curses.error:
                curses.endwin()
            for j in range(width_aspect * width + 1):
                [string, attr] = render_for_curses(temp_field[i][j])
                try:
                    curscr.addstr(string.encode(code), attr)
                except curses.error:
                    curses.endwin()
            try:
                [cur_y, cur_x] = curscr.getyx()
                curscr.move(cur_y + 1, horizontal_offset)
                curscr.clrtoeol()
            except curses.error:
                curses.endwin()

        info_template = info(player_list)
        for element in info_template:
            [info_string, attr] = render_for_curses(element)
            try:
                curscr.addstr(info_string.encode(code), attr)
            except curses.error:
                curses.endwin()
        curscr.refresh()
    else:
        vertical_offset = (25 - (height * height_aspect + 1 + 5)) / 2
        horizontal_offset = (80 - (width * width_aspect + 1)) / 2

        print '\033[2J'
        print '\n'*vertical_offset
        for i in range(height_aspect * height + 1):
            string = ' ' * horizontal_offset
            for j in range(width_aspect * width + 1):
                string += render_for_print(temp_field[i][j])

            print string

        info_template = info(player_list)
        info_string = ' ' * horizontal_offset
        for element in info_template:
            info_string += render_for_print(element)

        print info_string
        print '\n' * vertical_offset
