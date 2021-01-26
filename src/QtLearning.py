def hello_world():
    import sys
    from PySide6.QtWidgets import QApplication, QLabel

    app = QApplication(sys.argv)
    label = QLabel("Hello, World!")
    label.show()
    app.exec_()

if __name__ == '__main__':
    hello_world()