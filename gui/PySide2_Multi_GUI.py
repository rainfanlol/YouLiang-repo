import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Multi-Functional GUI")
        self.setGeometry(100, 100, 400, 400)

        # Create widgets
        self.label = QLabel("Enter your name:")
        self.name_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.reset_button = QPushButton("Reset")
        self.result_label = QLabel()
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        self.spin_box = QSpinBox()

        # Create layouts
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # Add widgets to layouts
        hbox1.addWidget(self.label)
        hbox1.addWidget(self.name_entry)
        hbox1.addWidget(self.submit_button)
        hbox1.addWidget(self.reset_button)
        hbox2.addWidget(self.result_label)
        hbox2.addWidget(self.combo_box)
        hbox2.addWidget(self.spin_box)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        # Set the main layout
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        # Connect buttons to functions
        self.submit_button.clicked.connect(self.submit)
        self.reset_button.clicked.connect(self.reset)

    def submit(self):
        name = self.name_entry.text()
        option = self.combo_box.currentText()
        number = self.spin_box.value()
        self.result_label.setText(f"Hello {name}! You selected {option} and your number is {number}.")

    def reset(self):
        self.name_entry.setText("")
        self.combo_box.setCurrentIndex(0)
        self.spin_box.setValue(0)
        self.result_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
