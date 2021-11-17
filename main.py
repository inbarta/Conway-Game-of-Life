import pygame, sys
import random
from pygame.locals import *


def start_game(rows, cols):
    '''
    Bullding the first matrix
    rows - number of rows
    cols - number of cols
    '''

    matrix = [['*'] * cols for row in range(0, rows)]  # matrix of 'dead' cells
    for row in range(rows):
        for col in range(cols):
            if random.randint(0, 3) == 0:  # 1/3 chance to 'wake up'
                matrix[row][col] = 'O'
    return matrix


def next_gen(matrix, rows, cols):
    '''
    Makeing the next gen matrix
    matrix - the old gen matrix
    rows - number of rows
    cols - number of cols
    '''

    new_gen_matrix = [['*'] * cols for row in range(0, rows)]  # making a new 'dead' matrix
    for row in range(0, len(matrix)):
        for col in range(0, len(matrix[1])):
            new_gen_matrix[row][col] = get_neighbours([row, col], matrix, cols, rows)  # check if cell need to wake up
    return new_gen_matrix


def get_neighbours(cell, matrix, cols, rows):
    '''
    Checks if cell need to wake up
    cell - [row,col] - the location of the cell
    matrix - the old gen matrix
    cols - number of cols
    rows - number of rows
    '''

    neigbours = []  # list of cell neigbours
    if cell[0] - 1 >= 0:  # check all the sides of the cell witout getting out of index
        neigbours.append(matrix[cell[0] - 1][cell[1]])
    if cell[0] - 1 >= 0 and cell[1] - 1 >= 0:
        neigbours.append(matrix[cell[0] - 1][cell[1] - 1])
    if cell[0] - 1 >= 0 and cell[1] + 1 < cols:
        neigbours.append(matrix[cell[0] - 1][cell[1] + 1])
    if cell[1] - 1 >= 0:
        neigbours.append(matrix[cell[0]][cell[1] - 1])
    if cell[1] + 1 < cols:
        neigbours.append(matrix[cell[0]][cell[1] + 1])
    if cell[0] + 1 < rows and cell[1] - 1 >= 0:
        neigbours.append(matrix[cell[0] + 1][cell[1] - 1])
    if cell[0] + 1 < rows:
        neigbours.append(matrix[cell[0] + 1][cell[1]])
    if cell[0] + 1 < rows and cell[1] + 1 < cols:
        neigbours.append(matrix[cell[0] + 1][cell[1] + 1])
    count = 0  # number of neigbours thats awake
    for sign in neigbours:
        if sign == 'O':
            count += 1  # if awake add 1
    if matrix[cell[0]][cell[1]] == 'O':  # if the cell is awake we need 2 or 3 awake neigbours to stay awake
        if count not in [2, 3]:
            return '*'
    else:
        if count != 3:  # if cell is dead we need 3 neigbours to become awake
            return '*'
    return 'O'


pygame.init()  # start the pygame program

size = (width, height) = 600, 350  # screen size
win = pygame.display.set_mode(size)
clock = pygame.time.Clock()

s = 5  # size of grid
cols, rows = int(win.get_width() / s), int(win.get_height() / s)  # get cols and rows
matrix = start_game(rows, cols)  # making the first matrix

while True:  # main loop
    # while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if user press on X quit
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))  # paint the backround
    for i in range(cols):  # paint the dead or awake cells
        for j in range(rows):
            x = i * s
            y = j * s
            if matrix[j][i] == 'O':
                pygame.draw.rect(win, (200, 14, 71), (x, y, s, s))
            elif matrix[j][i] == '*':
                pygame.draw.rect(win, (0, 0, 0), (x, y, s, s))
            pygame.draw.line(win, (20, 20, 20), (x, y), (x, height))
            pygame.draw.line(win, (20, 20, 20), (x, y), (width, y))
    new_matrix = []  # empty new gen matrix
    new_matrix = next_gen(matrix, rows, cols)  # fill the new gen matrix
    matrix = new_matrix  # step into the new gen

    pygame.display.flip()