from random import random, randint
from math import pi
import tkinter as tk
import multiprocessing as mp
from typing import Self


class Planet:
    def __init__(self,
                 x: float,
                 y: float,
                 xvel: float,
                 yvel: float,
                 mass: float
                 ) -> None:
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass
        self.radius = (self.mass / pi) ** (1 / 3)

    def addXVel(self, xaccel: float) -> None:
        """
        adds xaccel to the planet's x velocity
        """

        self.xvel += xaccel

    def addYVel(self, yaccel: float) -> None:
        """
        adds yaccel to the planet's y velocity
        """

        self.yvel += yaccel

    def move(self, winWidth, winHeight):
        """
        updates the planet's x and y positions according to its current
        velocities
        """

        self.x += self.xvel
        self.y += self.yvel

        if winwidth:
            self.x = max(self.radius, self.x)
            self.x = min(self.x, winWidth - self.radius)

        if winHeight:
            self.y = max(self.radius, self.y)
            self.y = min(self.y, winHeight - self.radius)

    def calcVelocity(self, secondary_planet: Self):
        """
        determines the change in velocity for this planet due to the force
        applied by secondary_planet
        """

        # determines the distance between the planets
        xdist = self.x - secondary_planet.x
        ydist = self.y - secondary_planet.y
        dist = ((xdist**2) + (ydist**2)) ** (1 / 2)

        # force is 0 if distance is 0, so no calculations are necessary
        if dist != 0:
            # determines the force applied on self by secondary_planet
            force = 6.67408 * 10**(-4) * self.mass * \
                secondary_planet.mass / (dist**2)

            # determines the acceleration from the force
            accel = force / self.mass

            # applies the found acceleration to each velocity component
            self.addXVel(-accel * (self.x - secondary_planet.x))
            self.addYVel(-accel * (self.y - secondary_planet.y))

    def overallVelocity(self, planets: list[Self]):
        """
        updates the planet's velocity based on the force from all planets in
        planets
        """

        for planet in planets:
            self.calcVelocity(planet)

    def draw(self, canvas):
        """
        draws the planet to tkinter canvas canvas
        """

        canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill="white")
