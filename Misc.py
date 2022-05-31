import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt


class AutoscaledGraphicsView(QtWidgets.QGraphicsView): # to adjust window size
    def __init__(self, *args, **kwargs) -> object:
        super().__init__(*args, **kwargs)
        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)