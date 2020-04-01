
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    initial_alpha = arm.getArmAngle()[0]
    initial_beta = arm.getArmAngle()[1]
    alpha_limit = arm.getArmLimit()[0]
    beta_limit = arm.getArmLimit()[1]
    rows = int((alpha_limit[1]-alpha_limit[0])/(granularity) + 1)
    cols = int((beta_limit[1]-beta_limit[0])/(granularity) + 1)
    maze_Map = [[SPACE_CHAR for x in range(cols)] for y in range(rows)]
    alpha = alpha_limit[0]
    beta = beta_limit[0]
    alpha_index = 0
    offset = [] 
    offset.append(alpha)
    offset.append(beta)
    start_val = angleToIdx((initial_alpha, initial_beta), offset, granularity)


    for i in range(rows):
        for j in range (cols):
                arm.setArmAngle(idxToAngle((i,j), offset, granularity))

                armPosDist = arm.getArmPosDist()
                armPos = arm.getArmPos()
                armEnd = arm.getEnd()


                if(doesArmTouchObjects(armPosDist, obstacles, False) == True):
                    maze_Map[i][j] = WALL_CHAR
                
                elif(isArmWithinWindow(armPos, window) == False):
                    maze_Map[i][j] = WALL_CHAR

                elif(doesArmTouchObjects(armPosDist, goals, True) == True):
                    maze_Map[i][j] = OBJECTIVE_CHAR

                elif(doesArmTouchObjects(armPosDist, goals, True) == True and doesArmTipTouchGoals(armEnd, goals) == False):
                    maze_Map[i][j] = WALL_CHAR

    maze_Map[start_val[0]][start_val[1]] = START_CHAR

    return Maze(maze_Map, [alpha_limit[0], beta_limit[0]], granularity)

    