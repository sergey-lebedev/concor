# -*- coding: utf-8 -*-
import __builtin__
from draw import *
from bots.algorithms import *
if enable_curses:
    import curses

# keyboard arrows
KEY_UP = 65
KEY_DOWN = 66
KEY_LEFT = 68
KEY_RIGHT = 67

def vector_sort(vectors):
    result = []
    I_quadrant = []
    II_quadrant = []
    III_quadrant = []
    IV_quadrant = []
    for vector in vectors:
        (x, y) = vector
        if x >= 0 and y > 0:
            #I_quadrant
            counter = 0
            for items in I_quadrant:
                (a, b) = items
                if (a / b) > (x / y):
                    counter += 1
            I_quadrant.insert(counter, vector)
        elif x < 0 and y >= 0:
            #II_quadrant
            counter = 0
            for items in II_quadrant:
                (a, b) = items
                if (b / a) < (y / x):
                    counter += 1
            II_quadrant.insert(counter, vector)
        elif x <= 0 and y < 0:
            #III_quadrant
            counter = 0
            for items in III_quadrant:
                (a, b) = items
                if (a / b) > (x / y):
                    counter += 1
            III_quadrant.insert(counter, vector)
        elif x > 0 and y <= 0:
            #IV_quadrant
            counter = 0
            for items in IV_quadrant:
                (a, b) = items
                if (b / a) < (y / x):
                    counter += 1
            IV_quadrant.insert(counter, vector)
        else:
            pass
    result.extend(II_quadrant)
    result.extend(III_quadrant)
    result.extend(IV_quadrant)
    result.extend(I_quadrant)
    return result

def user_turn(player_list, player, wall_list, available_positions, curscr):
    (x, y) = player['location']
    loc = (x, y)
    #print available_positions[loc]
    neighbors = []
    for location in available_positions[loc]:
        neighbors.append(location)

    p = w2p(wall_list)
    #(X, Y) = wall['location']
    command_list = []
    command_dict = {}
    directions = []
    for neighbor in neighbors:
        (a, b) = neighbor
        directions.append((a - x, b - y))
    directions = vector_sort(directions)
    neighbors = []
    for direction in directions:
        (a, b) = direction
        neighbors.append((x + a, y + b))
    for i in range(len(neighbors)):
        char = str(i + 1)
        command_list.append(char)
        command_dict[char] = i

    quit = False
    ready = False
    new_wall = False
    second_stage = False
    while not ready:
        while not ready and not second_stage:
            draw(player_list, wall_list, curscr, neighbors)
            if enable_curses:
                curses.noecho()
                k = curscr.getch()
                command = curses.keyname(k)
            else:
                command = raw_input()

            if command in command_list:
                (x, y) = neighbors[command_dict[command]]
                player['location'] = (x, y)
                ready = True
            elif command == 'q':
                quit = True
                ready = True
            elif command == 'n':
                new_wall = True
                ready = False
                second_stage = True
            elif command == 'u':
                __builtin__.rollback = True
                ready = True
            else:
                ready = False
                second_stage = False

            if player['amount_of_walls'] == 0:
                second_stage = False

        walls_installed = 0
        while not ready and second_stage:
            if enable_curses:
                curses.noecho()
                k = curscr.getch()
                command = curses.keyname(k)
            else:
                k = 0
                command = raw_input()

            if command == 'n':
                new_wall = False
                if walls_installed == 0 and player['amount_of_walls'] != 0:
                    wall = None
                    for i in range(1, width):
                        for j in range(height - 1, 0, -1):
                            for wall_type in p[(i, j)]:
                                wall = {'type': wall_type, 'location': (i, j), 'player_id': player['id']}
                                break
                    if wall != None:
                        wall_list.append(wall)
                        walls_installed +=1
                        (X, Y) = wall['location']

            elif command == 'i' or k == KEY_UP:
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    Y -= 1
                    Y = max(1, Y)
                    if wall['type'] == 'vertical' and Y <= 1:
                        wall['type'] = 'horizontal'
                    wall['location'] = (X, Y)

            elif command == 'j' or k == KEY_LEFT:
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    X -= 1
                    X = max(1, X)
                    if wall['type'] == 'horizontal' and X <= 1:
                        wall['type'] = 'vertical'
                    wall['location'] = (X, Y)

            elif command == 'k' or k == KEY_DOWN:
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    Y += 1
                    Y = min(height - wall_length + 1, Y)
                    if wall['type'] == 'vertical' and Y > (height - wall_length):
                        wall['type'] = 'horizontal'
                    wall['location'] = (X, Y)

            elif command == 'l' or k == KEY_RIGHT:
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    X += 1
                    X = min(width - wall_length + 1, X)
                    if wall['type'] == 'horizontal' and X > (width - wall_length):
                        wall['type'] = 'vertical'
                    wall['location'] = (X, Y)

            elif command == 'r':
                if walls_installed != 0:
                    wall = wall_list[len(wall_list) - 1]
                    if wall['type'] == 'horizontal':
                        wall['type'] = 'vertical'
                    elif wall['type'] == 'vertical':
                        wall['type'] = 'horizontal'

            elif command == 'b':
                if walls_installed != 0:
                    if wall['type'] in p[(X, Y)]:
                        player['amount_of_walls'] -= walls_installed
                        ready = True
                else:
                    ready = False

            elif command == 's':
                if walls_installed != 0:
                    removed_wall = wall_list.pop()
                    (X, Y) = removed_wall['location']
                    walls_installed -=1
                ready = False
                second_stage = False

            elif command == 'q':
                quit = True
                ready = True
            else:
                pass
            draw(player_list, wall_list, curscr)
    return quit
