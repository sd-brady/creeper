from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import pandas as pd
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)

from .modules import tables
from .modules import plotting
from .modules import data_classes
from .modules import unit_system


class View(qtw.QWidget):
    signal_errorbox = qtc.pyqtSignal(str)
    signal_test_added = qtc.pyqtSignal(data_classes.Test)
    signal_test_deleted = qtc.pyqtSignal(int)
    signal_request_test = qtc.pyqtSignal(data_classes.Test)
    signal_test_move_up = qtc.pyqtSignal(int)
    signal_test_move_down = qtc.pyqtSignal(int)

    # Signals for the Test Suite Tab. Arg1 is the test index to edit
    #   Arg2 is the test name, Arg3 is the stress, Arg4 is the color,
    #   Arg5 is the active status
    signal_edit_test = qtc.pyqtSignal(int, str, str, str, str)

    def __init__(self, ui):
        super().__init__()

        self._ui = ui
        self._ui.stacked_toplevel.setCurrentIndex(0)

        self.config_tables()
        self.config_plots()
        self.config_comboboxes()

        self.config_slots_and_signals()

        self.initialize_variables()

        return

    def initialize_variables(
        self,
    ):
        self.ts_current_test = data_classes.empty_test_class()
        return

    def config_slots_and_signals(
        self,
    ):
        # Connect the signal for selected row in the Test Suite testlist table
        return

    def config_comboboxes(self):
        self._ui.verticalLayout_9.setAlignment(self._ui.combo_ts_plotpicker, qtc.Qt.AlignRight)  # type: ignore
        return

    def config_plots(self):
        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_singleplot = plotting.SinglePlot_Strain_Canvas(self)
        toolbar1 = NavigationToolbar(self.canvas_ts_singleplot, self)
        self._ui.verticalLayout_13.addWidget(toolbar1)
        self._ui.verticalLayout_13.addWidget(self.canvas_ts_singleplot)
        self._ui.verticalLayout_13.setAlignment(toolbar1, qtc.Qt.AlignHCenter)  # type: ignore

        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_multiplot = plotting.MultiPlot_Strain_Canvas(self)
        toolbar2 = NavigationToolbar(self.canvas_ts_multiplot, self)
        self._ui.verticalLayout_14.addWidget(toolbar2)
        self._ui.verticalLayout_14.addWidget(self.canvas_ts_multiplot)
        self._ui.verticalLayout_14.setAlignment(toolbar2, qtc.Qt.AlignHCenter)  # type: ignore

        return

    def config_tables(self):
        # Configure the test data table
        self.config_testdata_table()
        self.config_testlist_table()
        return

    def config_testdata_table(self):
        # Set the table model
        self.testdata_model = tables.TestDataTableModel()
        self._ui.table_testdata.setModel(self.testdata_model)

        self._ui.table_testdata.horizontalHeader().setFixedHeight(40)
        self._ui.table_testdata.horizontalHeader().setDefaultAlignment(
            qtc.Qt.AlignCenter | qtc.Qt.Alignment(qtc.Qt.TextWordWrap)  # type: ignore
        )
        self._ui.table_testdata.verticalHeader().setFixedWidth(35)
        self._ui.table_testdata.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.Stretch
        )

        column_widths = [100, 100, 100, 100]
        for i in range(len(column_widths)):
            self._ui.table_testdata.horizontalHeader().resizeSection(
                i, column_widths[i]
            )

        return

    def ts_testlist_row_changed(self, selected, deselected):
        self.signal_test_requested(selected.row())
        return

    def get_test(self, test):
        if test.name == "":
            self.testdata_model.clear_data()
            self.canvas_ts_singleplot.setup_initial_figure()
        else:
            self.testdata_model.place_test(test)
            self.update_ts_single_plot(test)
        return

    def update_ts_single_plot(self, test: data_classes.Test):
        plotvar = self._ui.combo_ts_plotpicker.currentIndex()

        if plotvar == 0:
            self.canvas_ts_singleplot.update_plot_strain(test)
        elif plotvar == 1:
            self.canvas_ts_singleplot.update_plot_strainrate(test)
        elif plotvar == 2:
            self.canvas_ts_singleplot.update_plot_stress(test)
        elif plotvar == 3:
            self.canvas_ts_singleplot.update_plot_temp(test)

        return

    def config_testlist_table(self):
        # Set the table model
        self.testlist_model = tables.TestListTableModel()
        self._ui.table_testlist.setModel(self.testlist_model)

        self._ui.table_testlist.horizontalHeader().setFixedHeight(40)
        self._ui.table_testlist.horizontalHeader().setDefaultAlignment(
            qtc.Qt.AlignCenter | qtc.Qt.Alignment(qtc.Qt.TextWordWrap)  # type: ignore
        )
        self._ui.table_testlist.verticalHeader().setFixedWidth(35)
        self._ui.table_testlist.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.Stretch
        )

        column_widths = [100, 100, 100, 100]
        for i in range(len(column_widths)):
            self._ui.table_testlist.horizontalHeader().resizeSection(
                i, column_widths[i]
            )

        self.selmodel_testlist = self._ui.table_testlist.selectionModel()

        return

    def import_test_data(self):
        filename = self.select_file()

        # Make sure that the file is a CSV file
        if filename[-4::] != ".csv":
            self.signal_errorbox.emit("File must be a CSV file.")
        else:
            # Import the test data from the CSV file. Store the data in a dictionary
            # with the keys being the column headers from the table model.
            # testdata_dict = pd.read_csv(filename, ).to_dict(orient="list")
            imported_data = pd.read_csv(
                filename, header=0, names=self.testdata_model._headerkeys
            ).to_dict(orient="list")

            # Get the test name from the user
            dialog = tables.AddTestDialog()
            if dialog.exec():
                test_name = dialog.get_name()
                app_stress = dialog.get_stress()
                plot_color = dialog.get_color()
                active_state = dialog.get_active_state()
                test_unit_system = dialog.get_unit_system()

                test_data = data_classes.TestData(
                    time_list=imported_data["time"],
                    strain_list=imported_data["strain"],
                    stress_list=imported_data["stress"],
                    temperature_list=imported_data["temperature"],
                )

                # Initialize Local Fit Class for the Test
                local_fits = data_classes.LocalFits()
                test = data_classes.Test(
                    name=test_name,
                    stress=app_stress,
                    color=plot_color,
                    active_state=active_state,
                    test_data=test_data,
                    local_fits=local_fits,
                    unit_system=test_unit_system,
                )
                # self.signal_test_added.emit(test)

        return

    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            None,
            "Select CSV File to Open...",
            r"/home/brady/projects/creeper/examples/Markham 10a",
            "CSV Files (*.csv) ;; All Files (*)",
        )

        return filename

    def test_added(self, test: data_classes.Test):
        # Add Test to the test list table
        self.testlist_model.add_test(test)
        return

    def test_suite_changed(self, test_suite: data_classes.TestSuite):
        # Update the test list table
        self.testlist_model.place_test_suite(test_suite)
        self.selmodel_testlist.clearSelection()

        # Clear the single plot on the Test Suite tab
        self.canvas_ts_singleplot.setup_initial_figure()

        # Need to update the global plot on the Test Suite tab
        self.update_ts_multi_plot(test_suite)

        return

    def update_ts_multi_plot(self, test_suite):
        self.canvas_ts_multiplot.update_plot(test_suite)
        return

    def delete_test(self):
        test_index = self.selmodel_testlist.currentIndex().row()
        print("test index: ", test_index)
        self.signal_test_deleted.emit(test_index)
        return

    def ts_move_up(self):
        test_index = self.selmodel_testlist.currentIndex().row()
        num_tests = self.testlist_model.num_rows

        print("test index: ", test_index)
        print("num_tests: ", num_tests)

        if num_tests <= 1:
            pass
        elif test_index <= 0:
            pass
        else:
            self.signal_test_move_up.emit(test_index)

            # Need to update move the selected cell with the test
            self.selmodel_testlist.setCurrentIndex(
                self.testlist_model.index(test_index - 1, 0),
                qtc.QItemSelectionModel.SelectCurrent,
            )
        return

    def ts_move_down(self):
        test_index = self.selmodel_testlist.currentIndex().row()
        num_tests = self.testlist_model.num_rows

        print("test index: ", test_index)
        print("num_tests: ", num_tests)

        if num_tests <= 1:
            pass
        elif test_index < 0:
            pass
        elif test_index + 1 == num_tests:
            pass
        else:
            self.signal_test_move_down.emit(test_index)

            # Need to update move the selected cell with the test
            self.selmodel_testlist.setCurrentIndex(
                self.testlist_model.index(test_index + 1, 0),
                qtc.QItemSelectionModel.SelectCurrent,
            )
            return

    # # Signals for the Test Suite Tab. Arg1 is the test index to edit
    # #   Arg2 is the test name, Arg3 is the stress, Arg4 is the color,
    # #   Arg5 is the active status
    # signal_edit_test = qtc.pyqtSignal(int, str, str, str, str)
    def edit_test(self):
        test_index = self.selmodel_testlist.currentIndex().row()

        if test_index == -1:
            pass
        else:
            cur_test_info = self.testlist_model.get_test_info(test_index)

            unit_time, unit_stress, unit_temperature = self.get_units()

            dialog = tables.AddTestDialog()
            if dialog.exec():
                new_inputs = dialog.getInputs()

            self.signal_edit_test.emit(
                test_index, new_inputs[0], new_inputs[1], new_inputs[2], new_inputs[3]
            )
        return

    def get_units(self):
        unit_time = self._ui.combo_unit_time.currentText()
        unit_stress = self._ui.combo_unit_stress.currentText()
        unit_temperature = self._ui.combo_unit_temperature.currentText()
        print(unit_time, unit_stress, unit_temperature)
        return (unit_time, unit_stress, unit_temperature)
