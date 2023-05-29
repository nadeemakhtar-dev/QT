import sys
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        progress_bar = RoundProgressBar(widget)
        progress_bar.setGeometry(400, 10, 100, 100)

        seek_bar = QSlider(Qt.Orientation.Horizontal, widget)
        seek_bar.setGeometry(400, 120, 100, 20)
        seek_bar.setMinimum(0)
        seek_bar.setMaximum(100)
        seek_bar.valueChanged.connect(progress_bar.set_value)

        self.setWindowTitle("Black Window")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.show()


class RoundProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(100, 100)

        self.value = 0

    def set_value(self, value):
        self.value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        outer_radius = int(min(width, height) / 2 - 10)
        inner_radius = outer_radius

        center_x = int(width / 2)
        center_y = int(height / 2)

        # Draw background circle
        background_pen = QPen(Qt.GlobalColor.white)
        background_pen.setWidth(10)
        painter.setPen(background_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center_x - outer_radius, center_y - outer_radius,
                            outer_radius * 2, outer_radius * 2)

        # Draw progress arc
        progress_pen = QPen(QColor(0, 255, 0))
        progress_pen.setWidth(10)
        painter.setPen(progress_pen)
        start_angle = 90 * 16  # Start angle is in 1/16th of a degree
        span_angle = -self.value * (360 * 16) / 100  # Convert value to angle

        # Create a QRectF object to specify the position and size of the pie
        rect = QRectF(center_x - inner_radius, center_y - inner_radius,
                      inner_radius * 2, inner_radius * 2)

        painter.drawArc(rect, int(start_angle), int(span_angle))

        # Draw progress text
        font = QFont()
        font.setPixelSize(14)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.value}%")

    def sizeHint(self):
        return self.minimumSizeHint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
