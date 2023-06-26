from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .modules import canvas_classes
from .modules import table_classes
from .modules import canvas_classes

# DONE: Remove the padding from the single test plot on the
#   Test Suite tab.
#   - Removed the padding by switching to maptlotlib. Plots are looking nice
#   now.
# DONE: Stylize the single test plot on the Test Suite tab.
# TODO: Change the listbox to a table on the Test Suite tab.
# DONE: Change the data structure of self.tests in the View class.
#   The data structure should be a list of dictionaries, so that
#   the dictionary for a test can directly be passed into functions.
#   This will make updating tables and plots easier.
# TODO: Add functionality to remove the a test from the test list.
# TODO: Add functionality to rename tests.
# DONE: Figure out why there is stairstepping in the in the QChart plots.
#   - Fixed by changing from PyQt charts to matplotlib
# TODO: Begin adding the load/save functionality so that this can be
#   worked on as the project progresses (rather than trying to do it all
#   all at the end). This will make development easier because we won't
#   have to load in the tests every time we launch the GUI.
# DONE: Add functionality for the global test plot (i.e., shows all of the test
#   data on one plot).
# TODO: Make change to test data viewing table so that the active data shown
#   is completely controlled by the data for the test selected in the test list.
# TODO: Add functionality to move tests up and down in the test list.


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
        self.config_buttons()
        self.config_listboxes()
        self.config_plots()
        self.config_signals_slots()

        return

    def config_signals_slots(self):
        self._ui.list_ts_testlist.currentRowChanged.connect(self.testlist_changed)
        return

    def testlist_changed(self, row):
        self.canvas_ts_singleplot.update_plot(self.tests[row])
        # TODO: Change the table data
        self.canvas_ts_multiplot.update_plot(self.tests)
        return

    def config_plots(self):
        # self.testplot = canvas_classes.TestSuite_SinglePlot()
        # self._ui.verticalLayout_13.addWidget(self.testplot)

        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_singleplot = canvas_classes.SinglePlot_Strain_Canvas(self)
        self._ui.verticalLayout_13.addWidget(self.canvas_ts_singleplot)

        # Set up the single strain plot on the Test Suite Tab
        self.canvas_ts_multiplot = canvas_classes.MultiPlot_Strain_Canvas(self)
        self._ui.verticalLayout_14.addWidget(self.canvas_ts_multiplot)

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

    def config_buttons(self):
        self._ui.button_importtest.clicked.connect(self.import_test_data)
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
