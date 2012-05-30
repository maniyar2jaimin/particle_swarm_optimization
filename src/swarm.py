#!/usr/bin/env python

"""
Source: http://www.swarmintelligence.org/tutorials.php
(http://www.cs.tufts.edu/comp/150GA/homeworks/hw3/_reading6%201995%20particle%20swarming.pdf)

... PSO simulates the behaviors of bird flocking. Suppose the following scenario: a
group of birds are randomly searching food in an area. There is only one piece of food in the area
being searched. All the birds do not know where the food is. But they know how far the food is in
each iteration. So what's the best strategy to find the food? The effective one is to follow the
bird which is nearest to the food.

PSO learned from the scenario and used it to solve the optimization problems. In PSO, each single
solution is a "bird" in the search space. We call it "particle". All of particles have fitness
values which are evaluated by the fitness function to be optimized, and have velocities which direct
the flying of the particles. The particles fly through the problem space by following the current
optimum particles.

PSO is initialized with a group of random particles (solutions) and then searches for optima by
updating generations. In every iteration, each particle is updated by following two "best" values.
The first one is the best solution (fitness) it has achieved so far. (The fitness value is also
stored.) This value is called pbest. Another "best" value that is tracked by the particle swarm
optimizer is the best value, obtained so far by any particle in the population. This best value is a
global best and called gbest. When a particle takes part of the population as its topological
neighbors, the best value is a local best and is called lbest.

After finding the two best values, the particle updates its velocity and positions with following
equation (a) and (b).

v[] = v[] + c1 * rand() * (pbest[] - present[]) + c2 * rand() * (gbest[] - present[]) (a)
present[] = persent[] + v[] (b)

v[] is the particle velocity, persent[] is the current particle (solution). pbest[] and gbest[] are
defined as stated before. rand () is a random number between (0,1). c1, c2 are learning factors.
usually c1 = c2 = 2.

The pseudo code of the procedure is as follows

For each particle
    Initialize particle
END

Do
    For each particle
        Calculate fitness value
        If the fitness value is better than the best fitness value (pBest) in history
            set current value as the new pBest
    End

    Choose the particle with the best fitness value of all the particles as the gBest
    For each particle
        Calculate particle velocity according equation (a)
        Update particle position according equation (b)
    End
While maximum iterations or minimum error criteria is not attained

Particles' velocities on each dimension are clamped to a maximum velocity Vmax. If the sum of
accelerations would cause the velocity on that dimension to exceed Vmax, which is a parameter
specified by the user. Then the velocity on that dimension is limited to Vmax.
"""

import time
from random import randint, choice
from operator import add, sub, mul, mod

import pygame
from pygame.locals import *

screen_size = 640, 480
particle_pool = 100
initial_solution = 100, 100
learning_factors = 1, 1
maximum_velocity = 15
frame_rate = 35

solution_delta = (-120, 120)

center = screen_size[0]/2, screen_size[1]/2
radius = 100
points = [(center[0], center[1] - radius),
          (center[0] + radius, center[1]),
          (center[0], center[1] + radius),
          (center[0] - radius, center[1]),
          (center[0], center[1])]

class Coord(tuple):
    def __add__(self, other):
        return self.__class__(map(add, self, other))

    def __sub__(self, other):
        return self.__class__(map(sub, self, other))

    def __mul__(self, other):
        return self.__class__(map(mul, self, [other] * self.__len__()))

    def __abs__(self):
        return self.__class__(map(abs, self))

    def _mod_func(self, a, b):
        sign = cmp(b, 0)
        return sign * min(a, abs(b))

    def __mod__(self, other):
        return self.__class__(map(self._mod_func, [other] * self.__len__(), self))


class Particle(object):
    global_best = temp_global_best = Coord((0, 0))
    vmax = maximum_velocity
    solution = Coord(initial_solution)
    c1, c2 = learning_factors

    fitness_source =  None

    def __init__(self):
        self.local_best = self.position = self.old_position = Coord((randint(0,screen_size[0]), randint(0,screen_size[1])))
        self.velocity = Coord((0, 0))

    def plot(self):
        self.screen.set_at(self.old_position, (0, 0, 0))
        self.screen.set_at(self.position, (255, 255, 255))

    @classmethod
    def update_global_best(self):
        Particle.global_best = Particle.temp_global_best

    @classmethod
    def update_solution(self):
        self.solution = Coord((randint(0, screen_size[0]), randint(0, screen_size[1])))

    def tick(self):
        self._check_fitness()
        self._update_velocity()
        self._update_position()
        self.plot()

    def _update_velocity(self):
        self.velocity = (self.velocity +
                         (self.local_best - self.position) * self.c1 * randint(0,1) +
                         (Particle.global_best - self.position) * self.c2 * randint(0,1)
                        )
        self.velocity = self.velocity % self.vmax

    def _update_position(self):
        self.old_position = self.position
        self.position = self.position + self.velocity

    def _check_fitness(self):
        if self.__fitness(self.position) < self.__fitness(Particle.global_best):
            Particle.temp_global_best = self.position
        if self.__fitness(self.position) < self.__fitness(self.local_best):
            self.local_best = self.position

    def __fitness(self, position):
        return abs(self.solution[0] - position[0]) + abs(self.solution[1] - position[1])

    def _multiple_solutions(self):
        fitness = lambda solution, position: abs(solution[0] - position[0]) + abs(solution[1] - position[1])
        fitness_map = {}
        for solution in points:
            current_fitness = fitness(solution, self.position)
            fitness_map[current_fitness] = solution
        return min(fitness_map.keys())



def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    return screen


def initialize_particles(screen):
    particles = []
    for i in xrange(particle_pool):
        particle = Particle()
        particle.screen = screen
        particles.append(particle)
    return particles


def main():
    screen = initialize_screen()

    particles = initialize_particles(screen)

    initial_count = 30
    count = initial_count

    while 1:
        time.sleep(1.0/frame_rate)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        # count -= 1
        # if not count:
        #     Particle.update_solution()
        #     count = initial_count
        Particle.solution = Coord(pygame.mouse.get_pos())

        [particle.tick() for particle in particles]
        Particle.update_global_best()

        screen.blit(screen, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()
