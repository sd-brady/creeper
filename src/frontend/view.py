from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import pandas as pd
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)

from .modules import tables
from .modules import plotting
from .modules import data_classes


class View(qtw.QWidget):
    signal_errorbox = qtc.pyqtSignal(str)
    signal_test_added = qtc.pyqtSignal(data_classes.Test)
    signal_test_deleted = qtc.pyqtSignal(int)

    def __init__(self, ui):
        super().__init__()

        self._ui = ui
        self._ui.stacked_toplevel.setCurrentIndex(0)

        self.config_tables()
        self.config_plots()
        self.config_comboboxes()

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

    def config_testlist_table(self):
        # Set the table model
        self.testlist_model = tables.TestListTableModel()
        self._ui.table_testlist.setModel(self.testlist_model)

        # Set the "Active" column to a checkbox using a delegate


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
                filename, header=0, names=self.testdata_model._headerkeys  # type: ignore
            ).to_dict(orient="list")

            # Get the test name from the user
            test_name = qtw.QInputDialog.getText(
                self, "Input Dialog", "Enter Test Name: "
            )[0]


            test_data = data_classes.TestData(
                    time_list = imported_data["time"],
                    strain_list = imported_data["strain"],
                    stress_list = imported_data["stress"],
                    temperature_list = imported_data["temperature"],
                    )

            # Initialize Local Fit Class for the Test
            local_fits = data_classes.LocalFits()
            test = data_classes.Test(
                    name= test_name,
                    time_unit= "days",
                    stress_unit= "mpa",
                    TestData= test_data,
                    LocalFits= local_fits,
                    )
            self.signal_test_added.emit(test)

        return

    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            None,
            "Select CSV File to Open...",
            r"C:\Users\brady\Documents\GitHub\saltycreep\examples\Markham 10a",
            "CSV Files (*.csv) ;; All Files (*)",
        )

        return filename

    def test_added(self, test: data_classes.Test):
        # Add Test to the test list table

        return

