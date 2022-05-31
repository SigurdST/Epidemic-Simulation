from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import Globals
from typing import Tuple
from Individual import Individual
import Illness
import Graph
import random
import Interface

Point = Tuple[float, float]


def t(p: QtCore.QPointF) -> Point:
    return p.x(), p.y()



def toss(a, b):
    return random.choice([a, b])


class Physics(QtWidgets.QGraphicsRectItem):
    size = Globals.envSize
    extent = size / 2
    bounds = QtCore.QRectF(-extent, -extent, size, size)

    def __init__(self):
        super().__init__(self.bounds)
        self.setZValue(-10)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addItem(self)
        al = .5 * 10
        self.scene.setSceneRect(Physics.bounds.adjusted(-al, -al, al, al))
        self.individuals_sane = []
        self.individuals_infected = []
        self.list_illness = []
        self.total_child = []
        self.total_death = []
        self.immunity = []
        self.virulence = []
        self.duration = []
        self.heal = []
        self.i = 0

    def add_ind_sane(self, x, y, a): # To add the sane individual on the scene and on the list
        ind = Individual(x, y, a)
        self.individuals_sane.append(ind)
        self.scene.addItem(ind)


    def add_ind_child(self, x, y, a, dad, mom): # To add the new born on the scene and on the list
        ind = Individual(x, y, a)
        ind.love = 0
        ind.c = True
        ind.alpha = toss(dad.alpha, mom.alpha) # The children have randomly the same genetic than his dad or his mom
        ind.beta = toss(dad.beta, mom.beta)
        ind.gamma = toss(dad.gamma, mom.gamma)
        ind.immunity = toss(dad.immunity, mom.immunity)
        self.individuals_sane.append(ind)
        self.total_child.append(ind)
        self.scene.addItem(ind)

    def add_ind_sane_rnd(self): # To put randomly the sane on the scene
        a = random.uniform(-Physics.extent, Physics.extent)
        r = random.uniform(-Physics.extent, Physics.extent)
        a2 = random.uniform(0, 359)
        self.add_ind_sane(a, r, a2)

    def add_ind_infected(self, x, y, a): # To add the infected individual on the scene and on the list
        ind = Individual(x, y, a)
        ind.sickness = Illness.Illness()
        ind.alpha = 0.5
        ind.beta = 0.5
        ind.gamma = 0.5
        ind.sickness.alpha = ind.alpha
        ind.sickness.alpha = ind.beta
        ind.sickness.alpha = ind.gamma
        self.individuals_infected.append(ind)
        self.scene.addItem(ind)

    def add_ind_infected_rnd(self): # To put randomly the sane on the scene
        a = random.uniform(-Physics.extent, Physics.extent)
        r = random.uniform(-Physics.extent, Physics.extent)
        a2 = random.uniform(0, 359)
        self.add_ind_infected(a, r, a2)

    def paint(self, painter, option, widget=None):
        painter.fillRect(self.bounds, Qt.black)

    def step(self): # What happen every step of the timer
        self.i += 1 # Step counter
        self.list_illness = [] # We initialize the list link to illness and immunity, because the values change every steps
        self.virulence = []
        self.duration = []
        self.immunity = []
        for a in self.individuals_sane: # Actions of the sanes
            a.move(self)
            a.transmission(self)
            a.reproduction(self, self.individuals_sane, Globals.Cs)
            self.immunity.append(a.immunity)
        for b in self.individuals_infected: # Actions of infected individuals
            b.sickness.mutationalpha()
            b.sickness.mutationbeta()
            b.sickness.mutationgamma()
            b.sickness.mutationd()
            b.sickness.mutationv()
            b.move(self)
            b.reproduction(self, self.individuals_infected, Globals.Ci)
            self.virulence.append(b.sickness.v) # We put the new values in the lists
            self.duration.append(b.sickness.d)
            self.list_illness.append(b.sickness)
            self.immunity.append(b.immunity)
            b.evolution(self)
        # To stock every value in every step to do graphs after the simulation
        Graph.text(self.individuals_sane, "testsane.txt")
        Graph.text(self.individuals_infected, "testinfected.txt")
        Graph.text(self.individuals_infected+self.individuals_sane, "testpop.txt")
        Graph.text(self.total_child, "testbirth.txt")
        Graph.text(self.total_death, "testdeath.txt")
        Graph.text(self.heal, "testheal.txt")
        Graph.mean(self.immunity, "testimmunity.txt")
        Graph.mean(self.virulence, "testvirulence.txt")
        Graph.mean(self.duration, "testduration.txt")







