# -*- coding: utf-8 -*-
from patterns import *
from settings import *

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

#player picture
player_positions = width_aspect - 1
player_pic = ['player']*player_positions
cutoff = (player_positions - 1) / 2
player_pic[:cutoff] = ['blank']*cutoff
if cutoff != 0:
    player_pic[-cutoff:] = ['blank']*cutoff

#wall picture
vertical_wall = ['heavy_vertical']*(height_aspect*wall_length - 1)
horizontal_wall = ['heavy_horizontal']*(width_aspect*wall_length - 1)
#player_positions = width_aspect - 1
#player_pic = ['player']*player_positions
#cutoff = (player_positions - 1) / 2
#player_pic[:cutoff] = ['blank']*cutoff

def draw(player_list, wall_list):
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
