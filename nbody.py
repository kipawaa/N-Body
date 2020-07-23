from random import random, randint
from time import time
from math import pi
from Graphics_Functions import *

#class to create and manage planets
class Planet:
    def __init__(self, x, y, xvel, yvel, mass):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass
        self.radius = (self.mass/pi)**(1/2)

    def addXVel(self, x):
        self.xvel += x

    def addYVel(self, y):
        self.yvel += y
    
    def moveX(self, x):
        self.x += x

    def moveY(self, y):
        self.y += y

#places a given number of planets
def startScene(low, high):
    numPlanets = randint(low, high)
    planets = []
    for i in range(numPlanets):
        x = randint(0, 1280)
        y = randint(0, 710)
        mass = randint(100, 1000)
        planets.append(Planet(x, y, 0, 0, mass))
    return planets

#changes the velocities of the planets
def calcVelocities(arr):
    print('Calculating Velocities...')
    G = 6.67408*10**(-11)

    for i in arr:
        for j in arr:
            xdist = i.x-j.x
            ydist = i.x-j.x

            xforce = G*i.mass*j.mass*xdist
            yforce = G*i.mass*j.mass*ydist

            xaccel = xforce/i.mass
            yaccel = yforce/i.mass

            i.addXVel(xaccel)
            i.addYVel(yaccel)
        print(i.xvel, i.yvel)
    print('Velocities Calculated.')
    return arr

#is used to move planets and detet collisions
def movePlanets(arr):
    print('Moving Planets...')

    i = 0
    #cycles through all planets
    while i < len(arr)-1:
        #moves each planet
        arr[i].moveX(arr[i].xvel)
        arr[i].moveY(arr[i].yvel)
        
        j = 0
        while j < len(arr)-1:
            xdist = arr[i].x-arr[j].x
            ydist = arr[i].y-arr[j].y
            dist = (xdist**2 + ydist**2)**(1/2)

            #checks for collisions
            if dist < (arr[i].radius+arr[j].radius):
                arr.append(Planet((arr[i].x+arr[j].x)/2, (arr[i].y+arr[j].y)/2, arr[i].xvel+arr[j].xvel, arr[i].yvel+arr[j].yvel, arr[i].mass+arr[j].mass))
                arr.remove(arr[i])
                arr.remove(arr[j])
            j += 1
        i += 1
    print('Planets Moved.')
    return arr

#creates visual representation of an array of planets
def visualize(arr, win):
    print('visualizing the scene...')
    clearWin(win)
    for i in arr:
        circ = drawCircle(i.x, i.y, i.radius, 'black')
        circ.draw(win)
    print('visualized.')

#runs a simulation of Conway's Game of Life with Zelle Graphics
def graphicsRun():
    #creates a window
    win = prepWin('NBody Simulation', 1280, 710)

    #initializes a random set of planets
    planets = startScene(10, 15)

    visualize(planets, win)
    
    #runs the simulation continuously
    while True:
        win.getMouse()
        calcVelocities(planets)
        movePlanets(planets)

        visualize(planets, win)

graphicsRun()
