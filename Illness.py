import PyQt5.QtWidgets as QtWidgets
import random
import Globals


class Illness(QtWidgets.QGraphicsItem):

    def __init__(self):
        super().__init__()
        self.alpha = random.uniform(0, 1)
        self.beta = random.uniform(0, 1)
        self.gamma = random.uniform(0, 1)
        self.d = Globals.Duration
        self.v = Globals.Virulence
    # Here we have the mutation function of every genetic component, of course it is more optimal
    # to do only one function, and to put the genetic component in factor, or to do a list with
    # every component, but, we don't know why, it doesn't work, so we did 5 functions.
    def mutationalpha(self):
        x = random.uniform(0, 1)
        if x <= 0.1: # Every component have 10% chance to mute every step
            z = random.uniform(-Globals.Mutation, Globals.Mutation) # The component will mute a random quantity
            if 0 <= self.alpha + z <= 1: # Here we choose the thresholds for the component
                self.alpha += z

    def mutationbeta(self):
        x = random.uniform(0, 1)
        if x <= 0.1:
            z = random.uniform(-Globals.Mutation, Globals.Mutation)
            if 0 <= self.beta + z <= 1:
                self.beta += z

    def mutationgamma(self):
        x = random.uniform(0, 1)
        if x <= 0.1:
            z = random.uniform(-Globals.Mutation, Globals.Mutation)
            if 0 <= self.gamma + z <= 1:
                self.gamma += z

    def mutationd(self):
        x = random.uniform(0, 1)
        if x <= 0.1:
            z = random.uniform(-Globals.Mutation, Globals.Mutation)
            if 0.1 <= self.d + z <= 10:
                self.d += z

    def mutationv(self):
        x = random.uniform(0, 1)
        if x <= 0.1:
            z = random.uniform(-Globals.Mutation, Globals.Mutation)
            if 0.1 <= self.v + z <= 10:
                self.v += z