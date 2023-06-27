from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from . import model
from . import view
from .modules import ui_main


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up Designer UI Class
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)

        # Main UI Code goes in the View Class
        self.view = view.View(self.ui)

        # Set Up Model Class
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
        self.view.signal_errorbox.connect(self.messagebox_error)

        self.ui.list_ts_testlist.currentRowChanged.connect(self.view.testlist_changed)

        self.ui.combo_ts_plotpicker.currentIndexChanged.connect(
            self.view.ts_plotpicker_changed
        )

        self.ui.button_importtest.clicked.connect(self.view.import_test_data)
        self.ui.button_delete_test.clicked.connect(self.view.delete_test)

        return

    def messagebox_error(self, message):
        qtw.QMessageBox.critical(self, "Error", message)
        return
