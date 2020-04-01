# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
import queue, math, sys

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    q = queue.Queue()
    q.put(maze.getStart())
    traversed = []
    path = []
    tracker = {maze.getStart(): None} #Tracker needs to contain tuples

    while q:
        curr_loc = q.get() 

        if curr_loc not in traversed: #Add to traversed points list
            traversed.append(curr_loc)

            if maze.isObjective(curr_loc[0], curr_loc[1] ): #Reached end of maze
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
