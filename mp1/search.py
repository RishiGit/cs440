# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

import queue, math, sys

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.Queue()
    q.put(maze.getStart())
    traversed = []
    path = []
    tracker = {maze.getStart(): None} #Tracker needs to contain tuples

    while q:
        curr_loc = q.get() 

        if curr_loc not in traversed: #Add to traversed points list
            traversed.append(curr_loc)

            if maze.isObjective(curr_loc[0], curr_loc[1]): #Reached end of maze
                finished = curr_loc 
                break

            nextpath = maze.getNeighbors(curr_loc[0], curr_loc[1]) #Search neighbor points
            for point in nextpath:
                if point not in traversed and maze.isValidMove(point[0], point[1]):
                    q.put(point)
                    tracker[point] = curr_loc #Update curr_loc

    while finished:
        path.insert(0, finished) 
        finished = tracker[finished]

    return path
    

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.PriorityQueue()
    q.put((1, maze.getStart(), 0))
    traversed = []
    path = []
    tracker = {maze.getStart(): None} #Tracker needs to contain tuples

    while q:
        curr_loc = q.get()

        if curr_loc[1] not in traversed: #Add to traversed points list
            traversed.append(curr_loc[1])

            if maze.isObjective(curr_loc[1][0], curr_loc[1][1]):
                finished = curr_loc[1]
                break

            nextpath = maze.getNeighbors(curr_loc[1][0], curr_loc[1][1]) #Search neighbor points
            for point in nextpath:
                if point not in traversed and maze.isValidMove(point[0], point[1]):
                    q.put((manhattan_distance(point, maze) + curr_loc[2] + 1, point, curr_loc[2] + 1))
                    tracker[point] = curr_loc[1]

    while finished:
        path.insert(0, finished)
        finished = tracker[finished]

    return path

def manhattan_distance(loc, maze):
    goals = maze.getObjectives()
    curr_size = sys.maxsize
    for goal in goals:
        size = abs(loc[0] - goal[0]) + abs(loc[1] - goal[1])
        if size < curr_size:
            curr_size = size

    return curr_size


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    path = []
    endpoints = maze.getObjectives()
    start_point = maze.getStart()
    end_point = maze.getStart()

    while len(endpoints) > 0:
        end_point = endpoints[0]
        endpoints.pop(0)
        path.extend(astar_helper(start_point, end_point, maze))
        start_point = end_point

    path.extend(astar_helper(start_point, end_point, maze))

    i = 0
    while i < len(path):
        if path[i] == path[i+1]:
            path.remove(path[i])
        i = i + 1

    return path


def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    path = []
    endpoints = maze.getObjectives()
    start_point = maze.getStart()
    end_point = maze.getStart()

    while len(endpoints) > 0:
        end_point = endpoints[0]
        endpoints.pop(0)
        path.extend(astar_helper(start_point, end_point, maze))
        start_point = end_point

    path.extend(astar_helper(start_point, end_point, maze))

    i = 1
    while i < len(path):    
        if path[i] == path[i-1]:
            path.pop(i)
            i -= 1  
        i += 1
  
    return path



def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []

def astar_helper(start, end, maze):

    q = queue.PriorityQueue()
    q.put((1, start, 0))
    traversed = []
    path = []
    tracker = {start: None} #Tracker needs to contain tuples

    while q:
        curr_loc = q.get()

        if curr_loc[1] not in traversed: #Add to traversed points list
            traversed.append(curr_loc[1])

            if end in curr_loc:
                finished = curr_loc[1]
                break

            nextpath = maze.getNeighbors(curr_loc[1][0], curr_loc[1][1]) #Search neighbor points
            for point in nextpath:
                if point not in traversed and maze.isValidMove(point[0], point[1]):
                    q.put((manhattan_distance2(point, end) + curr_loc[2] + 1, point, curr_loc[2] + 1))
                    tracker[point] = curr_loc[1]

    while finished:
        path.insert(0, finished)
        finished = tracker[finished]

    return path

def manhattan_distance2(start, end):
    size = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return size
