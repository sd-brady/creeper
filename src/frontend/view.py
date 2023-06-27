from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import pandas as pd
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import matplotlib.pyplot as plt

from .modules import canvas_classes
from .modules import table_classes
from .modules import canvas_classes
from backend import creeprate


class View(qtw.QWidget):
    signal_errorbox = qtc.pyqtSignal(str)
    signal_test_added = qtc.pyqtSignal(str, dict)

    def __init__(self, ui):
        super().__init__()

        self._ui = ui
        self._ui.stacked_toplevel.setCurrentIndex(0)

        # Initialize a list to store imported creep tests
        self.tests = []

        self.config_tables()
        self.config_listboxes()
        self.config_plots()
        self.config_comboboxes()
        self.config_signals_slots()

        return

    def config_comboboxes(self):
        self._ui.verticalLayout_9.setAlignment(self._ui.combo_ts_plotpicker, qtc.Qt.AlignRight)  # type: ignore
        return

    def config_signals_slots(self):
        return

    def testlist_changed(self, row):
        plotvar = self._ui.combo_ts_plotpicker.currentIndex()
        print("row: ", row)

        if row == -1:
            self.canvas_ts_singleplot.setup_initial_figure()
        elif plotvar == 0:
            self.canvas_ts_singleplot.update_plot_strain(self.tests[row])
        elif plotvar == 1:
            self.canvas_ts_singleplot.update_plot_strainrate(self.tests[row])
        elif plotvar == 2:
            self.canvas_ts_singleplot.update_plot_stress(self.tests[row])
        elif plotvar == 3:
            self.canvas_ts_singleplot.update_plot_temp(self.tests[row])

        # Update the multi-test plot
        self.canvas_ts_multiplot.update_plot(self.tests)

        # Update the test data table
        print("ayye", self.tests[row]["name"])
        self.testdata_model.place_data(self.tests[row])

        return

    def config_plots(self):
        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_singleplot = canvas_classes.SinglePlot_Strain_Canvas(self)
        toolbar1 = NavigationToolbar(self.canvas_ts_singleplot, self)
        self._ui.verticalLayout_13.addWidget(toolbar1)
        self._ui.verticalLayout_13.addWidget(self.canvas_ts_singleplot)
        self._ui.verticalLayout_13.setAlignment(toolbar1, qtc.Qt.AlignHCenter)  # type: ignore

        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_multiplot = canvas_classes.MultiPlot_Strain_Canvas(self)
        toolbar2 = NavigationToolbar(self.canvas_ts_multiplot, self)
        self._ui.verticalLayout_14.addWidget(toolbar2)
        self._ui.verticalLayout_14.addWidget(self.canvas_ts_multiplot)
        self._ui.verticalLayout_14.setAlignment(toolbar2, qtc.Qt.AlignHCenter)  # type: ignore

        return

    def config_listboxes(self):
        self.config_testlist_listbox()
        return

    def config_testlist_listbox(self):
        self.listbox_testlist_model = self._ui.list_ts_testlist.model()
        return

    def config_tables(self):
        # Configure the test data table
        self.config_testdata_table()
        return

    def config_testdata_table(self):
        # Set the table model
        self.testdata_model = table_classes.TestDataTableModel()
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

    def ts_plotpicker_changed(self, index):
        test_index = self._ui.list_ts_testlist.currentRow()
        if index == -1:
            self.canvas_ts_singleplot.setup_initial_figure()
        elif index == 0:
            self.canvas_ts_singleplot.update_plot_strain(self.tests[test_index])
        elif index == 1:
            self.canvas_ts_singleplot.update_plot_strainrate(self.tests[test_index])
        elif index == 2:
            self.canvas_ts_singleplot.update_plot_stress(self.tests[test_index])
        elif index == 3:
            self.canvas_ts_singleplot.update_plot_temp(self.tests[test_index])
        return

    def delete_test(self):
        active_test = self._ui.list_ts_testlist.currentRow()
        if active_test == -1:
            pass
        else:
            for i in range(len(self.tests)):
                print(self.tests[i]["name"])
            self.tests.pop(active_test)
            print("During Test Deletion")
            for i in range(len(self.tests)):
                print(self.tests[i]["name"])
            self._ui.list_ts_testlist.setCurrentRow(-1)
            self._ui.list_ts_testlist.takeItem(active_test)

        print("After Test Deletion")
        for i in range(len(self.tests)):
            print(self.tests[i]["name"])

    def import_test_data(self):
        filename = self.select_file()

        # Make sure that the file is a CSV file
        if filename[-4::] != ".csv":
            self.signal_errorbox.emit("File must be a CSV file.")
        else:
            # Import the test data from the CSV file. Store the data in a dictionary
            # with the keys being the column headers from the table model.
            # testdata_dict = pd.read_csv(filename, ).to_dict(orient="list")
            testdata_dict = pd.read_csv(
                filename, header=0, names=self.testdata_model._headerkeys  # type: ignore
            ).to_dict(orient="list")

            test_name = qtw.QInputDialog.getText(
                self, "Input Dialog", "Enter Test Name: "
            )[0]

            # Check to see if the test name already exists
            current_test_list = []
            for x in range(self._ui.list_ts_testlist.count() - 1):
                current_test_list.append(self._ui.list_ts_testlist.item(x))

            if test_name in current_test_list:
                self.signal_errorbox.emit("Test name already exists.")
                return
            elif test_name == "":
                self.signal_errorbox.emit("Test name cannot be blank.")
                return
            else:
                self.signal_test_added.emit(test_name, testdata_dict)

                # Add the test name to the test dictionary
                testdata_dict["name"] = test_name

                # Add strain rate to the dictionary.
                testdata_dict["strain_rate"] = creeprate.get_strain_rate(
                    testdata_dict["time"], testdata_dict["strain"]
                )

                # Add the test to the global test list
                self.tests.append(testdata_dict)

                # Add the test to the test listbox on the Test Suite tab
                listbox_item = qtw.QListWidgetItem(test_name)
                listbox_item.setTextAlignment(qtc.Qt.AlignCenter)  # type: ignore
                self._ui.list_ts_testlist.addItem(listbox_item)
                #   Set the active item in the listbox to the new item
                listbox_active_index = self._ui.list_ts_testlist.count() - 1
                self._ui.list_ts_testlist.setCurrentRow(listbox_active_index)

        return

    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            None,
            "Select CSV File to Open...",
            r"C:\Users\brady\Documents\GitHub\saltycreep\examples\Markham 10a",
            "CSV Files (*.csv) ;; All Files (*)",
        )

        return filename
