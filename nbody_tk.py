from random import random, randint
from math import pi
import tkinter as tk
import multiprocessing as mp

#TODO
'''
trailing lines
specific simulations (solar system, balanced dual planet, etc.)
'''

#GLOBAL VARIABLES
winWidth = 1650
winHeight = 1000

# planet class
class Planet:
	# constructor for the class
	def __init__(self, x, y, xvel, yvel, mass):
		self.x = x
		self.y = y
		self.xvel = xvel
		self.yvel = yvel
		self.mass = mass
		# sets the radius to scale according to the mass (kept small by the exponent for screen size limitations and visual purposes)
		self.radius = (self.mass / pi) ** (1/3)
	
	# used to adjust the x velocity of the planet
	def addXVel(self, xaccel):
		self.xvel += xaccel
	
	# used to adjust the y velocity of the planet
	def addYVel(self, yaccel):
		self.yvel += yaccel
	
	# used to adjust the position of the planet according to its velocity
	def move(self):
		self.x += self.xvel
		self.y += self.yvel
	
	# determines the change in velocity for this planet due to the force applied by 'planet'
	def calcVelocity(self, secondary_planet):
		# determines the distance between the planets
		xdist = self.x - secondary_planet.x
		ydist = self.y - secondary_planet.y
		dist = ( (xdist**2) + (ydist**2) ) ** (1/2)
		
		# force is 0 if distance is 0, so no calculations are necessary
		if dist != 0:
			# determines the force applied on self by planet secondary
			force = 6.67408 * 10**(-4) * self.mass * secondary_planet.mass / (dist**2)

			# determines the acceleration from the force
			accel = force / self.mass
			
			# applies the found acceleration to each velocity component
			self.addXVel(-accel * (self.x - secondary_planet.x))
			self.addYVel(-accel * (self.y - secondary_planet.y))
	
	# uses calcVelocity to change self's velocity according to gravtitational forces from planets
	def overallVelocity(self, planets):
		for planet in planets:
			self.calcVelocity(planet)

	# used to draw the planet on the given canvas
	def draw(self, canvas):
		canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill = "white")

# returns an list of 'num' planets with random x and y coordinates, and mass from minMass to maxMass
def startPlanets(num, initialVelocity=1, maxVelocity=10, minMass=100, maxMass=1000):
	# list to store the planets
	planets = []

	for i in range(num):
		# generates random on-screen coordinates for each planet
		x = randint(0, winWidth)
		y = randint(0, winHeight)

		# this applies a little bit of "branchless programming" but achieves the same as saying "if initialVelocity then randomize intial velocities, otherwise set to 0"
		xvel = 0 + initialVelocity * randint(-maxVelocity, maxVelocity)
		yvel = 0 + initialVelocity * randint(-maxVelocity, maxVelocity)

		# generates a random mass within the global variable limits
		mass = randint(minMass, maxMass)

		# adds the created planet to the list
		planets.append(Planet(x, y, xvel, yvel, mass))
	
	return planets

# takes an array of planets and updates their velocities based on their proximity and masses. returns the updated array
# gravity should be 10**(-11) but this results in EXTREMELY slow moving simulations, so it has been strengthened for practical purpose
def calcVelocities(planets):
	# loops through each planet and each other planet to calculate forces and from that, velocities
	for planet in planets:
		planet.overallVelocity(planets)

# takes an array of planets and updates their positions based on their velocities. returns the updated array
def movePlanets(planets, keepOnScreen=True):
	for planet in planets:
		# adjusts the x and y coordinates of each planet
		planet.move()

		# ensures that planets are stopped if they reach or pass the edge of the screen
		if keepOnScreen:
			if planet.x - planet.radius < 0:
				planet.x = 0 + planet.radius
				planet.xvel = 0
			if planet.y - planet.radius < 0:
				planet.y = 0 + planet.radius
				planet.yvel = 0
			if planet.x + planet.radius > winWidth:
				planet.x = winWidth - planet.radius
				planet.xvel = 0
			if planet.y + planet.radius > winHeight:
				planet.y = winHeight - planet.radius
				planet.yvel = 0

# takes an array of planets and checks for collisions. collided planets will be merged. returns updated array
def collisionDetection(planets):
	for target_planet in planets:
		# stores which planets the target planet has collided with
		collided = []
		for secondary_planet in planets:
			# determines which planets have collided with the target
			dist = ( (target_planet.x - secondary_planet.x)**2 + (target_planet.y - secondary_planet.y)**2) **(1/2)
			if dist < target_planet.radius + secondary_planet.radius:
				collided.append(secondary_planet)

		# if collisions have occurred, combines the planets and removes them from the original array
		if len(collided) > 0:
			x = 0
			y = 0
			xvel = 0
			yvel = 0
			mass = 0
			# determine mass first in order to scale velocities properly later
			for planet in collided:
				mass += planet.mass
			
			# determines the rest of the parameters
			for planet in collided:
				# x, y, xvel and yvel are scaled according to mass for more "realistic" collisions
				x += planet.x * planet.mass / mass
				y += planet.y * planet.mass / mass
				xvel += planet.xvel * planet.mass / mass
				yvel += planet.yvel * planet.mass / mass

				# removes the planets once they're no longer needed for calculations
				planets.remove(planet)
			
			# adds the new planet to the active planets list
			planets.append(Planet(x, y, xvel, yvel, mass))

# takes an array of planets and draws them to the given canvas
def drawPlanets(planets, canvas):
	for planet in planets:
		planet.draw(canvas)

# runs the simulation for 'numFrames' frames (limited as a safety feature, prevents program from running infinitely if numPlanets is naively set very high (recommended <250))
def runSim(numFrames, numPlanets):
	# sets up tk window etc
	root = tk.Tk()
	root.wm_title = ("N-body Simulation")
	canvas = tk.Canvas(root, width = winWidth, height = winHeight, bg = 'black')
	canvas.grid(row = 0, column = 0)

	# intializes "time" to 0
	t = 0

	# creates all the initial planets
	planets = startPlanets(numPlanets, True)

	# runs the simulation for a given number of frames
	while t < numFrames:
		# increment the frame/time counter
		t += 1

		# remove all old objects from the canvas
		canvas.delete("all")

		# update the planets information (velocity, then position, then check for collisions)
		calcVelocities(planets)
		movePlanets(planets)
		collisionDetection(planets)
		
		# draw the planets
		drawPlanets(planets, canvas)
		
		# update the canvas
		canvas.update()
	mainloop()
	root.destroy()

if __name__ == '__main__':
	# calls the function to run the simulation with a set time limit and number of planets
	runSim(50000, 250)
	#dualOrbitSim(50000)
