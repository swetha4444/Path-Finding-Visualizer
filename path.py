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
w = 600 / cols
h = 600 / row
cameFrom = []
grid = [0 for i in range(cols)]

#* -----------------------  Creating Grid   -----------------------
# Create 2D array
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

#Marking boundaries
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

window = Tk()

# Start Cell
label = Label(window, text='Start (x,y) : ')
startBox = Entry(window)

#End Cell
label1 = Label(window, text='End (x,y) : ')
endBox = Entry(window)

#Menu Options
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
algoType = StringVar(window)
heur = StringVar(window)
mazeType = StringVar(window)

#List with options
choices = [ 'A*','DFS','BFS' ]
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
    option = algoType.get()
    print( option )
popupMenu = OptionMenu(window, algoType, *choices, command=change_dropdown)

#Maze Dropdown Menu
def change_layout(*args):
    global m_option
    m_option = mazeType.get()
    print( m_option )
mMenu = OptionMenu(window, mazeType, *m_choices, command=change_layout)


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

#Block Nodes
def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // cols)
    g2 = w // (600 // row)
    block = grid[g1][g2]
    if block != start and block != end:
        if block.obs == False:
            block.obs = True
            block.show(black, 0)

#Display Start and End Nodes
end.show((255, 50, 50), 0)
start.show((50, 255, 50), 0)

#Display Block Nodes
loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break


#* -----------------------  Execute Algorithm -----------------------
# Find Neighbours for all Cells
for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)

#Decide type of heurisitic
def heurisitic(n, e):
    if h_option == 'Euclidean':
        d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    elif h_option == 'Manhattan':
        d = abs(n.i - e.i) + abs(n.j - e.j)
    return d

def a_star():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    while len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance/least weighted path \n is ' + str(temp) + '\n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False

                            break
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    if var.get():
                        neighbor.show(teal,0)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
        
        if var.get() and current != start:
            current.show(purple,0)
        current.closed = True

def dfs():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    while len(openSet) > 0:
        current = openSet.pop(-1)
        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
            break

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            if not neighbors[i] in closedSet:
                openSet.append(neighbors[i])
                neighbors[i].previous = current
                neighbors[i].f = current.f + 1
                if var.get():
                    neighbors[i].show(teal,0)

        closedSet.append(current)
        if var.get() and current != start:
            current.show(purple,0)        
        
        current.closed = True

def bfs():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    current = start
    current.closed = True
    closedSet.append(current)
    while len(openSet) > 0:
        current = openSet.pop(0)
        if var.get() and current != start:
            current.closed = False
            current.show(purple,0) 
            current.closed = True

        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
            break

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            if not neighbors[i] in closedSet:
                openSet.append(neighbors[i])
                neighbors[i].previous = current
                neighbors[i].f = current.f + 1
                if var.get():
                    neighbors[i].show(teal,0)
                neighbors[i].closed = True
                closedSet.append(neighbors[i])  

def main():
    print( option )
    print( m_option )
    if option == 'A*':
        print( h_option )
        a_star()
    elif option == 'DFS':
        dfs()
    elif option == 'BFS':
        bfs()

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()

