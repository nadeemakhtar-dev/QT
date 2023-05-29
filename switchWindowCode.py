import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar


class SplashScreen(QWidget):
    def __init__(self, next_screen):
        super().__init__()

        self.setWindowTitle("Splash Screen")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()
        label = QLabel("Splash Screen", self)
        layout.addWidget(label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Set indeterminate range
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedSize(100, 20)  # Set width and height
        self.progress_bar.setStyleSheet("QProgressBar { background-color: lightgray; border: none; } "
                                         "QProgressBar::chunk { background-color: pink; }")
        layout.addWidget(self.progress_bar)

        button = QPushButton("Next", self)
        button.clicked.connect(next_screen)
        layout.addWidget(button)

        self.setLayout(layout)

        # Start the timer to delay the animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_progress_animation)
        self.timer.start(1000)  # 1000 milliseconds delay before starting the animation

    def start_progress_animation(self):
        self.timer.stop()
        self.progress_bar.setRange(0, 0)  # Set indeterminate range


class StandbyScreen(QWidget):
    def __init__(self, previous_screen, next_screen):
        super().__init__()

        self.setWindowTitle("Main Screen")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()
        label = QLabel("Standby Screen", self)
        layout.addWidget(label)

        button_back = QPushButton("Back", self)
        button_back.clicked.connect(previous_screen)
        layout.addWidget(button_back)

        button_next = QPushButton("Next", self)
        button_next.clicked.connect(next_screen)
        layout.addWidget(button_next)

        self.setLayout(layout)


class DashboardScreen(QWidget):
    def __init__(self, previous_screen):
        super().__init__()

        self.setWindowTitle("Dashboard Screen")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: red; color: white;")

        layout = QVBoxLayout()
        label = QLabel("Final Screen", self)
        layout.addWidget(label)

        button_back = QPushButton("Back", self)
        button_back.clicked.connect(previous_screen)
        layout.addWidget(button_back)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window Example")
        self.setGeometry(0, 0, 800, 600)
        self.center_window()

        self.splash_screen = None
        self.standby_screen = None
        self.dashboard_screen = None
        self.current_screen = None

        self.show_splash_screen()

    def center_window(self):
        available_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(available_geometry.center())
        self.move(window_geometry.topLeft())

    def show_splash_screen(self):
        if self.current_screen:
            self.current_screen.hide()
            self.current_screen.deleteLater()

        self.splash_screen = SplashScreen(self.show_standby_screen)
        self.setCentralWidget(self.splash_screen)
        self.current_screen = self.splash_screen

    def show_standby_screen(self):
        if self.current_screen:
            self.current_screen.hide()
            self.current_screen.deleteLater()

        self.standby_screen = StandbyScreen(self.show_splash_screen, self.show_dashboard_screen)
        self.setCentralWidget(self.standby_screen)
        self.current_screen = self.standby_screen

    def show_dashboard_screen(self):
        if self.current_screen:
            self.current_screen.hide()
            self.current_screen.deleteLater()

        self.dashboard_screen = DashboardScreen(self.show_standby_screen)
        self.setCentralWidget(self.dashboard_screen)
        self.current_screen = self.dashboard_screen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
