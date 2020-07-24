from random import random, randint
from math import atan, sin, cos, pi
import tkinter as tk

#GLOBAL VARIABLES
winWidth = 1000
winHeight = 1000
maxMass = 1000
minMass = 100
G = 6.67408 * 10**(-3)


# planet class
class Planet:
	def __init__(self, x, y, xvel, yvel, mass):
		self.x = x
		self.y = y
		self.xvel = xvel
		self.yvel = yvel
		self.mass = mass
		self.radius = (self.mass / pi) ** (1/3)
	
	# used to adjust the x velocity of the planet
	def addXVel(self, xaccel):
		self.xvel += xaccel
	
	# used to adjust the y velocity of the planet
	def addYVel(self, yaccel):
		self.yvel += yaccel
	
	# used to adjust the x position of the planet according to its velocity
	def moveX(self):
		self.x += self.xvel
	
	# used to adjust the y position of the planet according to its velocity
	def moveY(self):
		self.y += self.yvel
	
	# used to draw the planet on the given canvas
	def draw(self, canvas):
		canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill = "white")

# returns an list of 'num' planets with random x and y coordinates, and mass from minMass to maxMass
def startPlanets(num):
	# list to store the planets
	planets = []

	for i in range(num):
		# generates random on-screen coordinates for each planet
		x = randint(0, winWidth)
		y = randint(0, winHeight)

		# generates a random mass within the global variable limits
		mass = randint(minMass, maxMass)

		# adds the created planet to the list
		planets.append(Planet(x, y, 0, 0, mass))
	
	return planets

# takes an array of planets and updates their velocities based on their proximity and masses. returns the updated array
def calcVelocities(arr):
	# loops through each planet and each other planet to calculate forces and from that, velocities
	for i in arr:
		for j in arr:
			# determines the distance between the planets
			xdist = i.x - j.x
			ydist = i.y - j.y
			dist = ( (xdist**2) + (ydist**2) ) ** (1/2)
			
			# force is 0 if distance is 0, so no calculations are necessary
			if dist != 0:
				# determines the force applied on planet i by planet j
				force = G * i.mass * j.mass / (dist**2)

				# determines the acceleration from the force
				accel = force / i.mass
				
				# applies the found acceleration to each velocity component
				i.addXVel(-accel * (i.x - j.x))
				i.addYVel(-accel * (i.y - j.y))
	return arr

# takes an array of planets and updates their positions based on their velocities. returns the updated array
def movePlanets(arr):
	for i in arr:
		i.moveX()
		i.moveY()
	return arr


# takes an array of planets and checks for collisions. collided planets will be merged. returns updated array
#TODO

# takes an array of planets and draws them to the given canvas
def drawPlanets(arr, canvas):
	for i in arr:
		i.draw(canvas)

# runs the simulation for 'numFrames' frames
def runSim(numFrames):
	# sets up tk window etc
	root = tk.Tk()
	root.wm_title = ("N-body Simulation")
	canvas = tk.Canvas(root, width = winWidth, height = winHeight, bg = 'black')
	canvas.grid(row = 0, column = 0)
	# intializes "time" to 0
	t = 0

	planets = startPlanets(25)

	while t < numFrames:
		t += 1
		canvas.delete("all")
		planets = calcVelocities(planets)
		planets = movePlanets(planets)
		
		drawPlanets(planets, canvas)

		canvas.update()
	mainloop()

if __name__ == '__main__':
	runSim(10000)
