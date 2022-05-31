from PyQt5 import QtWidgets, QtCore
import Misc
import Physics
import Globals
import Interface
import random
import matplotlib.pyplot as plt
import os
import Graph

x = Globals.Seed
if x >= 0:
    random.seed(x)
app = QtWidgets.QApplication([])
physics = Physics.Physics()
view = Misc.AutoscaledGraphicsView(physics.scene)

timer = QtCore.QTimer()
w = Interface.MainWindow(view, timer, physics)


def on_timeout(): #To end automatically the simulation after a fixed number of steps
    if physics.i < Globals.Steps:
        physics.step()
    else:
        timer.stop()
        w.close()


timer.timeout.connect(on_timeout)

for i in range(Globals.IndCount): #To add the individuals on the scene
    if i < Globals.IndCount - 1:
        physics.add_ind_sane_rnd()
    else:
        physics.add_ind_infected_rnd()

if __name__ == '__main__':
    w.show()
    app.exec()

#In this part we create all the graphics of the simulation

list1 = Graph.list("testsane.txt")
list2 = Graph.list("testinfected.txt")
list3 = Graph.list("testbirth.txt")
list4 = Graph.list("testdeath.txt")
list5 = Graph.list("testimmunity.txt")
list6 = Graph.list("testvirulence.txt")
list7 = Graph.list("testduration.txt")
list8 = Graph.list("testpop.txt")
list9 = Graph.list("testheal.txt")

plt.figure(figsize=(20,15)) 
plt.subplot(311)
plt.plot(list1, c='g', label="sane")
plt.plot(list2, c='r', label="infected")
plt.plot(list8, c='m', label="total population")
plt.ylabel("Number of sane and infected", fontsize=8)
plt.title('Simulation Statistics', fontsize=20, fontweight='bold')
plt.legend()
plt.subplot(312)
plt.plot(list3, c='b', label="birth")
plt.plot(list4, c='k', label="death")
plt.plot(list9, c=(1, 0.5, 0), label="healed")

plt.ylabel("Total number of death and birth", fontsize=8)
plt.legend()
plt.subplot(313)
plt.plot(list5, c=(1, 0.9, 0), label="immunity")
plt.plot(list6, c=(0.5, 0, 1), label="virulence")
plt.plot(list7, c='c', label="duration")
plt.ylabel("Means of immunity, virulence and duration", fontsize=8)
plt.legend()
plt.show()

#To clean the graphics

os.remove("testsane.txt")
os.remove("testinfected.txt")
os.remove("testpop.txt")
os.remove("testbirth.txt")
os.remove("testdeath.txt")
os.remove("testimmunity.txt")
os.remove("testvirulence.txt")
os.remove("testduration.txt")
os.remove("testheal.txt")
