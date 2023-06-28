from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from . import view
from . import model
from .modules import ui_main


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up Designer UI Class
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)

        # Main UI Code goes in the View Class
        self.view = view.View(self.ui)
        
        # Set up Model
        self.model = model.Model()

        # Set up menubar buttons
        self.ui.actionExit.triggered.connect(self.close)  # type: ignore

        # Connect Signals and Slots
        self.connect_signals_and_slots()

        # End main UI code
        self.show()

        return

    def connect_signals_and_slots(self):
        # Connect error message box signal
        self.model.signal_error.connect(self.messagebox_error)

        # Connect test added signals
        self.view.signal_test_added.connect(self.model.add_test)
        self.model.signal_test_validated.connect(self.view.test_added)

        # Connect test added signal
        self.view.signal_test_deleted.connect(self.model.delete_test)

        return

    def messagebox_error(self, message):
        qtw.QMessageBox.critical(self, "Error", message)
        return
