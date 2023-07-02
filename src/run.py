import sys
from PyQt5 import QtWidgets as qtw

from frontend import controller

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = controller.MainWindow()
    sys.exit(app.exec_())
