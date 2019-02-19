# 2019 COLO SNAKE
# Author: Catherine, Chloe, Licht, Olivia
# ----------------------------------------------------------------------------------------------------------
import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
#------------------------------------------------methods----------------------------------------------
#TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#get the direction options of my snake head (avoid walls, self body, others' bodies, longer snakes' heads)
def next_direction_options(data):
    directions = []
    print(data["you"], "heihei")
    my_head = data['you']['body'][0] #{"x": 4, "y": 4}
    my_head_x = my_head['x']
    my_head_y = my_head['y']
    #check if we can move up
    if (my_head['y']-1 >= 0):#avoid the wall
        next_head_loc = {'x': my_head_x, 'y': my_head_y-1}
        if ((next_head_loc in data['you']['body'][0:-1])==False):#avoid self bodies

            directions.append('up')

    #check if we can move right
    if (my_head['x']+1 <= (data['board']['width']-1)):
        next_head_loc = {'x': my_head_x+1, 'y': my_head_y}
        if ((next_head_loc in data['you']['body'][0:-1])==False):
            directions.append('right')

    #check if we can move down
    if (my_head['y']+1 <= (data['board']['height']-1)):
        next_head_loc = {'x': my_head_x, 'y': my_head_y+1}
        if ((next_head_loc in data['you']['body'][0:-1])==False):
            directions.append('down')

    #check if we can move left
    if (my_head['x']-1 >= 0):
        next_head_loc = {'x': my_head_x-1, 'y': my_head_y}
        if ((next_head_loc in data['you']['body'][0:-1])==False):
            directions.append('left')
    return directions;


#-------------------------------------------API calls------------------------------------------------------
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
    print(json.dumps(data))

    color = "#FF69B4"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))
    print(data)

    # directions = ['up', 'down', 'left', 'right']
    directions = next_direction_options(data)
    direction = random.choice(directions)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

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






