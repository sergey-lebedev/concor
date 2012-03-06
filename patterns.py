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
