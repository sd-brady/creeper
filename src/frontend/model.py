from copy import deepcopy
from PyQt5 import QtCore as qtc

from .modules import data_classes
from .modules import unit_system
from .modules import mdmodel


class Model(qtc.QObject):
    test_suite_changed = qtc.pyqtSignal(data_classes.TestSuite)

    signal_test_validated = qtc.pyqtSignal(data_classes.Test)
    signal_error = qtc.pyqtSignal(str)
    signal_send_test = qtc.pyqtSignal(data_classes.Test)
    signal_send_testsuite = qtc.pyqtSignal(data_classes.TestSuite)
    signal_lf_fitlist_changed = qtc.pyqtSignal(list)
    signal_send_localfit_name_list = qtc.pyqtSignal(list)
    signal_send_mdmodel = qtc.pyqtSignal(mdmodel.MdModel)

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
            self.test_suite_changed.emit(deepcopy(self.test_suite))

        else:
            self.signal_error.emit(
                "Invalid Test Data. Please check your input and try again."
            )
            pass
        return

    def send_test(self, selected: qtc.QItemSelection, deselected: qtc.QItemSelection):
        if len(selected.indexes()) == 0:
            pass
        else:
            row = selected.indexes()[0].row()
            if row + 1 > self.test_suite.num_tests or row < 0:
                self.signal_send_test.emit(deepcopy(data_classes.empty_test_class()))
            else:
                self.signal_send_test.emit(deepcopy(self.test_suite.test_list[row]))
        return

    @qtc.pyqtSlot(int)
    def delete_test(self, index):
        if index + 1 <= len(self.test_suite.test_list):
            self.test_suite.delete_test(index)
            self.test_suite_changed.emit(deepcopy(self.test_suite))
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

        self.test_suite_changed.emit(deepcopy(self.test_suite))
        return

    def move_test_up(self, test_index: int):
        (
            self.test_suite.test_list[test_index],
            self.test_suite.test_list[test_index - 1],
        ) = (
            self.test_suite.test_list[test_index - 1],
            self.test_suite.test_list[test_index],
        )

        self.test_suite_changed.emit(deepcopy(self.test_suite))
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
            self.test_suite_changed.emit(deepcopy(self.test_suite))
        else:
            self.signal_error.emit(
                "Invalid Test Data. Please check your input and try again."
            )
            pass

        return

    def validate_new_test(self, new_name, new_stress):
        valid_list = []

        valid_list.append(self.validate_new_test_name(new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))

        if False in valid_list:
            return False
        else:
            return True

    def validate_edit_test(self, test_index, new_name, new_stress):
        valid_list = []

        valid_list.append(self.validate_edit_test_name(test_index, new_name))
        valid_list.append(self.validate_new_test_stress(new_stress))

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

    def send_current_testsuite(self):
        self.signal_send_testsuite.emit(deepcopy(self.test_suite))
        return

    def fun_debug(self):
        if len(self.test_suite.test_list) > 0:
            print(self.test_suite.test_list[0].stress)
        else:
            print("No tests.")

    def add_localfit(self, test_index: int, localfit: data_classes.LocalFit):
        # Validate Local Fit Name
        # Need to make sure the name is not already in the local fit list
        current_names = self.test_suite.test_list[test_index].get_localfit_names()

        if localfit.name in current_names:
            self.signal_error.emit("Local Fit with this name already exists.")
        elif localfit.name == "":
            self.signal_error.emit("Name of Local Fit cannot be an empty string.")
        else:
            self.test_suite.test_list[test_index].add_localfit(localfit)
            self.signal_lf_fitlist_changed.emit(
                deepcopy(self.test_suite.test_list[test_index].get_localfit_names())
            )

        print("Num_localfits: ", self.test_suite.test_list[test_index].num_localfits)

        return

    def send_localfit_name_list(self, test_index: int):
        self.signal_send_localfit_name_list.emit(
            deepcopy(self.test_suite.test_list[test_index].get_localfit_names())
        )
        return

    def send_localfit_mdmodel(self, test_index: int, fit_index: int):
        if test_index == -1 or fit_index == -1:
            pass
        else:
            self.signal_send_mdmodel.emit(
                deepcopy(
                    self.test_suite.test_list[test_index]
                    .localfit_list[fit_index]
                    .mdmodel
                )
            )
        return

    def delete_localfit(self, test_index, fit_index):
        self.test_suite.test_list[test_index].delete_localfit(fit_index)
        self.signal_send_localfit_name_list.emit(
            deepcopy(self.test_suite.test_list[test_index].get_localfit_names())
        )
        # If the test is
        return

    def edit_localfit_name(self, test_index: int, fit_index: int, name: str):
        # Make sure that the name isn't empty
        if name == "":
            self.signal_error.emit("Fit Name cannot be an empty string.")
        elif name in self.test_suite.test_list[test_index].get_localfit_names():
            self.signal_error.emit("Fit Name already exists for the current test.")
        else:
            self.test_suite.test_list[test_index].localfit_list[fit_index].name = name
            self.signal_send_localfit_name_list.emit(
                deepcopy(self.test_suite.test_list[test_index].get_localfit_names())
            )
        return

    def change_localfit_primary(self, test_index, fit_index):
        print("We're in!")
        current_primary = self.get_current_primary_localfit(
            self.test_suite.test_list[test_index]
        )
        if current_primary == -1:
            pass
        else:
            # Demote the current primary
            self.test_suite.test_list[test_index].localfit_list[
                current_primary
            ].demote_primary()

        # Promote the new primary
        self.test_suite.test_list[test_index].localfit_list[fit_index].promote_primary()

        self.signal_send_localfit_name_list.emit(
            deepcopy(self.test_suite.test_list[test_index].get_localfit_names())
        )

        return

    @staticmethod
    def get_current_primary_localfit(test: data_classes.Test):
        index = -1
        for i in range(test.num_localfits):
            if test.localfit_list[i].primary is True:
                index = i
            else:
                pass
        return index

    def save_localfit(self, test_index, fit_index, md_model: mdmodel.MdModel):
        self.test_suite.test_list[test_index].localfit_list[
            fit_index
        ].mdmodel = md_model
        return
