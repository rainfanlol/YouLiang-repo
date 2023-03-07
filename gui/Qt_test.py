import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 創建標籤
        self.label = QLabel('Hello, PySide2!', self)
        self.label.move(50, 50)

        # 創建按鈕
        self.button = QPushButton('Click me!', self)
        self.button.move(50, 80)
        self.button.clicked.connect(self.buttonClicked)

        # 創建佈局
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button)
        self.setLayout(vbox)

        # 設置窗口屬性
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('MyApp')
        self.show()

    def buttonClicked(self):
        # 按下按鈕時更新標籤文本
        self.label.setText('Button clicked')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())