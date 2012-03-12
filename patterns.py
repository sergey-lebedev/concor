# -*- coding: utf-8 -*-
#patterns
numbers={}
for i in range(10):
    char = str(i)
    numbers[char] = char
compact = {'blank': ' ',
           'light_horizontal': '-',
           'light_vertical': '|',
           'light_vertical_and_horizontal': '+',
           'light_down_and_horizontal': u'+',
           'light_up_and_horizontal': u'+',
           'light_vertical_and_right': u'+',
           'light_vertical_and_left': u'+',
           'light_down_and_right': u'+',
           'light_down_and_left': u'+',
           'light_up_and_left': u'+',           
           'light_up_and_right': u'+',
           'heavy_horizontal': '=',
           'heavy_vertical': u'║',
           'heavy_vertical_and_horizontal': '#',
           'player_0': 'A', 
           'player_1': 'B', 
           'player_2': 'C', 
           'player_3': 'D'
          }
compact.update(numbers)
box_drawing = {'blank': ' ',
               'light_horizontal': u'─',
               'light_vertical': u'│',
               'light_vertical_and_horizontal': u'┼',
               'light_down_and_horizontal': u'┬',
               'light_up_and_horizontal': u'┴',
               'light_vertical_and_right': u'├',
               'light_vertical_and_left': u'┤',
               'light_down_and_right': u'╭',
               'light_down_and_left': u'╮',
               'light_up_and_left': u'╯',           
               'light_up_and_right': u'╰',
               'heavy_horizontal': u'━',
               'heavy_vertical': u'┃',
               'heavy_vertical_and_horizontal': u'╋',
               'vertical_heavy_and_horizontal_light': u'╂',
               'vertical_light_and_horizontal_heavy': u'┿',
               'player_0': u'█', 
               'player_1': u'▓', 
               'player_2': u'▒', 
               'player_3': u'░'    
              }
box_drawing.update(numbers)
classic = {'blank': ' ',
           'light_horizontal': u'─',
           'light_vertical': u'│',
           'light_vertical_and_horizontal': u'┼',
           'light_down_and_horizontal': u'┬',
           'light_up_and_horizontal': u'┴',
           'light_vertical_and_right': u'├',
           'light_vertical_and_left': u'┤',
           'light_down_and_right': u'┌',
           'light_down_and_left': u'┐',
           'light_up_and_left': u'┘',           
           'light_up_and_right': u'└',
           'heavy_horizontal': u'═',
           'heavy_vertical': u'║',
           'heavy_vertical_and_horizontal': u'╬',
           'vertical_heavy_and_horizontal_light': u'╫',
           'vertical_light_and_horizontal_heavy': u'╪',               
           'player_0': u'█', 
           'player_1': u'▓', 
           'player_2': u'▒', 
           'player_3': u'░'    
          }
classic.update(numbers)
multicolored = {'blank': ' ',
                'light_horizontal': u'─',
                'light_vertical': u'│',
                'light_vertical_and_horizontal': u'┼',
                'light_down_and_horizontal': u'┬',
                'light_up_and_horizontal': u'┴',
                'light_vertical_and_right': u'├',
                'light_vertical_and_left': u'┤',
                'light_down_and_right': u'┌',
                'light_down_and_left': u'┐',
                'light_up_and_left': u'┘',           
                'light_up_and_right': u'└',
                'heavy_horizontal': u'═',
                'heavy_vertical': u'║',
                'heavy_vertical_and_horizontal': u'╬',
                'vertical_heavy_and_horizontal_light': u'╫',
                'vertical_light_and_horizontal_heavy': u'╪',               
                'player_0': u'\033[101m' + ' ' + u'\033[0m', 
                'player_1': u'\033[102m' + ' ' + u'\033[0m', 
                'player_2': u'\033[104m' + ' ' + u'\033[0m', 
                'player_3': u'\033[103m' + ' ' + u'\033[0m'    
               }
multicolored.update(numbers)

