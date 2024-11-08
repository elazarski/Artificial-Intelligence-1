#!/usr/bin/python3

# Artificial Intelligence
# MP1: A* for Sliding Puzzle
# SEMESTER: Spring 1, 2019
# NAME: Eric Lazarski

# imports
import numpy as np
import queue

# print header
print('Artificial Intelligence')
print('MP1: A* for Sliding Puzzle')
print('SEMESTER: Spring 1 2019')
print('NAME: Eric Lazarski')
print("")

# puzzle state class
class PuzzleState():
    SPACE = 0
    GOAL = np.array([[0,1,2],[3,4,5],[6,7,8]])

    def __init__(self, state, g=0, predState=None):
        self.state = state
        self.coord_0 = np.where(self.state == 0)
        self.coord_0 = (self.coord_0[0][0], self.coord_0[1][0])

        self.gcost = g
        self.pred = predState
        self.action_from_pred = None

        self.hcost = 0
        for i in range(0,9):
            # placement of i in state
            i_coord = np.where(self.state == i)
            i_coord = (i_coord[0][0], i_coord[1][0])

            # placement of i in solution
            i_solut = np.where(PuzzleState.GOAL == i)
            i_solut = (i_solut[0][0], i_solut[1][0])
            
            # update hcost
            self.hcost += abs(i_coord[0] - i_solut[0]) + abs(i_coord[1] - i_solut[1])

        self.fcost = self.gcost + self.hcost

    def __str__(self):
        return np.str(self.state)

    def __eq__(self, other):
        # to check if in frontier
        return np.array_equal(self.state, other.state)

    def __lt__(self, other):
        # for queue
        return self.fcost < other.fcost

    def __hash__(self):
        # for visited nodes
        return hash(str(self.state))

    def is_goal(self):
        return np.array_equal(self.state, PuzzleState.GOAL)

    def get_new_coord_0(self, direction):
        if direction == 'up':
            return (self.coord_0[0]-1, self.coord_0[1])
        elif direction == 'down':
            return (self.coord_0[0]+1, self.coord_0[1])
        elif direction == 'left':
            return (self.coord_0[0], self.coord_0[1]-1)
        elif direction == 'right':
            return (self.coord_0[0], self.coord_0[1]+1)
        else:
            raise('wrong direction for moving 0!')

    def can_move(self, direction):
        coords = self.get_new_coord_0(direction)

        # make sure coordinates of 0 are valid
        in_x_bounds = not (coords[0]<0 or coords[0]>=self.state.shape[0])
        in_y_bounds = not (coords[1]<0 or coords[1]>=self.state.shape[1])

        if not in_x_bounds or not in_y_bounds:
            return False
        else:
            return True

    def gen_next_state(self, direction):
        # get placemet for 0 and what number it is swapping with
        new_coord_0 = self.get_new_coord_0(direction)
        num_at_new_coord = self.state[new_coord_0]

        # generate new state and swap
        next_state = np.array(self.state)
        next_state[new_coord_0] = 0
        next_state[self.coord_0] = num_at_new_coord

        # puzzlestate object        
        n = PuzzleState(next_state, self.gcost+1, self)
        n.action_from_pred = direction
        return n

    move = 0
    def show_path(self):
        if self.pred is not None:
            self.pred.show_path()

        if PuzzleState.move == 0:
            print('START')
        else:
            print('Move {0} Action: {1}'.format(PuzzleState.move, self.action_from_pred))

        PuzzleState.move = PuzzleState.move + 1
        print(self)

# prepare for loop
possible_moves = ['up', 'down', 'left', 'right']
frontier = queue.PriorityQueue()
puzzle_state = np.genfromtxt('mp1input.txt', delimiter=' ', dtype=int)
start_state = PuzzleState(puzzle_state)
frontier.put(start_state)
closed_set = set()

# loop/algorithm
while not frontier.empty():
    # get best step based on fcost
    next_state = frontier.get()
    
    # expand
    if next_state.is_goal():
        # show solution
        break

    # add next_state to closed set and get its neighbors
    closed_set.add(next_state)
    for move in possible_moves:
        if next_state.can_move(move):
            neighbor = next_state.gen_next_state(move)

            if neighbor in closed_set: # already visited
                continue
            elif neighbor not in frontier.queue: # haven't seen this before
                frontier.put(neighbor)
            elif neighbor in frontier.queue: # make sure we don't have a cheaper path with this one
                # replace the one in the queue if neighbor.fcost < frontier.fcost
                temp_list = list(frontier.queue)
                for l in temp_list:
                    if l == neighbor:
                        if neighbor.fcost < l.fcost:
                            temp_list.remove(l)
                            temp_list.append(neighbor)

                frontier = queue.PriorityQueue()
                for l in temp_list:
                    frontier.put(l)

# show solution
next_state.show_path()
print("")
print('Number of states visited = {0}'.format(len(closed_set)))
