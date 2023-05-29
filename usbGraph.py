import sys
import serial
import serial.tools.list_ports
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLineEdit


class DataReader(QThread):
    data_received = pyqtSignal(float)

    def __init__(self, port_name, baud_rate):
        super().__init__()
        self.port_name = port_name
        self.baud_rate = baud_rate

    def run(self):
        try:
            with serial.Serial(self.port_name, self.baud_rate) as ser:
                while True:
                    data = float(ser.readline().decode().strip())
                    self.data_received.emit(data)
        except serial.SerialException as e:
            print(f"Failed to open serial port: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Devices")
        self.list_widget = QListWidget(self)
        self.text_edit = QTextEdit(self)
        self.write_text_field = QLineEdit(self)
        self.write_button = QPushButton("Write", self)
        self.write_button.clicked.connect(self.write_data)
        
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.write_text_field)
        layout.addWidget(self.write_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.refresh_devices()
        self.data_reader = None
        self.serial_port = None

    def refresh_devices(self):
        self.list_widget.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            item = QListWidgetItem(port.device)
            self.list_widget.addItem(item)

    def start_data_reader(self, port_name, baud_rate):
        if self.data_reader and self.data_reader.isRunning():
            return
        self.data_reader = DataReader(port_name, baud_rate)
        self.data_reader.data_received.connect(self.handle_data_received)
        self.data_reader.start()

        # Open serial port for writing
        self.serial_port = serial.Serial(port_name, baud_rate)

    def handle_data_received(self, data):
        self.text_edit.append(str(data))

    def write_data(self):
        data = self.write_text_field.text()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data.encode())
            print("Success")


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Graph")
        self.graph_widget = pg.PlotWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

        self.x_data = []
        self.y_data = []
        self.curve = self.graph_widget.plot(self.x_data, self.y_data)

    def update_graph(self, data):
        self.y_data.append(data)
        self.x_data.append(len(self.x_data) + 1)
        self.curve.setData(self.x_data, self.y_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    graph_window = GraphWindow()
    main_window.show()
    graph_window.show()

    main_window.start_data_reader("/dev/cu.usbmodem11301", 9600)
    main_window.data_reader.data_received.connect(graph_window.update_graph)

    sys.exit(app.exec())
