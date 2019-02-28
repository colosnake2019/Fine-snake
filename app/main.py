# 2019 COLO SNAKE
# Author: Catherine, Chloe, Licht, Olivia
# ----------------------------------------------------------------------------------------------------------
import json
import os
import random
import bottle
from dfs import DFS,get_distance
from collections import OrderedDict
import time

from api import ping_response, start_response, move_response, end_response
#------------------------------------------------methods----------------------------------------------

# -----------------------------
# | 0 | 0 | 5 | 0 | 0 | 0 | 8 |
# -----------------------------
# | 0 | 1 | 1 | 1 | 0 | 0 | 0 |
# -----------------------------
# | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
# -----------------------------
# | 1 | 0 | 0 | 0 | 0 | 5 | 0 |
# -----------------------------
# | 1 | 0 | 0 | 5 | 0 | 0 | 0 |
# -----------------------------
# | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
# -----------------------------
# | 0 | 5 | 0 | 0 | 0 | 1 | 1 |
# -----------------------------
# 0: safe 1: danger 5:food 

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
        board[y][x] = 5
        food_pos = (x,y)
        distance = get_distance(current_pos, food_pos)
        foodList[distance] = food_pos


    snakes = data['board']['snakes']
    for snake in snakes:
        # set body position
        snake_body = snake['body'][1:]
        for body_frag in snake_body:
            board[body_frag['y']][body_frag['x']] = 1

        # set head position
        snake_head = snake['body'][0]
        board[snake_head['y']][snake_head['x']] = 1

        # reopen tail position (if there's no food around a snake's head, open its tail position)
        snake_tail = snake['body'][-1]
        around_cells = get_around_cells(snake_head, board_width)
        occupied = 0
        for each_cell in around_cells:
            if(board[each_cell['y']][each_cell['x']]==5):
                occupied = 1
        if ((occupied == 0) and (len(snake['body']) >= 4)):
            board[snake_tail['y']][snake_tail['x']] = 0

        # set longer snakes' potential next head positions    (TBD)
        snake_length = len(snake['body'])
        self_length = len(selfsnake['body'])
        if((snake['id']!=selfsnake['id']) and (snake_length>=self_length)):
            for each_cell in around_cells:
                board[each_cell['y']][each_cell['x']] = 1


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
    print 'turn: ', data['turn']
    print 'current pos: ', current_pos
    # direction = data['turn']
    direction = 'up'
    next_pos = DFS(current_pos, destination, board)
    if(next_pos is None):
        return None
    print 'next pos: ', next_pos
    if next_pos[0]==current_pos[0]:
        direction = ('up' if next_pos[1]<current_pos[1] else 'down')
    if next_pos[1]==current_pos[1]:
        direction = ('left' if next_pos[0]<current_pos[0] else 'right')

    return direction

# pick a random safe direction(-------TODO-------)
def hover(board, head, board_width):
    direction = 'up'
    cells = get_around_cells({'x': head[0], 'y': head[1]}, board_width)
    for cell in cells:
        if (board[cell['y']][cell['x']] != 1):
            if cell['x']==head[0]:
                direction = ('up' if cell['y']<head[1] else 'down')
            if cell['y']==head[1]:
                direction = ('left' if cell['x']<head[0] else 'right')
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

    color = "#FF69B4"
    headType = "silly"
    tailType = "bolt"

    return start_response(color, headType, tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """

    Stratege:
        if just had a food (100 health)
            pick a random safe direction (TODO need to be modified)

        if health>=80 
            chase the tail
        
        else
            look for each food (closest to farthest)
                if there's a path from head to food, and a path from food to tail (perfect!) 
                    return direction
                else
                    continue the for loop
            
            all food has been visited, and no safe food can be found
                chase tail(TODO need to be modified)

    """


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

    # had a food at this step, do not chase the tail (find longest path to the tail) (------TODO-------)
    if ((health == 100) and len(data['you']['body'])>=4):
        print('!!=============HOVER==============!!')
        direction = hover(board_, head, data['board']['width'])
        print 'next direction: ', direction
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        return move_response(direction)

    # if (health>=80):
    if (health>=80):
        # chasing the tail     (---------TODO----------if there's no path to the tail...) 
        print('!!=============TAIL==============!!')  
        direction = next_direction(data, board_, tail, head)
        print 'next direction: ', direction
        print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
        return move_response(direction)
    else:
        # chasing the food in sequence
        print('!!=============FOOD==============!!')
        for food in foodList:    
            direction_head_to_food = next_direction(data, board_, food, head)
            # if there's a path from head to food
            if (direction_head_to_food is not None):
                direction_food_to_tail = next_direction(data, board_, tail, food)
                # if there's a path from the food to tail
                if (direction_food_to_tail is not None):
                    direction = direction_head_to_food
                    print 'next direction: ', direction
                    print("--- %s miliseconds ---" % int((time.time() - start_time) * 1000))
                    return move_response(direction)
                    
        # no path find for all of the food (----------TODO-----------)            
        direction = next_direction(data, board_, tail, head)
        print 'next direction: ', direction
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






