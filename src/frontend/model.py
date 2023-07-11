from PyQt5 import QtCore as qtc

from .modules import data_classes
from .modules import unit_system


class Model(qtc.QObject):
    test_suite_changed = qtc.pyqtSignal(data_classes.TestSuite)

    signal_test_validated = qtc.pyqtSignal(data_classes.Test)
    signal_error = qtc.pyqtSignal(str)
    signal_send_test = qtc.pyqtSignal(data_classes.Test)
    signal_send_testsuite = qtc.pyqtSignal(data_classes.TestSuite)

    def __init__(self):
        super().__init__()
        self.test_suite = data_classes.TestSuite()
        return

    def add_test(self, test: data_classes.Test, usys: unit_system.UnitSystem):
        valid = self.validate_new_test(test.name, test.stress)

        if valid:
            # Convert everything to base unit system (MPa, seconds, kelvin)
            test = unit_system.convert_test_to_base(test, usys)

            self.test_suite.add_test(test)
            self.test_suite_changed.emit(self.test_suite)

        else:
            self.signal_error.emit(
                "Invalid Test Data. Please check your input and try again."
            )
            pass

        print("1.")
        return

    def send_test(self, selected: qtc.QItemSelection, deselected: qtc.QItemSelection):
        if len(selected.indexes()) == 0:
            pass
        else:
            row = selected.indexes()[0].row()
            if row + 1 > self.test_suite.num_tests:
                self.signal_send_test.emit(data_classes.empty_test_class())
            else:
                self.signal_send_test.emit(self.test_suite.test_list[row])
        print("2.")
        return

    @qtc.pyqtSlot(int)
    def delete_test(self, index):
        if index + 1 <= len(self.test_suite.test_list):
            self.test_suite.delete_test(index)
            self.test_suite_changed.emit(self.test_suite)
        print("3.")
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
        print("4.")
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
        print("5.")
        return

    def edit_test(
        self,
        test_index: int,
        name: str,
        stress: float,
        color: data_classes.PlotColors,
        active: data_classes.ActiveState,
    ):
        valid = self.validate_edit_test(test_index, name, stress)

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

        print("6.")
        return

    def validate_new_test(self, new_name, new_stress):
        valid_list = []

        valid_list.append(self.validate_new_test_name(new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))

        print("7.")
        if False in valid_list:
            return False
        else:
            return True

    def validate_edit_test(self, test_index, new_name, new_stress):
        valid_list = []

        valid_list.append(self.validate_edit_test_name(test_index, new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))

        print("8.")
        if False in valid_list:
            return False
        else:
            return True

    def validate_new_test_name(self, new_name):
        print("9.")
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

        print("10.")
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
        print("11.")
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

    def send_current_testsuite(self):
        self.signal_send_testsuite.emit(self.test_suite)
        return

    def fun_debug(self):
        print("13.")
        if len(self.test_suite.test_list) > 0:
            print(self.test_suite.test_list[0].stress)
        else:
            print("No tests.")
