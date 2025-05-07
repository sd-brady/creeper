from pprint import pprint
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import pandas as pd
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)

from .modules import tables
from .modules import plotting
from .modules import data_classes
from .modules import unit_system
from .modules import mdmodel


class View(qtw.QWidget):
    signal_errorbox = qtc.pyqtSignal(str)
    signal_test_added = qtc.pyqtSignal(data_classes.Test, unit_system.UnitSystem)
    signal_test_deleted = qtc.pyqtSignal(int)
    signal_request_test = qtc.pyqtSignal(data_classes.Test)
    signal_test_move_up = qtc.pyqtSignal(int)
    signal_test_move_down = qtc.pyqtSignal(int)
    signal_gui_units_changed = qtc.pyqtSignal()
    signal_localfit_added = qtc.pyqtSignal(int, data_classes.LocalFit)
    signal_request_localfit = qtc.pyqtSignal(int, int)
    signal_request_localfit_list = qtc.pyqtSignal(int, int)
    signal_request_localfit_mdmodel = qtc.pyqtSignal(int, int)
    signal_delete_localfit = qtc.pyqtSignal(int, int)
    signal_edit_localfit_name = qtc.pyqtSignal(int, int, str)
    signal_make_localfit_primary = qtc.pyqtSignal(int, int)
    signal_save_localfit = qtc.pyqtSignal(int, int, mdmodel.MdTableModel)
    signal_edit_test = qtc.pyqtSignal(
        int, str, str, data_classes.PlotColors, data_classes.ActiveState
    )

    def __init__(self, ui):
        super().__init__()

        self._ui = ui
        self._ui.stacked_toplevel.setCurrentIndex(0)

        self.config_buttons()

        self.config_tables()
        self.config_listwidgets()
        self.config_plots()
        self.config_comboboxes()

        self.config_slots_and_signals()

        # self._ui.localfit_mdwidget.a1_value.setText("test!")

        return

    def config_listwidgets(self):
        return

    def config_buttons(self):
        # Test Suite Button
        self._ui.button_testsuite.clicked.connect(self.config_testsuite_button)

        # Local Fits Button
        self._ui.button_localfits.clicked.connect(self.config_localfits_button)

        return

    def config_testsuite_button(self):
        self._ui.stacked_toplevel.setCurrentWidget(self._ui.tab_testsuite)
        return

    def config_localfits_button(self):
        self._ui.stacked_toplevel.setCurrentWidget(self._ui.tab_localfits)
        return

    def config_slots_and_signals(
        self,
    ):
        # Connect the signal for selected row in the Test Suite testlist table
        return

    def config_comboboxes(self):
        self._ui.verticalLayout_9.setAlignment(self._ui.combo_ts_plot_type, qtc.Qt.AlignRight)  # type: ignore
        return

    def config_plots(self):
        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_singleplot = plotting.SinglePlot_Strain_Canvas(
            usys=self.get_gui_unit_system(), plot_type=self.get_ts_plot_type()
        )
        toolbar1 = NavigationToolbar(self.canvas_ts_singleplot, self)
        self._ui.verticalLayout_13.addWidget(toolbar1)
        self._ui.verticalLayout_13.addWidget(self.canvas_ts_singleplot)
        self._ui.verticalLayout_13.setAlignment(toolbar1, qtc.Qt.AlignHCenter)  # type: ignore

        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_multiplot = plotting.MultiPlot_Strain_Canvas(
            usys=self.get_gui_unit_system(),
            plot_type=self.get_ts_plot_type(),
        )
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
            self.canvas_ts_singleplot.setup_initial_figure(
                usys=self.get_gui_unit_system(), plot_type=self.get_ts_plot_type()
            )
        else:
            # Get gui unit system
            gui_usys = self.get_gui_unit_system()

            # Convert the test to the gui unit system
            test = unit_system.convert_test_from_base(test, gui_usys)
            self.testdata_model.place_test(test)

            # Update the single plot
            self.canvas_ts_singleplot.update_plot(
                test=test, usys=gui_usys, plot_type=self.get_ts_plot_type()
            )

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
                print("Dialog result: ", dialog.result())
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
                test = data_classes.Test(
                    name=test_name,
                    stress=app_stress,
                    color=plot_color,
                    active_state=active_state,
                    test_data=test_data,
                )
                self.signal_test_added.emit(test, test_unit_system)

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
        self.testlist_model.add_test(test)
        return

    def test_suite_changed(self, testsuite: data_classes.TestSuite):
        gui_usys = self.get_gui_unit_system()

        # Convert the test suite to gui unit system
        testsuite = unit_system.convert_testsuite_from_base(testsuite, gui_usys)

        # Update the test list table
        self.testlist_model.place_test_suite(testsuite)
        self.selmodel_testlist.clearCurrentIndex()
        self.selmodel_testlist.clearSelection()

        # Clear the test data table
        self.testdata_model.clear_data()

        # Clear the single plot on the Test Suite tab
        self.canvas_ts_singleplot.setup_initial_figure(
            self.get_gui_unit_system(), self.get_ts_plot_type()
        )

        # Need to update the global plot on the Test Suite tab
        self.update_ts_multi_plot(testsuite)

        # Need to update the test list widget on the local fits tab
        self._ui.list_lf_testlist.clear()
        for item_text in testsuite.get_test_names():
            item = qtw.QListWidgetItem(item_text)
            item.setTextAlignment(qtc.Qt.AlignHCenter)
            self._ui.list_lf_testlist.addItem(item)

        return

    def lf_fitlist_changed(self, primary_index: int, name_list: list[str]):
        # Clear the MdWidget
        self._ui.localfit_mdwidget.clear_table()

        # Add the name_list to the fit list QListWidget
        self._ui.list_lf_fitlist.clear()
        for i, item_text in enumerate(name_list):
            font = qtg.QFont()
            if i == primary_index:
                font.setBold(True)
            else:
                font.setBold(False)

            item = qtw.QListWidgetItem(item_text)
            item.setFont(font)
            item.setTextAlignment(qtc.Qt.AlignHCenter)
            self._ui.list_lf_fitlist.addItem(item)

        return

    def update_ts_multi_plot(self, test_suite):
        self.canvas_ts_multiplot.update_plot(
            test_suite=test_suite,
            usys=self.get_gui_unit_system(),
            plot_type=self.get_ts_plot_type(),
        )
        return

    def delete_test(self):
        if self.selmodel_testlist.currentIndex().row() == -1:
            pass
        else:
            test_index = self.selmodel_testlist.currentIndex().row()
            self.signal_test_deleted.emit(test_index)
        return

    def ts_move_up(self):
        test_index = self.selmodel_testlist.currentIndex().row()
        num_tests = self.testlist_model.num_rows

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

    def edit_test(self):
        test_index = self.selmodel_testlist.currentIndex().row()

        if test_index == -1:
            pass
        else:
            cur_name = self.testlist_model.get_test_name(test_index)
            cur_stress = str(self.testlist_model.get_test_stress(test_index))
            cur_color = self.testlist_model.get_test_color(test_index)
            cur_active = self.testlist_model.get_test_active(test_index)

            dialog = tables.EditTestDialog(cur_name, cur_stress, cur_color, cur_active)
            if dialog.exec():
                print("Dialog result: ", dialog.result())
                new_name = dialog.get_name()
                new_stress = dialog.get_stress()
                new_color = dialog.get_color()
                new_active = dialog.get_active_state()

                self.signal_edit_test.emit(
                    test_index, new_name, new_stress, new_color, new_active
                )
        return

    def get_gui_unit_system(self):
        unit_time = unit_system.UnitTime(self._ui.combo_unit_time.currentText())
        unit_stress = unit_system.UnitStress(self._ui.combo_unit_stress.currentText())
        unit_temperature = unit_system.UnitTemp(
            self._ui.combo_unit_temperature.currentText()
        )
        usys = unit_system.UnitSystem(unit_time, unit_temperature, unit_stress)
        return usys

    def get_ts_plot_type(self):
        plot_type = data_classes.PlotType(self._ui.combo_ts_plot_type.currentText())
        return plot_type

    def gui_units_changed(self, test_suite: data_classes.TestSuite):
        # Get the gui unit system
        gui_usys = self.get_gui_unit_system()

        if len(test_suite.test_list) == 0:
            pass
        else:
            # Convert the test suite to gui unit system
            test_suite = unit_system.convert_testsuite_from_base(test_suite, gui_usys)

            # Change the current test list table index to -1.
            #   Change the units of the stress and temperature columns
            self._ui.table_testlist.selectionModel().clearCurrentIndex()
            self._ui.table_testlist.selectionModel().clearSelection()
            self.testlist_model.place_test_suite(test_suite)

            # Clear the test data table
            self.testdata_model.clear_data()

        # Make sure the single plot gets re-initialized (i.e., "no test selected")
        #   Update the axis labels acording to the new units
        self.canvas_ts_singleplot.setup_initial_figure(
            usys=gui_usys,
            plot_type=self.get_ts_plot_type(),
        )

        # Update the multi plot canvas
        self.canvas_ts_multiplot.update_plot(
            test_suite=test_suite,
            usys=gui_usys,
            plot_type=self.get_ts_plot_type(),
        )

        # Update Widget Unit Labels
        #   Update the Test List Table Units based on Gui Units
        self.testlist_model.update_stress_header(gui_usys.stress)

        #   Update the Test Data List Units based on Gui Units
        # self.
        self.testdata_model.update_time_header(gui_usys.time)
        self.testdata_model.update_temp_header(gui_usys.temperature)
        self.testdata_model.update_stress_header(gui_usys.stress)

        # Convert the units in the local fit md_widget
        self._ui.localfit_mdwidget.convert_usys(gui_usys)

        return

    def localfit_place_softsalt(self):
        softsalt_model = mdmodel.MdModel()
        softsalt_model.set_soft_salt(self.get_gui_unit_system())
        self._ui.localfit_mdwidget.place_mdmodel_val(softsalt_model)
        return

    def localfit_place_hardsalt(self):
        hardsalt_model = mdmodel.MdModel()
        hardsalt_model.set_hard_salt(self.get_gui_unit_system())
        self._ui.localfit_mdwidget.place_mdmodel_val(hardsalt_model)
        return

    def add_localfit(self):
        # get the index of the selected test
        row = self._ui.list_lf_testlist.currentRow()
        print("Current Row: ", row)
        if row == -1:
            print("No test selected.")
            pass
        elif self._ui.localfit_mdwidget.validate():
            gui_usys = self.get_gui_unit_system()
            mdtablemodel = self._ui.localfit_mdwidget.get_table_mdmodel(gui_usys)
            mdtablemodel.convert_usys_to_base()

            dialog = tables.LocalFitNameDialog(name="")
            if dialog.exec():
                fit_name = dialog.get_name()
            else:
                fit_name = ""

            localfit = data_classes.LocalFit(mdtablemodel=mdtablemodel, name=fit_name)
            self.signal_localfit_added.emit(row, localfit)
        else:
            print("Invalid User Input.")
            pass

        return

    def lf_fitlist_selection_changed(self, fit_index: int):
        # Get the selected test from the testlist QListWidget
        test_index = self._ui.list_lf_testlist.currentRow()

        # Request the mdmodel from the localfit class in the model
        self.signal_request_localfit_mdmodel.emit(test_index, fit_index)
        return

    def request_localfit_name_list(self, test_index: int):
        self.signal_request_localfit_list.emit(test_index, -1)
        return

    def update_lf_fitlist(self, primary_index, name_list: list):
        self._ui.list_lf_fitlist.clear()
        for i, name in enumerate(name_list):
            font = qtg.QFont()
            if i == primary_index:
                font.setBold(True)
            else:
                font.setBold(False)

            item = qtw.QListWidgetItem(name)
            item.setFont(font)
            item.setTextAlignment(qtc.Qt.AlignHCenter)
            self._ui.list_lf_fitlist.addItem(item)

        self._ui.list_lf_fitlist.setCurrentRow(-1)
        return

    def update_mdwidget_mdmodel(self, mdtablemodel: mdmodel.MdTableModel):
        # Get the gui unitsystem
        gui_usys = self.get_gui_unit_system()

        # Convert the mdmodel to gui units
        mdtablemodel.val_model.convert_usys(gui_usys)
        mdtablemodel.min_model.convert_usys(gui_usys)
        mdtablemodel.max_model.convert_usys(gui_usys)

        # Place the mdmodel in the mdwidget
        self._ui.localfit_mdwidget.place_mdtablemodel(mdtablemodel)

        return

    def delete_lf_localfit(self):
        # Get the selected test in the localfit testlist QListWidget
        test_index = self._ui.list_lf_testlist.currentRow()

        # Get the selected row in the localfit fitlist QListWidget
        fit_index = self._ui.list_lf_fitlist.currentRow()

        if test_index == -1 or fit_index == -1:
            pass
        else:
            self.signal_delete_localfit.emit(test_index, fit_index)

        return

    def edit_lf_localfit_name(self):
        # Get the selected test on the list_lf_testlist widget
        test_index = self._ui.list_lf_testlist.currentRow()
        # Get the selected fit on the list_lf_fitlist widget
        fit_index = self._ui.list_lf_fitlist.currentRow()

        if test_index == -1 or fit_index == -1:
            pass
        else:
            current_name = self._ui.list_lf_fitlist.currentItem().text()
            if current_name[:1] == "* " and current_name[-2:] == " *":
                current_name = "* " + current_name + " *"

            dialog = tables.LocalFitNameDialog(name=current_name)
            if dialog.exec():
                new_name = dialog.get_name()
            else:
                new_name = ""
            self.signal_edit_localfit_name.emit(test_index, fit_index, new_name)

        return

    def make_localfit_primary(self):
        # Get the selected test on the list_lf_testlist widget
        test_index = self._ui.list_lf_testlist.currentRow()
        # Get the selected fit on the list_lf_fitlist widget
        fit_index = self._ui.list_lf_fitlist.currentRow()

        if test_index == -1 or fit_index == -1:
            pass
        else:
            self.signal_make_localfit_primary.emit(test_index, fit_index)

        return

    def save_localfit(self):
        # Get the selected test on the list_lf_testlist widget
        test_index = self._ui.list_lf_testlist.currentRow()
        # Get the selected fit on the list_lf_fitlist widget
        fit_index = self._ui.list_lf_fitlist.currentRow()

        if test_index == -1 or fit_index == -1:
            pass
        elif self._ui.localfit_mdwidget.validate:
            # Get the gui usys
            gui_usys = self.get_gui_unit_system()

            # Get an mdmodel from the mdwidget
            md_model = self._ui.localfit_mdwidget.get_table_mdmodel(usys=gui_usys)

            # Convert the mdmodel to base units
            md_model.convert_usys_to_base()

            # Send the md_model to the model
            self.signal_save_localfit.emit(test_index, fit_index, md_model)
        else:
            print("Invalid User Input.")

    def gamma_radio_toggled(self):
        # Get the current state of the gamma radio button
        widget_list = [
            self._ui.localfit_mdwidget.a1_flag,
            self._ui.localfit_mdwidget.a2_flag,
            self._ui.localfit_mdwidget.b1_flag,
            self._ui.localfit_mdwidget.b2_flag
        ]

        if self._ui.localfit_mdwidget.gamma_radio.isChecked():
            dialog = tables.gammaRadioDialog()
            if dialog.exec():
                for i in range(len(widget_list)):
                    darker_color = "#333333"
                    # Uncheck widget list
                    # Deactivate the widget list
                    widget_list[i].setCheckable(False)
                    widget_list[i].setChecked(True)
                    widget_list[i].setStyleSheet(f"QCheckBox::indicator {{ background-color: {darker_color}; }}")
            else: 
                # Set the gamma value to 0.0
                self._ui.localfit_mdwidget.gamma_radio.setChecked(False)
                for i in range(len(widget_list)):
                    # Activate the widget list
                    widget_list[i].setCheckable(True)
                    widget_list[i].setChecked(False)
                    widget_list[i].setStyleSheet("")
            
        else:
            # Set the gamma value to 0.0
            for i in range(len(widget_list)):
                # Activate the widget list
                widget_list[i].setCheckable(True)
                widget_list[i].setChecked(False)
                widget_list[i].setStyleSheet("")
        return