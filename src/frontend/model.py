from PyQt5 import QtCore as qtc

from .modules import data_classes


class Model(qtc.QObject):

    signal_test_validated = qtc.pyqtSignal(data_classes.Test)
    signal_error = qtc.pyqtSignal(str)
    signal_send_test = qtc.pyqtSignal(data_classes.Test)

    def __init__(self):
        super().__init__()
        self.test_suite = data_classes.TestSuite()
        return

    def add_test(self, test: data_classes.Test):

        valid = self.validate_test(test)

        if valid:
            self.test_suite.add_test(test)
            self.signal_test_validated.emit(test)
        else:
            self.signal_error.emit("Invalid Test Data. Please check your input and try again.")
            pass

        return

    def send_test(self, selected, deselected):
        print(selected.row())
        print(self.test_suite.num_tests)
        if selected.row()+1 > self.test_suite.num_tests:
            self.signal_send_test.emit(data_classes.empty_test_class())
        else:
            self.signal_send_test.emit(self.test_suite.test_list[selected.row()])
        return

    def validate_test(self, test: data_classes.Test):

        # Validate test name
        #   TODO: probably should add more validation here
        if test.name == '':
            return False
        elif test.name in self.test_suite.get_test_names():
            return False
        else:
            pass

        # Validate time_unit
        if test.time_unit in ["seconds", "days", "years"]:
            pass
        else:
            return False

        # Validate stress unit
        if test.stress_unit in ["psi", "mpa"]:
            pass
        else:
            return False

        # TODO: Validate TestData class (time, strain, stress, and temperature lists)
        # TODO: Validate LocalFits
        
        return True

    def delete_test(self, test_index):
        self.test_suite.delete_test(test_index)
        return
