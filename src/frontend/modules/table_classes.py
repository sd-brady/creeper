from PyQt5 import QtCore as qtc
import csv


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

        self.index_upperleft = qtc.QModelIndex(
            self.index(0, 0),
        )
        self.index_lowerright = qtc.QModelIndex(
            self.index(len(self._headerkeys), len(self._data[0]))
        )

        return

    def new_data(self):
        data = []
        for col in range(len(self._headers)):
            data.append([""] * self.num_rows)

        self._data = data

        return

    def clear_data(self):
        self.new_data()
        return

    def place_data(self, testdata_dict):
        self.clear_data()

        for col in range(len(self._headerkeys)):
            column_data = testdata_dict[self._headerkeys[col]]
            for row in range(len(column_data)):
                self._data[col][row] = column_data[row]

        self.dataChanged.emit(
            self.index_upperleft, self.index_lowerright, [qtc.Qt.DisplayRole] # type: ignore
        )

        return

    def validate_data(self):
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
