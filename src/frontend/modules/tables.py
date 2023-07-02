from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from . import data_classes

class TestDataTableModel(qtc.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._headers = [
            "Time (Days)",
            "Temperature (K)",
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
                test.test_data.strain
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
            "Stress Difference",
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

    def new_data(self):
        data = []
        for _ in range(len(self._headers)):
            data.append([""] * self.num_rows)

        self._data = data

        self.dataChanged.emit(
            qtc.QModelIndex(self.index(0, 0)),
            qtc.QModelIndex(self.index(len(self._headerkeys), self.num_rows)),
            [qtc.Qt.DisplayRole]  # type: ignore
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
                qtc.Qt.EditRole
            )

            self.setData(
                qtc.QModelIndex(self.index(row, 1)),
                test_suite.test_list[row].stress,
                qtc.Qt.EditRole
            )

            # TODO: Get color from user rather than hard coding it.
            self.setData(
                qtc.QModelIndex(self.index(row, 2)),
                test_suite.test_list[row].color,
                qtc.Qt.EditRole
            )

            # TODO: Get active state from user rather than hard coding it.
            self.setData(
                qtc.QModelIndex(self.index(row, 3)),
                test_suite.test_list[row].active_state,
                qtc.Qt.EditRole
            )

        print(self._data)

        self.refresh()

        return

    def refresh(self):
        self.dataChanged.emit(
            qtc.QModelIndex(self.index(0, 0)),
            qtc.QModelIndex(self.index(self.rowCount(None)-1, self.columnCount(None)-1)),
        )
        self.layoutChanged.emit()
        return


class TestListComboDelegate(qtw.QStyledItemDelegate):
    items = [
        "Blue",
        "Orange",
        "Green",
        "Red",
        "Purple",
        "Brown",
        "Pink",
        "Grey",
        "Olive",
        "Cyan",
    ]

    def __init__(self, parent=None):
        super(TestListComboDelegate, self).__init__(parent)
        print(self.items[1])
        return

    def createEditor(self, parent, option, index):
        self.editor = qtw.QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor

    def setEditorData(self, editor, index):
        value = index.data(qtc.Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)
        return

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(
            index, qtc.QVariant(value), qtc.Qt.DisplayRole
        )
        return

