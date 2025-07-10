from random import random, randint
from math import pi
import tkinter as tk
import multiprocessing as mp

from planet import Planet

# GLOBAL VARIABLES
WINWIDTH = 1650
WINHEIGHT = 1000


def startPlanets(
    numPlanets,
    initialVelocity=1,
    maxVelocity=10,
    minMass=100,
     maxMass=1000):
    
    """
    returns a list of numPlanets Planets with the following properties:
    - random x and y coordinates
    - mass from minMass to maxMass
    """

    planets = []

    for _ in range(numPlanets):
        # generates random on-screen coordinates for each planet
        x = randint(0, WINWIDTH)
        y = randint(0, WINHEIGHT)

        # generate velocities conditioned on intialVelocity
        xvel = 0 + initialVelocity * randint(-maxVelocity, maxVelocity)
        yvel = 0 + initialVelocity * randint(-maxVelocity, maxVelocity)

        # generates a random mass within the global variable limits
        mass = randint(minMass, maxMass)

        # store the Planet
        planets.append(Planet(x, y, xvel, yvel, mass))

    return planets


def calcVelocities(planets):
    """
    updates the velocities of Planets in planets based on their proximity and
    masses.
    """

    for planet in planets:
        planet.overallVelocity(planets)


def movePlanets(planets, keepOnScreen=True):
    """
    takes an array of planets and updates their positions based on their
    velocities. returns the updated array
    """

    for planet in planets:
        # adjusts the x and y coordinates of each planet
        planet.move()

        # ensures that planets are stopped if they reach or pass the edge of
        # the screen
        if keepOnScreen:
            if planet.x - planet.radius < 0:
                planet.x = 0 + planet.radius
                planet.xvel = 0
            if planet.y - planet.radius < 0:
                planet.y = 0 + planet.radius
                planet.yvel = 0
            if planet.x + planet.radius > WINWIDTH:
                planet.x = WINWIDTH - planet.radius
                planet.xvel = 0
            if planet.y + planet.radius > WINHEIGHT:
                planet.y = WINHEIGHT - planet.radius
                planet.yvel = 0


def collisionDetection(planets: list[Planet]):
    """
    Determines if any Planets in planets have collided, and combines any that
    have.
    """

    for target_planet in planets:
        # stores which planets the target planet has collided with
        collided = []
        for secondary_planet in planets:
            # determines which planets have collided with the target
            dist = ((target_planet.x - secondary_planet.x)**2 + (target_planet.y - secondary_planet.y)**2) ** (1/2)
            if dist < target_planet.radius + secondary_planet.radius:
                collided.append(secondary_planet)

        # if collisions have occurred, combines the planets and removes them
        # from the original array
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
                # x, y, xvel and yvel are scaled according to mass for more
                # "realistic" collisions
                x += planet.x * planet.mass / mass
                y += planet.y * planet.mass / mass
                xvel += planet.xvel * planet.mass / mass
                yvel += planet.yvel * planet.mass / mass

                # removes the planets once they're no longer needed for
                # calculations
                planets.remove(planet)

            # adds the new planet to the active planets list
            planets.append(Planet(x, y, xvel, yvel, mass))


def drawPlanets(planets, canvas):
    """
    draws Planets planets to the tkinter canvas canvas
    """

    for planet in planets:
        planet.draw(canvas)



def runSim(numFrames, numPlanets, collisions=True):
    """
    creates a tkinter canvas and simulation with numPlanets Planets.
    """

    # sets up tk window etc
    root = tk.Tk()
    root.wm_title = ("N-body Simulation")
    canvas = tk.Canvas(root, width=WINWIDTH, height = WINHEIGHT, bg = 'black')
    canvas.grid(row=0, column = 0)

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

        # update the planets information (velocity, then position, then check
        # for collisions)
        calcVelocities(planets)
        movePlanets(planets)
        if (collisions):
            collisionDetection(planets)

        # draw the planets
        drawPlanets(planets, canvas)

        # update the canvas
        canvas.update()
    mainloop()
    root.destroy()


def twoPlanet(numFrames):
    root = tk.Tk()
    root.wm_title = ("Two Planet")
    canvas = tk.Canvas(root, width=WINWIDTH, height = WINHEIGHT, bg = 'black')
    canvas.grid(row=0, column = 0)

    t = 0

    planet1 = Planet(WINWIDTH /2 - 100, WINHEIGHT /2 - 100, 0, -1.5, 10000)
    planet2 = Planet(WINWIDTH /2 + 100, WINHEIGHT /2 + 100, 0, 1.5, 10000)
    planets = [planet1, planet2]

    while t < numFrames:
        t += 1

        canvas.delete("all")

        calcVelocities(planets)
        movePlanets(planets)
        collisionDetection(planets)

        drawPlanets(planets, canvas)

        canvas.update()
    mainloop()
    root.destroy()


if __name__ == '__main__':
    # calls the function to run the simulation with a set time limit and
    # number of planets
    user = int(input(
        "Menu:\ninput 1 to run a regular, randomized simulation\ninput 2 to see a two planet simulation\nenter your choice:"))
    if (user == 1):
        collisions = input(
            "input 'y' to enable collision detection, 'n' to disable")
        if (collisions == 'y'):
            collisions = True
        else:
            collisions = False
        runSim(50000, 200, collisions)
    if (user == 2):
        twoPlanet(50000)
