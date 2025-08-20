from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen

class ROISelector(QWidget):
    roiSelected = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.begin = None
        self.end = None
        self.roi = None

    def start_selection(self, target_rect):
        self.setGeometry(target_rect)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 0, 0, 120)))
        painter.drawRect(self.rect())

        if self.begin and self.end:
            self.roi = QRect(self.begin, self.end).normalized()
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.drawRect(self.roi)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(self.roi)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.roi:
            screen_roi = QRect(self.geometry().topLeft() + self.roi.topLeft(), self.roi.size())
            self.roiSelected.emit(screen_roi)
        self.hide()
        self.begin = None
        self.end = None
        self.roi = None