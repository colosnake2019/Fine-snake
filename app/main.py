# 2019 COLO SNAKE
# Author: Catherine, Chloe, Licht, Olivia
# ----------------------------------------------------------------------------------------------------------
import json
import os
import random
import bottle
from dfs import DFS,get_distance, createChild
from collections import OrderedDict
import time

from api import ping_response, start_response, move_response, end_response
#------------------------------------------------methods----------------------------------------------

# -----------------------------
# | 0 | 0 | -1 | 0 | 0 | 0 | 0 |
# -----------------------------
# | 0 | 4 | 4 | 4 | 0 | 0 | 0 |
# -----------------------------
# | 0 | -1 | 0 | 0 | 0 | 0 | 0 |
# -----------------------------
# | 4 | 0 | 0 | 0 | 0 | -1 | 0 |
# -----------------------------
# | 4 | 0 | 0 | -1 | 0 | 0 | 0 |
# -----------------------------
# | 4 | 4 | 0 | 0 | 0 | 4 | 0 |
# -----------------------------
# | 0 | -1 | 0 | 0 | 0 | 4 | 4 |
# -----------------------------
# 0: food, 0: safe, 2: position will be reached in 2 steps, 3: in 1 step, 4:dangerous 

def setBoard(data, current_pos):
    selfsnake = data['you']
    board_width = data['board']['width']
    board_height = data['board']['height']
    board = [[0 for x in range(board_width)] for y in range(board_height)]

    foodList = {}
    # set food positions
    food = get_food_positions(data)
    for each_food in food:
        y = each_food['y']
        x = each_food['x']
        board[y][x] = 0
        food_pos = (x,y)
        distance = get_distance(current_pos, food_pos)
        foodList[distance] = food_pos

    snakes = data['board']['snakes']
    for snake in snakes:
        print ('snake body', snake['body'])
        # set body position
        snake_body = snake['body'][1:]
        for body_frag in snake_body:
            board[body_frag['y']][body_frag['x']] = 4

        # set head position
        snake_head = snake['body'][0]
        board[snake_head['y']][snake_head['x']] = 4

        # reopen tail position (if the snake didnt eat at this step, reopen its tail position)
        if((snake['health']!=100) and (snake['body'][-1]!=snake['body'][-2])):
            snake_tail = snake['body'][-1]
            board[snake_tail['y']][snake_tail['x']] = 0

        # (----------------TODO-------------------)
        # set longer snakes' potential next head positions    
        snake_length = len(snake['body'])
        self_length = len(selfsnake['body'])
        if((snake['id']!=selfsnake['id']) and (snake_length>=self_length)):
            around_cells_1 = get_around_cells(snake['body'][0], board_width)
            for each_cell_1 in around_cells_1:
                cell = board[each_cell_1['y']][each_cell_1['x']]
                if (cell==0): #or cell==-1
                    board[each_cell_1['y']][each_cell_1['x']] = 3 # next 1 step
                around_cells_2 = get_around_cells(each_cell_1, board_width)
                for each_cell_2 in around_cells_2:
                    cell =  board[each_cell_2['y']][each_cell_2['x']]
                    if(cell==0): #or cell==-1
                        board[each_cell_2['y']][each_cell_2['x']] = 2 # next 2 step


    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in board]))

    orderedFoodList = OrderedDict(sorted(foodList.items()))
    # print(board)
    return board, orderedFoodList.values()

# up, down, left, right cell coordinates of a cell
def get_around_cells(cell, board_width):
    cells = []
    x = cell['x']
    y = cell['y']
    if (y-1>=0): cells.append({'x': x, 'y': y-1}) #up
    if (y+1<=board_width-1): cells.append({'x': x, 'y': y+1}) #down
    if (x+1<=board_width-1): cells.append({'x': x+1, 'y': y}) #right
    if (x-1>=0): cells.append({'x': x-1, 'y': y}) #left
    return cells

# this method will return an array of food positions. 
def get_food_positions(data):
    return data['board']['food'];

# this method will return the next direction e.g. 'up'
def next_direction(data, board, destination, current_pos):
    # print 'data:' , data
    print ('turn: ', data['turn'])
    print ('current pos: ', current_pos)
    # direction = data['turn']
    direction = 'up'
    next_pos = DFS(current_pos, destination, board)
    if(next_pos is None):
        return None
    print ('next pos: ', next_pos)
    if next_pos[0]==current_pos[0]:
        direction = ('up' if next_pos[1]<current_pos[1] else 'down')
    if next_pos[1]==current_pos[1]:
        direction = ('left' if next_pos[0]<current_pos[0] else 'right')

    return direction

def chaseFood(foodList, data, board_, head, tail, flag):
    close_food = []
    food_sub_list = foodList
    if (len(foodList)>=4):
        food_sub_list = foodList[0:4]
    for food in food_sub_list:
        direction_head_to_food = next_direction(data, board_, food, head)
        if direction_head_to_food is not None: # check there is path from head to food
            # if flag == 1 means the game just start, no need to test path from food to tail
            if (flag == 1) or (next_direction(data, board_, tail, food) is not None): # check there is path from food to tail
                # or (get_distance(tail, food) > 225)
                print('There is path from food ', food, 'to tail')
                return direction_head_to_food
    return None


def safeCheck(x, y, board):
    if y<0 or y>(len(board)-1):
        return False
    if x<0 or x>(len(board[0])-1):
        return False
    return board[y][x] == 0 # or board[y][x] == -1

# (-----------TODO---------------)
def finalChoice(position, board):
    x = position[0]
    y = position[1]
    direction = "right"

    if safeCheck(x-1, y, board):
        print("go left safe!")
        direction = "left"
    if safeCheck(x+1, y, board):
        print("go right safe!")
        direction = "right"
    if safeCheck(x, y-1, board):
        print("go up safe!")
        direction = "up"
    if safeCheck(x, y+1, board):
        print("go down safe!")
        direction = "down"
    # no way to go, then whatever
    print("final choice direction:", direction)
    return direction

#------------------------------------------------API calls------------------------------------------------------
@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    # print(json.dumps(data))

    color = "#e6e600"
    headType = "silly"
    tailType = "bolt"

    return start_response(color, headType, tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json
    direction = 'up' #initialize a direction

    # draw the board
    start_time = time.time()
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']
    head = (x,y)
    tail_pos_x = data['you']['body'][-1]['x']
    tail_pos_y = data['you']['body'][-1]['y']
    tail = (tail_pos_x, tail_pos_y)
    board_, foodList = setBoard(data, head)

    health = data['you']['health']

    # at the beginning of the game, chase food and increase length to 5
    if (len(data['you']['body'])<=5):
        print('!!=============LENGTH<=5 CHASE FOOD==============!!')
        direction = chaseFood(foodList, data, board_, head, tail, 1)
        if direction is None:
            direction = finalChoice(head, board_)
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        print('next direction: ', direction)
        print('move', move_response(direction))
        return move_response(direction)

    #(---------TODO---------- if eat a food at this step, DFS to tail doesnt work, so chase tail around) 
    if (health == 100):
        print('!!========HEALTH FULL, CHASE TAIL==============!!') 
        direction = next_direction(data, board_, tail, head)
        if direction is None:
            print('!!=============CHASE FOOD==============!!') 
            direction = chaseFood(foodList, data, board_, head, tail, 0)
        if direction is None:
            print('!!=========HEALTH FULL, NO PATH TO FOOD, FINAL==============!!')
            direction = finalChoice(head, board_)
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        return move_response(direction)

    if (health>=70): # chasing the tail 
        print('!!==========Health>=70, CHASE TAIL==============!!') 
        print("health",health) 
        direction = next_direction(data, board_, tail, head)
        # (------------TODO------------- if there's no path to the tail)
        if direction is None:
            print('!!=============Health>=70, NO PATH TO TAIL, CHASE FOOD=========!!')
            print("health",health)   
            direction = chaseFood(foodList, data, board_, head, tail, 0)
        if direction is None:
            print('!!=============Health>=70, NO PATH TO TAIL, FINAL==========!!')
            direction = finalChoice(head, board_)
        print ('next direction: ', direction)
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        return move_response(direction)
    else:
        # chasing the food in sequence
        print('!!============Health<70 CHASE FOOD==============!!')
        direction = chaseFood(foodList, data, board_, head, tail, 0)
        if direction is not None:
            print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
            print('direction', direction)
            return move_response(direction)
                    
        # no path find for all of the food (----------TODO-----------)   
        print('!!=============NO FOOD!! GO TAIL==============!!')         
        direction = next_direction(data, board_, tail, head)
        if direction is None:
            print('!!=============NO FOOD!! NO TO TAIL, FINAL==============!!')
            direction = finalChoice(head, board_)
        print ('next direction: ', direction)
        print('move', move_response(direction))
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        return move_response(direction)

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )





