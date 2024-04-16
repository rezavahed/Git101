import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from GUI import Ui_MainWindow
import serial

SER_TIMEOUT_DUR = 1


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_button.clicked.connect(self.on_connect_button_clicked)

    def on_connect_button_clicked(self):
        selected_baudrate = int(self.Baudrate_combo.currentText())
        selected_com = self.com_combo.currentText()
        selected_command = self.command_combo.currentText()

        self.read_serial(selected_com, selected_baudrate)

    def read_serial(self, selected_com, selected_baudrate):
        print("hello")
        try:
            ser = serial.Serial(selected_com, selected_baudrate,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=SER_TIMEOUT_DUR)

            # Read bytes from the serial port
            #data = ser.read(6)  # Read 6 bytes of data
            #print(f"Read {len(data)} bytes from serial port: {data}")
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
