from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget
from PyQt5 import QtWidgets
import PyQt5.QtGui as QtGui
import Globals


def build_buttons_panel(timer, physics):  # Function to create buttons

    controls = QtWidgets.QHBoxLayout()
    controls.addStretch(1)

    v_holder = QWidget()
    v_holder.setLayout(controls)

    b_pause = QtWidgets.QToolButton()
    b_pause.setShortcut("Space")
    b_pause.setIcon(QtGui.QIcon('play.png'))
    controls.addWidget(b_pause)

    b_step = QtWidgets.QToolButton()
    b_step.setShortcut("N")
    b_step.setIcon(QtGui.QIcon('skip.png'))
    controls.addWidget(b_step)

    controls.addStretch(1)

    def maybe_run(): # To permit the play/pause button to work
        if timer.isActive():
            timer.stop()
            b_pause.setIcon(QtGui.QIcon('play.png'))
        else:
            timer.start(1000 // Globals.Speed)
            b_pause.setIcon(QtGui.QIcon('pause.png'))

    b_pause.clicked.connect(maybe_run)
    b_step.clicked.connect(physics.step)

    return v_holder



def build_control_panel(timer, physics):
    holder = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.addLayout(build_buttons_panel(timer, physics))
    holder.setLayout(layout)
    return holder





class MainWindow(QMainWindow):

    def __init__(self, view, timer, physics):
        super().__init__()
        self.setWindowTitle("Simulation")

        self.splitter = QSplitter()

        self.splitter.addWidget(view)

        self.splitter.addWidget(build_buttons_panel(timer, physics))

        self.setCentralWidget(self.splitter)






