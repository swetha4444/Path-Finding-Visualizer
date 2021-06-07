import pygame
import sys
import math
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from cell import Cell

#* -----------------------  Main Screen -----------------------
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))

#* -----------------------  Initialize Variables    -----------------------
cols = 50
row = 50
openSet = []
closedSet = []
purple = (128,0,128)
teal = (173,216,230)
blue = (0, 0, 255)
black = (0, 0, 0)
end.show((255, 50, 50), 0)
start.show((50, 255, 50), 0)
w = 600 / cols
h = 600 / row
cameFrom = []
grid = [0 for i in range(cols)]


#* -----------------------  Creating Grid   -----------------------
# create 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]
# Create Spots
for i in range(cols):
    for j in range(row):
        grid[i][j] = Cell(pygame, screen, w, h, row, cols, i, j)
# Display Grid
for i in range(cols):
    for j in range(row):
        grid[i][j].show((0, 0, 0), 1)


#* -----------------------  Marking boundaries  -----------------------
for i in range(0,row):
    grid[0][i].show(black, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].show(black, 0)
    grid[i][row-1].show(black, 0)
    grid[i][0].show(black, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True

#* -----------------------  Default Settings    -----------------------
# Set start and end node
start = grid[12][5]
end = grid[3][6]
#Algorithm choice
option = 'A*'
#heuristic choice
h_option = 'Euclidean'
#initial layout choice
m_option = 'Blank'

#* -----------------------  Create Menu -----------------------
window = Tk()
label = Label(window, text='Start (x,y) : ')

# Start Cell
startBox = Entry(window)
startBox.grid(row=0, column=1, pady=3)

#End Cell
endBox = Entry(window)
label1 = Label(window, text='End (x,y) : ')

#Menu Options
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
algoType = StringVar(window)
heur = StringVar(window)
mazeType = StringVar(window)

#List with options
choices = [ 'A*','Dijkstra','DFS','BFS' ]
h_choices = [ 'Euclidean', 'Manhattan']
m_choices = [ 'Blank','Random' ]

#Set the default option
algoType.set(option)
heur.set(h_option)
mazeType.set(m_option)

#Heur Dropdown Menu
def change_heuristic(*args):
    global h_option
    h_option = heur.get()
    print( h_option )
hMenu = OptionMenu(window, heur, *h_choices, command=change_heuristic)

#Algo Dropdown Menu
def change_dropdown(*args):
    global choices
    c_option = heur.get()
    print( c_option )
popupMenu = OptionMenu(window, algoType, *choices, command=change_dropdown)

#Maze Dropdown Menu
def change_layout(*args):
    global m_option
    m_option = mazeType.get()
    print( m_option )
mMenu = OptionMenu(window, mazeType, *m_choices, command=change_layout)

#Handle Submit
def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()
submit = Button(window, text='Submit', command=onsubmit)

#Adding Labels
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
Label(window, text="Algorithm:").grid(row=2, pady=3, padx=3)
popupMenu.grid(row=2, column=1, pady=3)
Label(window, text="Heuristic:").grid(row=4, pady=3, padx=3)
hMenu.grid(row=4, column=1, pady=3)
Label(window, text="Starting Layout:").grid(row=5, pady=3, padx=3)
mMenu.grid(row=5, column=1, pady=3)
Label(window, text="1 ≤ x ≤ 48 and 1 ≤ y ≤ 48").grid(row=6, column=0, pady=3, padx=25)
Label(window, text="Use cursor to draw walls.").grid(row=7, column=0, pady=3, padx=25)
Label(window, text="Press 'SPACE' to start.").grid(row=8, column=0, pady=3, padx=25)
showPath.grid(columnspan=2, row=9, pady=3)
submit.grid(columnspan=2, row=10)

#* -----------------------  Inititialize Menu and Start Game -----------------------
window.update()
mainloop()
pygame.init()
openSet.append(start)

#* -----------------------  Inititialize Game as per menu options -----------------------
#Randomize Maze
if m_option == 'Random':
    for i in range(1,cols-1):
        for j in range(1,row-1):
            if random.choice([1, 2, 3, 4]) == 2 and grid[i][j]!=start and grid[i][j]!=end :
                grid[i][j].obs = True
                grid[i][j].show(black, 0)

def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // cols)
    g2 = w // (600 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show(black, 0)
