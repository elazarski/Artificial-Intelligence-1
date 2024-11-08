#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Eric Lazarski
# 2/7/2019
# CPSC 57100 - Artificial Intelligence
# Spring 2019
# MP2


"""
Created on Fri Jan 18 14:30:21 2019

@author: szczurpi

Machine Problem 2
Gen-Tic-Tac-Toe Minimax Search with alpha/beta pruning
"""

import numpy as np
import random
import math

# self class is responsible for representing the game board
class GenGameBoard: 
    
    # Constructor method - initializes each position variable and the board size
    def __init__(self, boardSize):
        self.boardSize = boardSize  # Holds the size of the board
        self.marks = np.empty((boardSize, boardSize),dtype='str')  # Holds the mark for each position
        self.marks[:,:] = ' '
    
    # Prints the game board using current marks
    def printBoard(self): 
        # Prthe column numbers
        print(' ',end='')
        for j in range(self.boardSize):
            print(" "+str(j+1), end='')
        
        
        # Prthe rows with marks
        print("")
        for i in range(self.boardSize):
            # Prthe line separating the row
            print(" ",end='')
            for j in range(self.boardSize):
                print("--",end='')
            
            print("-")

            # Prthe row number
            print(i+1,end='')
            
            # Prthe marks on self row
            for j in range(self.boardSize):
                print("|"+self.marks[i][j],end='')
            
            print("|")
                
        
        # Prthe line separating the last row
        print(" ",end='')
        for j in range(self.boardSize):
            print("--",end='')
        
        print("-")
    
    
    # Attempts to make a move given the row,col and mark
    # If move cannot be made, returns False and prints a message if mark is 'X'
    # Otherwise, returns True
    def makeMove(self, row, col, mark):
        possible = False  # Variable to hold the return value
        if row==-1 and col==-1:
            return False
        
        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1
        
        if row<0 or row>=self.boardSize or col<0 or col>=self.boardSize:
            print("Not a valid row or column!")
            return False
        
        # Check row and col, and make sure space is empty
        # If empty, set the position to the mark and change possible to True
        if self.marks[row][col] == ' ':
            self.marks[row][col] = mark
            possible = True    
        
        # Prout the message to the player if the move was not possible
        if not possible and mark=='X':
            print("\nself position is already taken!")
        
        return possible
    
    
    # Determines whether a game winning condition exists
    # If so, returns True, and False otherwise
    def checkWin(self, mark):
        won = False # Variable holding the return value
        
        # Check wins by examining each combination of positions
        
        # Check each row
        for i in range(self.boardSize):
            won = True
            for j in range(self.boardSize):
                if self.marks[i][j]!=mark:
                    won=False
                    break        
            if won:
                break
        
        # Check each column
        if not won:
            for i in range(self.boardSize):
                won = True
                for j in range(self.boardSize):
                    if self.marks[j][i]!=mark:
                        won=False
                        break
                if won:
                    break

        # Check first diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[i][i]!=mark:
                    won=False
                    break
                
        # Check second diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[self.boardSize-1-i][i]!=mark:
                    won=False
                    break

        return won
    
    # Determines whether the board is full
    # If full, returns True, and False otherwise
    def noMoreMoves(self):
        return (self.marks!=' ').all()
    
    # checks if terminating state has been reached by
    # checking if comp or player has won then if
    # there are any moves left
    def terminalTest(self):
        termed = self.checkWin('O')
        if termed == False:
            termed = self.checkWin('X')
        if termed == False:
            termed = self.noMoreMoves()
        
        return termed

    # gets the utility of the current state
    # 1 if comp won, -1 if player won, 0 if draw
    def getUtility(self):
        if self.checkWin('O'):
            return 1
        elif self.checkWin('X'):
            return -1
        else:
            return 0

    # gets available actions
    def getActions(self):
        rows, cols = np.where(self.marks == ' ')
        availMarks = []
        for i in range(0, len(rows)):
            availMarks.append(tuple((rows[i]+1, cols[i]+1)))
        return availMarks
    
    # get best move for player given current state
    def minValue(self, alpha, beta):
        # check to make sure current state is not the end of a game
        if self.terminalTest():
            return self.getUtility()
        
        v = math.inf 
        
        # get available actions and loop over them
        # make action then get computer moves
        # select best option for human
        actions = self.getActions()
        for row, col in actions:
            self.makeMove(row, col, 'X')
            maxVal, maxAction = self.maxValue(alpha, beta)
            self.marks[row-1][col-1] = ' '
            if maxVal < v:
                v = maxVal

            # alpha/beta part
            if v < beta:
                beta = v
            if alpha >= beta:
                break # prune, stop searching
            
        return v
        
    # get best move for computer given current state
    def maxValue(self, alpha, beta):
        # check to make sure current state is not the end of a game
        if self.terminalTest():
            return self.getUtility(), None
        
        v = -math.inf
        
        # get available actions and loop over them
        # make action then get human moves
        # select the best option for computer
        actions = self.getActions()
        for row, col in actions:
            self.makeMove(row, col, 'O')
            minVal = self.minValue(alpha, beta)
            self.marks[row-1][col-1] = ' '
            if minVal > v:
                v = minVal
                bestAction = row, col
            
            # alpha/beta part
            if v >= alpha:
                alpha = v
            if alpha >= beta:
                break # prune, stop searching
        
        return v, bestAction
    
    # selects the best computer move based on alpha/beta
    # pruning
    def makeCompMove(self):
        # get best move for computer
        v, bestAction = self.maxValue(-math.inf, math.inf)
        self.makeMove(bestAction[0], bestAction[1], 'O')
        
        print("Computer chose: "+str(row)+","+str(col))
        
        

# Print out the header info
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Eric Lazarski")

LOST = 0
WON = 1
DRAW = 2    
wrongInput = False
boardSize = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))
        
# Create the game board of the given size
board = GenGameBoard(boardSize)
        
board.printBoard()  # Print the board before starting the game loop
        
# Game loop
while True:
    # *** Player's move ***        
    
    # Try to make the move and check if it was possible
    # If not possible get col,row inputs from player    
    row, col = -1, -1
    while not board.makeMove(row, col, 'X'):
        print("Player's Move")
        row, col = input("Choose your move (row, column): ").split(',')
        row = int(row)
        col = int(col)

    # Display the board again
    board.printBoard()
            
    # Check for ending condition
    # If game is over, check if player won and end the game
    if board.checkWin('X'):
        # Player won
        result = WON
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break
            
    # *** Computer's move ***
    board.makeCompMove()
    
    # Print out the board again
    board.printBoard()    
    
    # Check for ending condition
    # If game is over, check if computer won and end the game
    if board.checkWin('O'):
        # Computer won
        result = LOST
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break
        
# Check the game result and print out the appropriate message
print("GAME OVER")
if result==WON:
    print("You Won!")            
elif result==LOST:
    print("You Lost!")
else: 
    print("It was a draw!")

