from PyQt5 import QtCore as qtc

from .modules import data_classes


class Model(qtc.QObject):
    test_suite_changed = qtc.pyqtSignal(data_classes.TestSuite)

    signal_test_validated = qtc.pyqtSignal(data_classes.Test)
    signal_error = qtc.pyqtSignal(str)
    signal_send_test = qtc.pyqtSignal(data_classes.Test)

    def __init__(self):
        super().__init__()
        self.test_suite = data_classes.TestSuite()
        return

    def add_test(self, test: data_classes.Test):
        valid = self.validate_new_test(
            test.name,
            test.stress,
            test.color,
            test.active_state,
        )

        if valid:
            self.test_suite.add_test(test)
            self.signal_test_validated.emit(test)
        else:
            self.signal_error.emit(
                "Invalid Test Data. Please check your input and try again."
            )
            pass

        # This will be connected later for functionality
        self.test_suite_changed.emit(self.test_suite)

        return

    def send_test(self, selected: qtc.QItemSelection, deselected: qtc.QItemSelection):
        if len(selected.indexes()) == 0:
            print("Nothing Selected.")
            pass
        else:
            print("Row", selected.indexes()[0].row())
            row = selected.indexes()[0].row()

            print(self.test_suite.num_tests)
            if row + 1 > self.test_suite.num_tests:
                self.signal_send_test.emit(data_classes.empty_test_class())
            else:
                self.signal_send_test.emit(self.test_suite.test_list[row])

        return

    @qtc.pyqtSlot(int)
    def delete_test(self, index):
        if index + 1 <= len(self.test_suite.test_list):
            self.test_suite.delete_test(index)
            self.test_suite_changed.emit(self.test_suite)
        return

    def move_test_down(self, test_index: int):
        # Swap the indexes of of the selected test and the test below it
        (
            self.test_suite.test_list[test_index],
            self.test_suite.test_list[test_index + 1],
        ) = (
            self.test_suite.test_list[test_index + 1],
            self.test_suite.test_list[test_index],
        )

        self.test_suite_changed.emit(self.test_suite)
        return

    def move_test_up(self, test_index: int):
        (
            self.test_suite.test_list[test_index],
            self.test_suite.test_list[test_index - 1],
        ) = (
            self.test_suite.test_list[test_index - 1],
            self.test_suite.test_list[test_index],
        )

        self.test_suite_changed.emit(self.test_suite)
        return

    def edit_test(
        self,
        test_index: int,
        name: str,
        stress: float,
        color: str,
        active: str,
    ):
        valid = self.validate_edit_test(test_index, name, stress, color, active)

        if valid:
            self.test_suite.test_list[test_index].name = name
            self.test_suite.test_list[test_index].stress = stress
            self.test_suite.test_list[test_index].color = color
            self.test_suite.test_list[test_index].active_state = active
            self.test_suite_changed.emit(self.test_suite)
        else:
            self.signal_error.emit(
                "Invalid Test Data. Please check your input and try again."
            )
            pass

        return

    def validate_new_test(self, new_name, new_stress, new_color, new_active):
        valid_list = []

        valid_list.append(self.validate_new_test_name(new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))
        valid_list.append(self.validate_new_test_color(new_color))
        valid_list.append(self.validate_new_test_active(new_active))

        print(valid_list)

        if False in valid_list:
            return False
        else:
            return True

    def validate_edit_test(
        self, test_index, new_name, new_stress, new_color, new_active
    ):
        valid_list = []

        valid_list.append(self.validate_edit_test_name(test_index, new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))
        valid_list.append(self.validate_new_test_color(new_color))
        valid_list.append(self.validate_new_test_active(new_active))

        print(valid_list)

        if False in valid_list:
            return False
        else:
            return True

    def validate_new_test_name(self, new_name):
        # Need to make sure the name is not already in the test suite
        if new_name in self.test_suite.get_test_names():
            return False
        elif new_name == "":
            return False
        else:
            return True

    def validate_edit_test_name(self, test_index, new_name):
        # Need to make sure the name is not already in the test suite
        #   (other than the test being edited)
        if (
            new_name in self.test_suite.get_test_names()
            and new_name != self.test_suite.test_list[test_index].name
        ):
            return False
        elif new_name == "":
            return False
        else:
            return True

    def validate_new_test_stress(self, new_stress):
        # Make sure it isn't an empty string
        if new_stress == "":
            return False
        # Make sure it is a float
        try:
            float(new_stress)
        except ValueError:
            return False

        # Make sure it is greater or equal to zero
        if float(new_stress) < 0:
            return False

        return True

    def validate_new_test_color(self, color):
        # Make sure it isn't an empty string
        if color == "":
            return False

        return True

    def validate_new_test_active(self, active):
        # Make sure the string is a boolean value
        if active in ["True", "False", "true", "false", "1", "0"]:
            return True
        else:
            return False

    @staticmethod
    def convert_time_to_seconds(from_value: float, from_unit: str):
        if from_unit == "seconds":
            to_value = from_value
        elif from_unit == "days":
            to_value = from_value * 24.0 * 60.0 * 60.0
        elif from_unit == "years":
            to_value = from_value * 365.0 * 24.0 * 60.0 * 60.0
        else:
            raise Exception("Invalid time unit")
        return to_value

    @staticmethod
    def convert_time_from_seconds(from_value: float, to_unit: str):
        if to_unit == "seconds":
            to_value = from_value
        elif to_unit == "days":
            to_value = from_value / (24.0 * 60.0 * 60.0)
        elif to_unit == "years":
            to_value = from_value / (365.0 * 24.0 * 60.0 * 60.0)
        else:
            raise Exception("Invalid time unit")
        return to_value

    @staticmethod
    def convert_stress_to_mpa(from_value: float, from_unit: str):
        if from_unit == "mpa":
            to_value = from_value
        elif from_unit == "psi":
            to_value = from_value / 145.0377377
        else:
            raise Exception("Invalid stress unit")
        return to_value

    def convert_stress_from_mpa(from_value: float, to_unit: str):
        if to_unit == "mpa":
            to_value = from_value
        elif to_unit == "psi":
            to_value = from_value * 145.0377377
        else:
            raise Exception("Invalid stress unit")
        return to_value

    def convert_temp_to_kelvin(from_value: float, from_unit: str):
        if from_unit == "K":
            to_value = from_value
        elif from_unit == "C":
            to_value = from_value + 273.15
        elif from_unit == "F":
            to_value = (from_value - 32) * (5.0 / 9.0) + 273.15
        elif from_unit == "R":
            to_value = from_value * (5.0 / 9.0)
        else:
            raise Exception("Invalid temperature unit")
        return to_value

    def convert_temp_from_kelvin(from_value: float, to_unit: str):
        if to_unit == "K":
            to_value = from_value
        elif to_unit == "C":
            to_value = from_value - 273.15
        elif to_unit == "F":
            to_value = (from_value - 273.15) * (9.0 / 5.0) + 32
        elif to_unit == "R":
            to_value = from_value / (5.0 / 9.0)
        else:
            raise Exception("Invalid temperature unit")
        return to_value
