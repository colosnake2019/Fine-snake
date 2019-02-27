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
    # set body positions
    snakes_bodies = get_snakes_body_positions(data['board']['snakes'])
    for body_frag in snakes_bodies:
        board[body_frag['y']][body_frag['x']] = 1
        
    # set head positions and longer snakes' potential next head positions
    snakes_heads = get_snakes_head_positions(data['board']['snakes'], data['you']['id'], len(data['you']['body']))

    for head_frag in snakes_heads:
        if((head_frag['y']>=0) and (head_frag['y']<board_height) and (head_frag['x']>=0) and (head_frag['x']<board_width)):
            board[head_frag['y']][head_frag['x']] = 1

    # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    #   for row in board]))

    orderedFoodList = OrderedDict(sorted(foodList.items()))
    return board, orderedFoodList.values()

# this method will return an array of coordinates of all the snakes' bodies.
def get_snakes_body_positions(snakes):
    result = []
    for snake in snakes:
        snake_body = snake['body'][1:]
        for body_fragment in snake_body:
            result.append(body_fragment)
    return result;

# this method will return an array of coordinates of all the other snakes' current head positions and longer snakes' potential next-step head positions
def get_snakes_head_positions(snakes, self_id, self_length):
    result = []
    for snake in snakes:
        if(snake['id'] != self_id):
            snake_head_current = snake['body'][0]
            result.append(snake_head_current)
            snake_length = len(snake['body'])
            if (snake_length >= self_length):
                #the longer snake's (or same-length snake) potential next-step head position
                cur_x = snake_head_current['x']
                cur_y = snake_head_current['y']
                result.append({'x':cur_x, 'y': cur_y-1})#up
                result.append({'x':cur_x, 'y': cur_y+1})#down
                result.append({'x':cur_x+1, 'y': cur_y})#right
                result.append({'x':cur_x-1, 'y': cur_y})#left
        else:
            snake_head_current = snake['body'][0]
            result.append(snake_head_current)

    return result;

# this method will return an array of food positions. 
def get_food_positions(data):
    return data['board']['food'];


# this method should be removed later
# this method will get the direction options of my snake head (avoid walls, bodies, heads, and longer snakes' potential next head positions)
def next_direction_options(data, board, foodList, current_pos):
    # print 'data:' , data
    print 'turn: ', data['turn']
    print 'current pos: ', current_pos
    direction = data['turn']
    next_pos = DFS(current_pos, foodList[0], board)
    print 'next pos: ', next_pos
    if next_pos[0]==current_pos[0]:
        direction = ('up' if next_pos[1]>current_pos[1] else 'down')
    if next_pos[1]==current_pos[1]:
        direction = ('left' if next_pos[1]>current_pos[1] else 'right')

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
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    # print(json.dumps(data))
    start_time = time.time()
    print("data is "+str(data))
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']
    board_, foodList = setBoard(data, (x,y))
    direction = next_direction_options(data, board_, foodList, (x,y))
    print 'get next direction: ', direction
    print("--- %s seconds ---" % (time.time() - start_time))
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






