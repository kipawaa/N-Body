from random import random, randint
from math import pi
import tkinter as tk
from multiprocessing import Pool
import os

from copy import deepcopy

from planet import Planet
from constants import *

class Simulation():
    def __init__(self,
        num_planets: int,
        max_velocity: float=MAX_INITIAL_VELOCITY,
        min_mass: float=MIN_MASS,
        max_mass: float=MAX_MASS) -> None:
    
        """
        creates a Simulation with the following properties:
        - random x and y coordinates
        - initial velocities in a random direction with magnitude up to max_velocity
        - mass from min_mass to max_mass
        """

        self.num_planets = num_planets
        self.planets = []

        for _ in range(num_planets):
            # generates random on-screen coordinates for each planet
            x = randint(0, WINWIDTH)
            y = randint(0, WINHEIGHT)

            # generate velocities conditioned on intialVelocity
            xvel = random() * 2 * max_velocity - max_velocity
            yvel = random() * 2 * max_velocity - max_velocity

            # generates a random mass within the global variable limits
            mass = randint(min_mass, max_mass)

            # store the Planet
            self.planets.append(Planet(x, y, xvel, yvel, mass))


    def collisionDetection(self):
        """
        Determines if any Planets in planets have collided, and combines any that
        have.
        """

        for target_planet in self.planets:
            # stores which planets the target planet has collided with
            collided = []
            for secondary_planet in self.planets:
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
                    self.planets.remove(planet)

                # adds the new planet to the active planets list
                self.planets.append(Planet(x, y, xvel, yvel, mass))


    def draw(self):
        """
        draws Planets planets to the tkinter canvas canvas
        """

        for planet in self.planets:
            planet.draw(self.canvas)


    def run(self, collisions=True):
        """
        Creates a tkinter canvas and simulation with num_planets Planets.
        """

        # sets up tk window etc
        root = tk.Tk()
        root.wm_title = ("N-body Simulation")
        self.canvas = tk.Canvas(root, 
                                width=WINWIDTH, 
                                height=WINHEIGHT, 
                                bg='black')
        self.canvas.grid(row=0, 
                         column=0)

        # get max number of processes
        num_processes = max(1, 
                            min(self.num_planets // 200, 
                                os.process_cpu_count()))

        t = 0

        # runs the simulation for a given number of frames
        while True:
            t +=1
            print(t)
            
            # remove all old objects from the canvas
            self.canvas.delete("all")

            # update the planets (velocity, then position, then
            # check for collisions, then draw)
            with Pool(num_processes) as pool:
                self.planets = pool.starmap(update_planet, [(planet, self.planets) for planet in self.planets])

            if (collisions):
                self.collisionDetection()

            self.draw()

            # update the canvas
            self.canvas.update()
        mainloop()
        root.destroy()

def update_planet(planet, planets):
    """
    Computes velocity and position update for Planet planet.
    """
    planet = deepcopy(planet)

    planet.overallVelocity(planets)
    planet.move(WINWIDTH, WINHEIGHT)

    return planet

if __name__ == '__main__':
    # calls the function to run the simulation with a set time limit and
    # number of planets
    collisions = input(COLLISION_MENU)
    if (collisions == 'y'):
        collisions = True
    else:
        collisions = False
    sim = Simulation(100, collisions)
    sim.run()
