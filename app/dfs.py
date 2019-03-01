
from collections import OrderedDict

# 0/5: safe 1:danger
def isSafe(x, y, board, goal):
    if y<0 or y>(len(board)-1):
        return False
    if x<0 or x>(len(board[0])-1):
        return False
    if (x,y) == goal and get_distance(goal, cur_pos) > 1:
        print('goal tail is 1')
        return True
    return board[y][x] == 0 or board[y][x] == 5;

# calculate the distance between two points
def get_distance(start, end):
    distance = ((start[0]-end[0])**2)+((start[1]-end[1])**2)
    return distance

# in this method, could optimal the child list, like put them in order and check the security
def createChild(position, goal, board): 
    childList = {}
    # all these check should be covered by method isSafe(), we don't need the board_width and board_height
    # right now just write like this for testing
    x = position[0]
    y = position[1]

    if isSafe(x-1, y, board, goal):
        next = (x-1,y)
        childList[get_distance(next, goal)] = next
    if isSafe(x+1, y, board, goal):
        next = (x+1,y)
        childList[get_distance(next, goal)] = next
    if isSafe(x, y-1, board, goal):
        next = (x,y-1)
        childList[get_distance(next, goal)] = next
    if isSafe(x, y+1, board, goal):
        next = (x,y+1)
        childList[get_distance(next, goal)] = next

    sorted_children = OrderedDict(sorted(childList.items(), reverse = True))
    return sorted_children.values()


def DFS(current_pos, goal_state, board):
    global cur_pos
    cur_pos = current_pos
    print ('goal_state', goal_state)
    childrenStates = createChild(current_pos, goal_state, board)
    childrenStates = childrenStates[::-1]
    for child in childrenStates: 
        if dfs_solution(child, goal_state, board):
            print ('path exist from ', current_pos, ' to ', goal_state)
            return child

    print ('no path from ', current_pos, ' to ', goal_state)
    return None

def dfs_solution(current_pos, goal_state, board):
    frontier = createChild(current_pos, goal_state, board)
    frontier.append(current_pos)
    trackExplored = {}
    explored = []
    explored.append(current_pos)
    trackExplored[current_pos] = 0
    while frontier:
        node = frontier.pop()
        if node not in trackExplored:
            explored.append(node)
            trackExplored[node] = 0
        if node == goal_state:
            return True
        child_list = createChild(node, goal_state, board)
        frontier.extend(child for child in child_list if child not in trackExplored and child not in frontier)
    print(explored)
    return False
