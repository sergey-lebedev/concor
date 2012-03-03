# -*- coding: utf-8 -*-
def user_turn(player, wall_list, available_positions, players, width, height):
    command = raw_input()
    (x, y) = player['location']
    loc = (x, y)
    (X, Y) = wall_list[0]['location']        
    if (command == 'i'):
        if (x, y - 1) in available_positions[loc]:
            players[x][y] = 0
            y -= 1
            y = max(0, y)
            player['location'] = (x, y)
            players[x][y] = 1  
    elif (command == 'j'):
        if (x - 1, y) in available_positions[loc]:
            players[x][y] = 0    
            x -= 1
            x = max(0, x)
            player['location'] = (x, y)
            players[x][y] = 1 
    elif (command == 'k'):
        if (x, y + 1) in available_positions[loc]:
            players[x][y] = 0    
            y += 1
            y = min(height-1, y)
            player['location'] = (x, y)
            players[x][y] = 1 
    elif (command == 'l'):
        if (x + 1, y) in available_positions[loc]:
            players[x][y] = 0    
            x += 1
            x = min(width-1, x)
            player['location'] = (x, y)
            players[x][y] = 1
    elif (command == 'I'):
        walls[X][Y] = 0    
        Y -= 1
        Y = max(1, Y)
        if (wall_list[0]['type'] == 'vertical') & (Y <= 1):
            wall_list[0]['type'] = 'horizontal'
        wall_list[0]['location'] = (X, Y)
        walls[X][Y] = 1 
    elif (command == 'J'):
        walls[X][Y] = 0    
        X -= 1
        X = max(1, X)
        if (wall_list[0]['type'] == 'horizontal') & (X <= 1):
            wall_list[0]['type'] = 'vertical'
        wall_list[0]['location'] = (X, Y)
        walls[X][Y] = 1 
    elif (command == 'K'):
        walls[X][Y] = 0    
        Y += 1
        Y = min(height - wall_length + 1, Y)
        if (wall_list[0]['type'] == 'vertical') & (Y > height - wall_length):
            wall_list[0]['type'] = 'horizontal'
        wall_list[0]['location'] = (X, Y)
        walls[X][Y] = 1 
    elif (command == 'L'):
        walls[X][Y] = 0    
        X += 1
        X = min(width - wall_length + 1, X)
        if (wall_list[0]['type'] == 'horizontal') & (X > width - wall_length):
            wall_list[0]['type'] = 'vertical'
        wall_list[0]['location'] = (X, Y)
        walls[X][Y] = 1
    elif (command == 'R'):
        if (wall_list[0]['type'] == 'horizontal'):
            wall_list[0]['type'] = 'vertical'   
        elif (wall_list[0]['type'] == 'vertical'):
            wall_list[0]['type'] = 'horizontal'       
    elif (command == 'N'):
        wall_list.insert(0, {'type': 'horizontal', 'location': (1, 1)})                
    elif (command == 'q'):
        end = True
    elif (command == 'q!'):
        end = True
        win = True
    else:
        pass

def bot_turn(bot_type, player, wall_list, available_positions, players, width, height):
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        pass
    else:
        pass
