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
        self.ui.button_delta.clicked.connect(self.model.fun_debug)

        self.ui.button_importtest.clicked.connect(self.view.import_test_data)
        self.view.signal_test_added.connect(self.model.add_test)
        self.model.signal_send_test.connect(self.view.get_test)
        self.ui.combo_unit_time.currentTextChanged.connect(
            self.model.send_current_testsuite
        )
        self.ui.combo_unit_temperature.currentTextChanged.connect(
            self.model.send_current_testsuite
        )
        self.ui.combo_unit_stress.currentIndexChanged.connect(
            self.model.send_current_testsuite
        )
        self.ui.combo_ts_plot_type.currentIndexChanged.connect(
            self.model.send_current_testsuite
        )

        # self.model.signal_send_testsuite.connect(self.view.ts_plot_type_changed)
        self.model.signal_send_testsuite.connect(self.view.gui_units_changed)

        # These are good
        self.model.signal_error.connect(self.messagebox_error)
        self.model.test_suite_changed.connect(self.view.test_suite_changed)
        self.ui.button_edit_test.clicked.connect(self.view.edit_test)
        self.view.selmodel_testlist.selectionChanged.connect(self.model.send_test)
        self.view.signal_edit_test.connect(self.model.edit_test)
        self.view.signal_test_deleted.connect(self.model.delete_test)
        self.ui.button_delete_test.clicked.connect(self.view.delete_test)
        self.ui.button_ts_moveup.clicked.connect(self.view.ts_move_up)
        self.view.signal_test_move_up.connect(self.model.move_test_up)
        self.view.signal_test_move_down.connect(self.model.move_test_down)
        self.ui.button_ts_movedown.clicked.connect(self.view.ts_move_down)

        self.ui.button_lf_softsalt.clicked.connect(self.view.localfit_place_softsalt)
        self.ui.button_lf_hardsalt.clicked.connect(self.view.localfit_place_hardsalt)
        self.ui.button_lf_cleartable.clicked.connect(
            self.ui.localfit_mdwidget.clear_table
        )
        return

    def messagebox_error(self, message):
        qtw.QMessageBox.critical(self, "Error", message)
        return
