from random import random, randint
from math import pi
import tkinter as tk
from multiprocessing import Pool
import os

from planet import Planet
from constants import *

def startPlanets(
        numPlanets: int,
        maxVelocity: float=MAX_INITIAL_VELOCITY,
        minMass: float=MIN_MASS,
        maxMass: float=MAX_MASS) -> list[Planet]:
    
    """
    returns a list of numPlanets Planets with the following properties:
    - random x and y coordinates
    - initial velocities in a random direction with magnitude up to maxVelocity
    - mass from minMass to maxMass
    """

    planets = []

    for _ in range(numPlanets):
        # generates random on-screen coordinates for each planet
        x = randint(0, WINWIDTH)
        y = randint(0, WINHEIGHT)

        # generate velocities conditioned on intialVelocity
        xvel = random() * 2 * maxVelocity - maxVelocity
        yvel = random() * 2 * maxVelocity - maxVelocity

        # generates a random mass within the global variable limits
        mass = randint(minMass, maxMass)

        # store the Planet
        planets.append(Planet(x, y, xvel, yvel, mass))

    return planets


def update_planet(planet, planets):
    """
    Computes velocity and position update for Planet planet.
    """

    planet.overallVelocity(planets)
    planet.move(WINWIDTH, WINHEIGHT)


def overall_velocity_wrapper(planet, planets):
    planet.overallVelocity(planets)


def calcVelocities(planets):
    """
    Updates the velocities of Planets in planets based on their proximity and
    masses.
    """

    #num_processes = len(planets) // 200

    #with Pool(max(1, min(num_processes, os.process_cpu_count()))) as pool:
    #    pool.starmap(overall_velocity_wrapper, ((planet, planets) for planet in planets))

    for planet in planets:
        planet.overallVelocity(planets)


def movePlanets(planets, keepOnScreen=True):
    """
    Updates the positions of Planets in planets based on their
    velocities.
    """

    for planet in planets:
        # adjusts the x and y coordinates of each planet
        planet.move(WINWIDTH, WINHEIGHT)


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


def runSim(numPlanets, collisions=True):
    """
    Creates a tkinter canvas and simulation with numPlanets Planets.
    """

    # sets up tk window etc
    root = tk.Tk()
    root.wm_title = ("N-body Simulation")
    canvas = tk.Canvas(root, width=WINWIDTH, height=WINHEIGHT, bg = 'black')
    canvas.grid(row=0, column = 0)

    # intializes "time" to 0
    t = 0

    # creates all the initial planets
    planets = startPlanets(numPlanets)

    # runs the simulation for a given number of frames
    while True:
        # increment the frame/time counter
        t += 1

        # remove all old objects from the canvas
        canvas.delete("all")

        #num_processes = max(1, 
        #                    min(len(planets) // 200, 
        #                        os.process_cpu_count() - 1))

        # update the planets information (velocity, then position, then check
        # for collisions)
        #with Pool(num_processes) as pool:
        #    pool.starmap(update_planet, ((planet, planets) for planet in planets))
        calcVelocities(planets)
        movePlanets(planets)

        if (collisions):
            collisionDetection(planets)

        drawPlanets(planets, canvas)

        # update the canvas
        canvas.update()
    mainloop()
    root.destroy()


if __name__ == '__main__':
    # calls the function to run the simulation with a set time limit and
    # number of planets
    collisions = input(COLLISION_MENU)
    if (collisions == 'y'):
        collisions = True
    else:
        collisions = False
    runSim(10, collisions)
