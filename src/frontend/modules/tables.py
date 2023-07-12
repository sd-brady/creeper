from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from . import unit_system
from . import data_classes


class TestDataTableModel(qtc.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._headers = [
            "Time (Seconds)",
            "Temperature (Kelvin)",
            "Deviatoric Stress (MPa)",
            "Creep Strain (-)",
        ]

        self._headerkeys = [
            "time",
            "temperature",
            "stress",
            "strain",
        ]

        self.num_rows = 5000
        self.new_data()

        self.qindex_topleft = qtc.QModelIndex(
            self.index(0, 0),
        )
        self.qindex_lowerright = qtc.QModelIndex(
            self.index(len(self._headerkeys), len(self._data[0]))
        )

        return

    def update_time_header(self, time_unit: unit_system.UnitTime):
        self._headers[0] = f"Time ({time_unit.value})"
        self.headerDataChanged.emit(qtc.Qt.Horizontal, 0, len(self._headers) - 1)
        return

    def update_temp_header(self, temp_unit: unit_system.UnitTemp):
        self._headers[1] = f"Temperature ({temp_unit.value})"
        self.headerDataChanged.emit(qtc.Qt.Horizontal, 0, len(self._headers) - 1)
        return

    def update_stress_header(self, stress_unit: unit_system.UnitStress):
        self._headers[2] = f"Deviatoric Stress ({stress_unit.value})"
        self.headerDataChanged.emit(qtc.Qt.Horizontal, 0, len(self._headers) - 1)
        return

    def new_data(self):
        data = []
        for col in range(len(self._headers)):
            data.append([""] * self.num_rows)

        self._data = data

        return

    def place_test(self, test: data_classes.Test):
        self.clear_data()

        data_list = [
            test.test_data.time,
            test.test_data.temperature,
            test.test_data.stress,
            test.test_data.strain,
        ]

        for col in range(len(self._headerkeys)):
            for row in range(len(test.test_data.time)):
                qindex = qtc.QModelIndex(self.index(row, col))
                self.setData(qindex, data_list[col][row], qtc.Qt.EditRole)

        self.dataChanged.emit(
            self.qindex_topleft, self.qindex_lowerright, [qtc.Qt.DisplayRole]  # type: ignore
        )

        return

    def clear_data(self):
        self.new_data()
        self.dataChanged.emit(
            self.qindex_topleft, self.qindex_lowerright, [qtc.Qt.DisplayRole]
        )
        return

    def place_data(self, testdata_dict):
        self.clear_data()

        for col in range(len(self._headerkeys)):
            column_data = testdata_dict[self._headerkeys[col]]
            for row in range(len(column_data)):
                self.setData(
                    qtc.QModelIndex(self.index(row, col)),
                    column_data[row],
                    qtc.Qt.EditRole,  # type: ignore
                )

        self.dataChanged.emit(
            self.qindex_topleft, self.qindex_lowerright, [qtc.Qt.DisplayRole]  # type: ignore
        )

        return

    def rowCount(self, parent):
        return len(self._data[0])

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):  # type: ignore
            return self._data[index.column()][index.row()]

    def headerData(self, section, orientation, role):
        if (
            orientation == qtc.Qt.Horizontal  # type: ignore
            and role == qtc.Qt.DisplayRole  # type: ignore
        ):
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def setData(self, index, value, role):
        if index.isValid() and role == qtc.Qt.EditRole:  # type: ignore
            self._data[index.column()][index.row()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def flags(self, index):
        return super().flags(index)


class TestListTableModel(qtc.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._headers = [
            "Test Name",
            "Deviatoric Stress (MPa)",
            "Plot Color",
            "Active",
        ]

        self._headerkeys = [
            "name",
            "stress",
            "color",
            "active",
        ]

        self.num_rows = 0
        self.new_data()

        return

    def update_stress_header(self, stress_unit: unit_system.UnitStress):
        self._headers[1] = f"Deviatoric Stress ({stress_unit.value})"
        self.headerDataChanged.emit(qtc.Qt.Horizontal, 0, len(self._headers) - 1)
        return

    def new_data(self):
        data = []
        for _ in range(len(self._headers)):
            data.append([""] * self.num_rows)

        self._data = data

        self.dataChanged.emit(
            qtc.QModelIndex(self.index(0, 0)),
            qtc.QModelIndex(self.index(len(self._headerkeys), self.num_rows)),
            [qtc.Qt.DisplayRole],  # type: ignore
        )

        return

    def clear_data(self):
        self.new_data()
        return

    def rowCount(self, parent):
        return self.num_rows

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):  # type: ignore
            return self._data[index.column()][index.row()]

    def headerData(self, section, orientation, role):
        if (
            orientation == qtc.Qt.Horizontal  # type: ignore
            and role == qtc.Qt.DisplayRole  # type: ignore
        ):
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def setData(self, index, value, role):
        if index.isValid() and role == qtc.Qt.EditRole:  # type: ignore
            self._data[index.column()][index.row()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def flags(self, index):
        return super().flags(index)

    def place_test_suite(self, test_suite: data_classes.TestSuite):
        self.num_rows = len(test_suite.test_list)
        self.clear_data()

        for row in range(len(test_suite.test_list)):
            self.setData(
                qtc.QModelIndex(self.index(row, 0)),
                test_suite.test_list[row].name,
                qtc.Qt.EditRole,
            )

            self.setData(
                qtc.QModelIndex(self.index(row, 1)),
                test_suite.test_list[row].stress,
                qtc.Qt.EditRole,
            )

            # TODO: Get color from user rather than hard coding it.
            self.setData(
                qtc.QModelIndex(self.index(row, 2)),
                test_suite.test_list[row].color.value,
                qtc.Qt.EditRole,
            )

            # TODO: Get active state from user rather than hard coding it.
            self.setData(
                qtc.QModelIndex(self.index(row, 3)),
                test_suite.test_list[row].active_state.value,
                qtc.Qt.EditRole,
            )

        self.refresh()

        return

    def get_test_info(self, row):
        # if row == -1:
        #     test_name = ""; stress = ""; color = ""; active = ""
        #     pass
        # else:
        test_name = self._data[0][row]
        stress = self._data[1][row]
        color = self._data[2][row]
        active = self._data[3][row]

        return (test_name, stress, color, active)

    def get_test_name(self, row):
        return self._data[0][row]

    def get_test_stress(self, row):
        return self._data[1][row]

    def get_test_color(self, row):
        return self._data[2][row]

    def get_test_active(self, row):
        return self._data[3][row]

    def refresh(self):
        self.dataChanged.emit(
            qtc.QModelIndex(self.index(0, 0)),
            qtc.QModelIndex(
                self.index(self.rowCount(None) - 1, self.columnCount(None) - 1)
            ),
        )
        self.layoutChanged.emit()
        return


class AddTestDialog(qtw.QDialog):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        layout = qtw.QFormLayout(self)

        self.inputs = []

        # ---- Rows are as follows
        # 0) Test Name (QLineEdit)
        # 1) Time Unit (QCombobox)
        # 2) Stress Unit (QCombobox)
        # 3) Temperature Unit (QCombobox)
        # 4) Applied Deviatoric Stress (QLineEdit)
        # 5) Color (QCombobox)
        # 6) Active Status (QCombobox)
        # 7) ButtonBox

        # QLineEdit for Test Name
        self.lineedit_testname = qtw.QLineEdit(self)
        layout.addRow("Test Name", self.lineedit_testname)

        # QComboBox for Units of Time
        self.combo_time = qtw.QComboBox(self)
        time_units = [member.value for member in unit_system.UnitTime]
        self.combo_time.addItems(time_units)
        self.combo_time.setCurrentText(unit_system.UnitTime["SECONDS"].value)
        layout.addRow("Time Unit", self.combo_time)

        # QComboBox for Units of Stress
        self.combo_stress = qtw.QComboBox(self)
        stress_units = [member.value for member in unit_system.UnitStress]
        self.combo_stress.addItems(stress_units)
        self.combo_stress.setCurrentText(unit_system.UnitStress["MPA"].value)
        layout.addRow("Stress Unit", self.combo_stress)

        # QComboBox for Units of Temperature
        self.combo_temp = qtw.QComboBox(self)
        temp_units = [member.value for member in unit_system.UnitTemp]
        self.combo_temp.addItems(temp_units)
        self.combo_temp.setCurrentText(unit_system.UnitTemp["KELVIN"].value)
        layout.addRow("Temperature Unit", self.combo_temp)

        # QLineEdit for Applied Deviatoric Stress
        self.lineedit_appstress = qtw.QLineEdit(self)
        layout.addRow("Applied Deviatoric Stress", self.lineedit_appstress)

        # QComboBox for plot color
        self.combo_color = qtw.QComboBox(self)
        colors = [member.value for member in data_classes.PlotColors]
        self.combo_color.addItems(colors)
        self.combo_color.setCurrentText(data_classes.PlotColors["BLUE"].value)
        layout.addRow("Plot Color", self.combo_color)

        # QComboBox for active_state
        self.combo_active = qtw.QComboBox(self)
        states = [member.value for member in data_classes.ActiveState]
        self.combo_active.addItems(states)
        self.combo_active.setCurrentText(data_classes.ActiveState["ON"].value)
        layout.addRow("Active Status", self.combo_active)

        buttonBox = qtw.QDialogButtonBox(
            qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel, self
        )
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        return

    def get_name(self) -> str:
        return self.lineedit_testname.text()

    def get_stress(self) -> str:
        return self.lineedit_appstress.text()

    def get_color(self) -> data_classes.PlotColors:
        return data_classes.PlotColors(self.combo_color.currentText())

    def get_active_state(self) -> data_classes.ActiveState:
        return data_classes.ActiveState(self.combo_active.currentText())

    def get_unit_system(self) -> unit_system.UnitSystem:
        unit_time = unit_system.UnitTime(self.combo_time.currentText())
        unit_stress = unit_system.UnitStress(self.combo_stress.currentText())
        unit_temp = unit_system.UnitTemp(self.combo_temp.currentText())
        return unit_system.UnitSystem(unit_time, unit_temp, unit_stress)


class EditTestDialog(qtw.QDialog):
    def __init__(
        self,
        name: str,
        stress: str,
        color: str,
        active: str,
        parent=None,
    ):
        super().__init__(parent)

        layout = qtw.QFormLayout(self)

        self.inputs = []

        # QLineEdit for Test Name
        self.lineedit_testname = qtw.QLineEdit(self, text=name)
        layout.addRow("Test Name", self.lineedit_testname)

        # QLineEdit for Applied Deviatoric Stress
        self.lineedit_appstress = qtw.QLineEdit(self, text=stress)
        layout.addRow("Applied Deviatoric Stress", self.lineedit_appstress)

        # QComboBox for plot color
        self.combo_color = qtw.QComboBox(self)
        colors = [member.value for member in data_classes.PlotColors]
        self.combo_color.addItems(colors)
        self.combo_color.setCurrentText(color)
        layout.addRow("Plot Color", self.combo_color)

        # QComboBox for active_state
        self.combo_active = qtw.QComboBox(self)
        states = [member.value for member in data_classes.ActiveState]
        self.combo_active.addItems(states)
        self.combo_active.setCurrentText(active)
        layout.addRow("Active Status", self.combo_active)

        buttonBox = qtw.QDialogButtonBox(
            qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel, self
        )
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        return

    def get_name(self) -> str:
        return self.lineedit_testname.text()

    def get_stress(self) -> str:
        return self.lineedit_appstress.text()

    def get_color(self) -> data_classes.PlotColors:
        return data_classes.PlotColors(self.combo_color.currentText())

    def get_active_state(self) -> data_classes.ActiveState:
        return data_classes.ActiveState(self.combo_active.currentText())
