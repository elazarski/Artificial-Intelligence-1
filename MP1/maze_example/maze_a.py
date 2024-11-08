#!/usr/bin/python3

# imports
import numpy as np
import queue

class MazeState():
    SPACE = 0
    WALL = 1
    EXIT = 2
    START = (0, 0)

    def __init__(self, conf=(0,0), g=0, predState=None):
        self.maze = np.genfromtxt('maze_input.txt', delimiter=',')
        self.state = conf
        self.gcost = g
        self.pred = predState
        self.action_prof_pred = None

        # will only work with one exit to the maze
        temp = np.where(self.maze == MazeState.EXIT)
        self.exit_coords = (temp[0][0], temp[1][0])
        self.hcost = abs(self.state[0] - self.exit_coords[0]) + abs(self.state[1] - self.exit_coords[1])
        self.fcost = self.gcost + self.hcost

    def __str__(self):
        a = np.array(self.maze)
        a[self.state] = 4
        return np.str(a)

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.fcost < other.fcost

    def __hash__(self):
        # for visited nodes
        return self.state.__hash__()

    def is_goal(self):
        return self.maze[self.state] == MazeState.EXIT

    def get_coords(self, direction):
        if direction == 'up':
            return (self.state[0]-1, self.state[1])
        elif direction == 'down':
            return (self.state[0]+1, self.state[1])
        elif direction == 'left':
            return (self.state[0], self.state[1]-1)
        elif direction == 'right':
            return (self.state[0], self.state[1]+1)
        else:
            raise('wrong direction for checking move!')

    def can_move(self, direction):
        # determine possible coordinates
        coords = self.get_coords(direction)

        # check if coordinates are valid
        if (coords[0]<0 or coords[0]>=self.maze.shape[0]) or (coords[1]<0 or coords[1]>=self.maze.shape[1]):
            return False
        else:
            return self.maze[coords] == MazeState.SPACE or self.maze[coords] == MazeState.EXIT

    def gen_next_state(self, direction):
        s = MazeState(tuple(self.state), self.gcost+1, self)
        coords = self.get_coords(direction)
        s.state = coords
        s.action_from_pred = direction
        return s

    move = 0
    def show_path(self):
        # recursive!
        if self.pred is not None:
            self.pred.show_path()

        if MazeState.move == 0:
            print('START')
        else:
            print('Move', MazeState.move, ' Action ', self.action_from_pred)

        MazeState.move = MazeState.move + 1
        print(self)


# get ready for loop
frontier = queue.PriorityQueue()
start_state = MazeState()
frontier.put(start_state)
closed_set = set()

# loop/algorithm
while not frontier.empty():
    next_state = frontier.get()

    # expand state
    if next_state.is_goal():
        # show solution
        break

    # add next_state to explored/closed set
    closed_set.add(next_state)
    possible_moves = ['up', 'down', 'left', 'right']
    for move in possible_moves:
        if next_state.can_move(move):
            neighbor = next_state.gen_next_state(move)
            if neighbor in closed_set:
                continue
            elif neighbor not in frontier.queue:
                frontier.put(neighbor)
            elif neighbor in frontier.queue:
                # replace if neightor.fcost < frontier's.fcost
                temp_list = list(frontier.queue)
                for l in temp_list:
                    if l == neighbor:
                        if neighbor.fcost < l.fcost:
                            temp_list.remove(neighbor)
                            temp_list.append(neighbor)
                            
                frontier = queue.PriorityQueue()
                for l in temp_list:
                    frontier.put(l)

next_state.show_path()
