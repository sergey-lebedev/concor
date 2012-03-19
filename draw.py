# -*- coding: utf-8 -*-
from patterns import *
from settings import *

#pattern = compact
#pattern = box_drawing
#pattern = classic
#pattern = multicolored
pattern = colorwalls

vertical_offset = (25 - (height*height_aspect + 1 + 5))/2
horizontal_offset = (80 - (width*width_aspect + 1))/2

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

#colorwalls
invertor = ''
if pattern == multicolored:
    invertor = u'\033[07m'
if pattern == colorwalls:
    invertor = u'\033[07m'
    for i in range(amount_of_players):    
        color_template = PLAYERS[i*max(AMOUNT_OF_PLAYERS)/amount_of_players]['color']
        for wall_template in ['heavy_vertical', 'heavy_horizontal']:
            new_wall_template = '%s_%s'%(color_template, wall_template)    
            pattern[new_wall_template] = pattern[color_template] + pattern[wall_template]

#player picture
player_positions = width_aspect - 1
player_pic = []
for i in range(amount_of_players):
    color_template = ''
    player_template = 'player_%d'%(i*max(AMOUNT_OF_PLAYERS)/amount_of_players)
    if pattern == multicolored or pattern == colorwalls:
        color_template = PLAYERS[i*max(AMOUNT_OF_PLAYERS)/amount_of_players]['color']
        new_player_template = '%s_%s'%(color_template, player_template)
        pattern[new_player_template] = invertor + pattern[color_template] + pattern[player_template]
        player_template = new_player_template
    player_pic.append([player_template]*player_positions)
    cutoff = (player_positions - 1) / 2
    player_pic[i][:cutoff] = ['blank']*cutoff
    if cutoff != 0:
        player_pic[i][-cutoff:] = ['blank']*cutoff

#digits
digit_positions = width_aspect - 1
digit = ['blank']*digit_positions
numbers={}
for i in range(10):
    char = str(i)
    numbers[char] = char
pattern.update(numbers)

#wall picture
vertical_wall = ['heavy_vertical']*(height_aspect*wall_length - 1)
horizontal_wall = ['heavy_horizontal']*(width_aspect*wall_length - 1)
#player_positions = width_aspect - 1
#player_pic = ['player']*player_positions
#cutoff = (player_positions - 1) / 2
#player_pic[:cutoff] = ['blank']*cutoff

#corner_polish
def corner_polish(field):
    for i in range(len(field)):
        vertical_min = 0
        vertical_max = len(field) - 1
        vertical_minimax = [vertical_min, vertical_max]
        for j in range(len(field[i])):
            horizontal_min = 0
            horizontal_max = len(field[i]) - 1
            horizontal_minimax = [horizontal_min, horizontal_max]
            char = field[i][j]
            if (char == 'light_vertical_and_horizontal'):
                if (i == vertical_min) and (j not in horizontal_minimax):                    
                    field[i][j] = 'light_down_and_horizontal'
                if (i == vertical_max) and (j not in horizontal_minimax):
                    field[i][j] = 'light_up_and_horizontal'
                if (j == horizontal_min) and (i not in vertical_minimax):
                    field[i][j] = 'light_vertical_and_right'
                if (j == horizontal_max) and (i not in vertical_minimax):
                    field[i][j] = 'light_vertical_and_left'
                if (i == vertical_min) and (j == horizontal_min):   
                    field[i][j] = 'light_down_and_right'
                elif (i == vertical_min) and (j == horizontal_max):
                    field[i][j] = 'light_down_and_left'
                elif (i == vertical_max) and (j == horizontal_max):
                    field[i][j] = 'light_up_and_left'                
                elif (i == vertical_max) and (j == horizontal_min):
                    field[i][j] = 'light_up_and_right'                 

corner_polish(field)

def septum_polish(field):
    pass

def info(player_list):  
    string = ''
    for player in player_list:
        i = player['id']    
        player_template = 'player_%d'%i
        if pattern == multicolored or pattern == colorwalls:
            color_template = PLAYERS[i]['color']
            player_template = '%s_%s'%(color_template, player_template)
        string += ' ' + pattern[player_template] + '[' + str(player['amount_of_walls']) + ']'
    return string

def draw(player_list, wall_list, additional=[]):
    temp_field = []
    for lines in field:
        temp_field.append(lines[:])
    
    i = 0
    for player in player_list:
        (row, col) = player['location']   
        for j in range(len(player_pic[i])):
            temp_field[col*height_aspect + 1][row*width_aspect + 1 + j] = player_pic[i][j]
        i +=1    

    for wall in wall_list:
        (row, col) = wall['location']
        color_template = PLAYERS[wall['player_id']]['color']
        if wall['type'] == 'vertical':
            vertical_wall_template = 'heavy_vertical'
            if pattern == colorwalls:               
                vertical_wall_template = '%s_%s'%(color_template, vertical_wall_template)    
            for i in range(len(vertical_wall)):
                temp_field[(col - 1)*height_aspect + 1 + i][row*width_aspect] = vertical_wall_template
        elif wall['type'] == 'horizontal':
            horizontal_wall_template = 'heavy_horizontal'
            if pattern == colorwalls:               
                horizontal_wall_template = '%s_%s'%(color_template, horizontal_wall_template)
            for i in range(len(horizontal_wall)):
                temp_field[col*height_aspect][(row - 1)*width_aspect + 1 + i] = horizontal_wall_template
        else:
            pass  

    for i in range(len(additional)):
        (row, col) = additional[i]  
        digit[digit_positions/2] = str(i + 1)
        for j in range(digit_positions):
            temp_field[col*height_aspect + 1][row*width_aspect + 1 + j] = digit[j]  

    print '\033[2J'
    print '\n'*vertical_offset
    info_string = info(player_list)
    for i in range(height_aspect*height + 1):
        string = ' '*horizontal_offset
        for j in range(width_aspect*width + 1):
                string += pattern[temp_field[i][j]]
        print string
    print ' '*horizontal_offset + info_string
    print '\n'*vertical_offset
