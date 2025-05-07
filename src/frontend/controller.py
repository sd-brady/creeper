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

        self.ui.button_lf_newfit.clicked.connect(self.view.add_localfit)
        self.view.signal_localfit_added.connect(self.model.add_localfit)
        self.model.signal_lf_fitlist_changed.connect(self.view.lf_fitlist_changed)

        self.ui.list_lf_testlist.currentRowChanged.connect(
            self.view.request_localfit_name_list
        )
        self.view.signal_request_localfit_list.connect(
            self.model.send_localfit_name_list
        )
        self.model.signal_send_localfit_name_list.connect(self.view.update_lf_fitlist)

        self.ui.list_lf_fitlist.currentRowChanged.connect(
            self.view.lf_fitlist_selection_changed
        )
        self.view.signal_request_localfit_mdmodel.connect(
            self.model.send_localfit_mdmodel
        )
        self.model.signal_send_mdtablemodel.connect(self.view.update_mdwidget_mdmodel)

        # Set up the signals to delete a local fit from a test.
        self.ui.button_lf_deletefit.clicked.connect(self.view.delete_lf_localfit)
        self.view.signal_delete_localfit.connect(self.model.delete_localfit)

        # Set up the signals to edit a the name of a local fit
        self.ui.button_lf_edit_fitname.clicked.connect(self.view.edit_lf_localfit_name)
        self.view.signal_edit_localfit_name.connect(self.model.edit_localfit_name)

        # Set up the signals to make a localfit primary
        self.ui.button_lf_make_fit_primary.clicked.connect(
            self.view.make_localfit_primary
        )
        self.view.signal_make_localfit_primary.connect(
            self.model.change_localfit_primary
        )

        # Set up the signals to save a localfit
        self.ui.button_lf_savefit.clicked.connect(self.view.save_localfit)
        self.view.signal_save_localfit.connect(self.model.save_localfit)

        # Set up the signals for gamma radio button
        self.ui.localfit_mdwidget.gamma_radio.toggled.connect(self.view.gamma_radio_toggled)
        return

    def messagebox_error(self, message):
        qtw.QMessageBox.critical(self, "Error", message)
        return
