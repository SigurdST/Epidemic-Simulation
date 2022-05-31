import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
import random
import math

import Globals
import Physics
import Illness


class Individual(QtWidgets.QGraphicsItem):  # The class that define all the individuals of the simulation
    pixRect = None
    length = Globals.IndLength
    half_length = .5 * length
    width = 2 * length / 3
    bounds = QtCore.QRectF(-.5 * length, -.5 * width, length, width)

    def __init__(self, x, y, a):
        super().__init__()
        self.setPos(x, y)
        self.setRotation(a)
        self.alpha = random.uniform(0, 1)
        self.beta = random.uniform(0, 1)
        self.gamma = random.uniform(0, 1)
        self.love = random.uniform(0, 1)
        self.c = False
        self.day_of_c = 0
        self.sickness = None
        self.healing = False
        self.sick = 0
        self.day_of_sickness = 0
        self.nb_of_c = 0
        self.immunity = random.uniform(0.5, 1.5)

    def boundingRect(self):
        return Individual.bounds

    def paint(self, painter, option, widget=None):  # To put color on the individuals
        painter.setBrush(QColor.fromRgbF(self.alpha, self.beta, self.gamma))
        # To paint each individual with the color correspondig to his genetic code
        if self.sickness is not None:
            if not self.healing:
                painter.setPen(QColor.fromRgbF(1, 0, 0))  # To put red outline if the individuals is infected
            else:
                painter.setPen(QColor.fromRgbF(1, 1, 0))  # To put yellow outline if the individuals is healing
        elif self.c:
            painter.setPen(QColor.fromRgbF(0, 0, 1))  # To put blue outline if the individuals is new born
            self.day_of_c += 1
            if self.day_of_c >= 500:
                self.c = False
        else:
            painter.setPen(
                QColor.fromRgbF(self.alpha, self.beta, self.gamma))  # To put an outline for the sane individuals
        painter.drawRect(Individual.bounds)

    def move(self, physics):  # To make the individuals moving
        a = self.rotation()
        ab = a + (random.uniform(-15, 15))
        p = Physics.t(self.pos())
        x, y = p
        ar = math.pi * ab / 180
        if abs(
                x) >= physics.extent - physics.extent / 100:  # To do a U-turn when the individual is at the border of the scene
            ab += 10
        if abs(y) >= physics.extent - physics.extent / 100:
            ab += 10
        self.setRotation(ab)  # To turn
        self.setPos(min(physics.extent, max(x - math.cos(ar), -physics.extent)),
                    min(physics.extent, max(y - math.sin(ar), -physics.extent)))  # To move

    def transmission(self, physics):  # To transmit the virus
        p = Physics.t(self.pos())
        x, y = p
        for i in physics.individuals_infected:  # We only select the infected individuals
            pi = Physics.t(i.pos())
            xi, yi = pi
            if self in physics.individuals_sane and self != i and \
                    xi - physics.extent / Globals.InfRadius <= x <= xi + physics.extent / Globals.InfRadius and \
                    yi - physics.extent / Globals.InfRadius <= y <= yi + physics.extent / Globals.InfRadius and \
                    self.alpha - Globals.CloseGenetic / self.immunity <= i.sickness.alpha <= self.alpha + Globals.CloseGenetic / self.immunity and \
                    self.beta - Globals.CloseGenetic / self.immunity <= i.sickness.beta <= self.beta + Globals.CloseGenetic / self.immunity and \
                    self.gamma - Globals.CloseGenetic / self.immunity <= i.sickness.gamma <= self.gamma + Globals.CloseGenetic / self.immunity:
                # We check if the individual is close enough to transmit the illness and if the genetic of the illness is close to the genetic
                # of the sane individual
                self.sickness = Illness.Illness()  # We give the sickness and its charateristic to the new infected
                self.sickness.alpha = i.sickness.alpha
                self.sickness.beta = i.sickness.beta
                self.sickness.gamma = i.sickness.gamma
                self.sickness.v = i.sickness.v
                self.sickness.d = i.sickness.d
                physics.list_illness.append(self.sickness)  # We add the illness to the list of illness
                physics.individuals_sane.remove(
                    self)  # We remove the individual from the sane list and put him in the infected list
                physics.individuals_infected.append(self)
                self.sick += Globals.Infection * self.sickness.v

    def evolution(self, physics):  # To make the illness evolve in the infected individuals
        if self.day_of_sickness <= self.sickness.d * Globals.DayOfSick and self.healing == False:
            # To check that the infected is sick from less that a certain duration and that he is not healing
            self.sick += (Globals.Infection * self.sickness.v) / self.immunity  # The individual is more and more sick
            self.day_of_sickness += 1
            if self.sick >= Globals.MaxInf:  # If the sickness exceeds a threshold, the individual dies
                physics.individuals_infected.remove(self)
                physics.total_death.append(self)
                physics.scene.removeItem(self)  # We remove the individual from the list and the scene
        else:  # If the individual survived a certain number of steps, he begins to heal
            self.healing = True
            self.sick += -(Globals.Heal * self.immunity) / self.sickness.v  # The individual is less and less sick
            if self.sick <= 0:  # If the sickness decrease enough, he is sane again
                self.sick = 0
                self.day_of_sickness = 0
                self.immunity *= Globals.ImmunityIncrease
                physics.individuals_infected.remove(self)  # He goes back to the sane list
                physics.individuals_sane.append(self)
                self.sickness = None  # He is no more sick or healing
                self.healing = False
                physics.heal.append(self)  # We add him to the healed list (for the graph)

    def reproduction(self, physics, a, b):  # To make babies
        self.love += Globals.Love  # The love increase every step
        # Here we have the decrease the immunity and the number of days of childhood
        # We put this here because the reproduction function is applied for every individuals
        self.immunity += -Globals.ImmunityLoss
        self.day_of_c += 1
        if self.day_of_c >= 500:  # After 365 steps, the new born is not in childhood anymore
            self.c = False
        p = Physics.t(self.pos())
        x, y = p
        if len(physics.individuals_infected + physics.individuals_sane) <= Globals.MaxPop and self.c == False and self.nb_of_c <= Globals.MaxChild:
        # We chech that we are under the maximum threshold of population and that the individual is an adult and have less than a certain number of childrens
            for i in a:
                pi = Physics.t(i.pos())
                xi, yi = pi
                if self != i and xi - physics.extent / Globals.ChildRadius <= x <= xi + physics.extent / Globals.ChildRadius and \
                        yi - physics.extent / Globals.ChildRadius <= y <= yi + physics.extent / Globals.ChildRadius and \
                        i.love + self.love > b * ((abs(i.alpha - self.alpha + i.beta - self.beta + i.gamma - self.gamma)) + 0.2):
                    # We check that the individual is close enough, and that the sum of their love is over a threshold
                    # The threshold take in account if the individual is sick and the genetic distance between the two individuals
                    physics.add_ind_child(xi, yi, random.uniform(0, 359), self, i)
                    self.love = 0
                    i.love = 0
                    self.nb_of_c += 1
