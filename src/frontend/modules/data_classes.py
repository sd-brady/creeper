from enum import Enum


from .mdmodel import MdTableModel


class PlotType(Enum):
    STRAIN = "Strain"
    STRAINRATE = "Strain Rate"
    STRESS = "Deviatoric Stress"
    TEMPERATURE = "Temperature"


class ActiveState(Enum):
    ON = "On"
    OFF = "Off"


class PlotColors(Enum):
    BLUE = "tab:blue"
    ORANGE = "tab:orange"
    GREEN = "tab:green"
    RED = "tab:red"
    PURPLE = "tab:purple"
    BROWN = "tab:brown"
    PINK = "tab:pink"
    GRAY = "tab:gray"
    OLIVE = "tab:olive"
    CYAN = "tab:cyan"


class TestData:
    def __init__(
        self,
        time_list: list,
        strain_list: list,
        stress_list: list,
        temperature_list: list,
    ):
        self.time = time_list
        self.strain = strain_list
        self.stress = stress_list
        self.temperature = temperature_list

        self.get_strainrate()

        return

    def get_strainrate(self):
        self.strainrate = []

        for i in range(1, len(self.time)):
            self.strainrate.append(
                (self.strain[i] - self.strain[i - 1])
                / (self.time[i] - self.time[i - 1])
            )

        return


class LocalFit:
    def __init__(self, mdtablemodel: MdTableModel, name: str):
        self.mdtablemodel = mdtablemodel
        self.name = name
        self.primary = False
        return

    def promote_primary(self):
        # print("Before Name: ", self.name)
        self.primary = True
        # self.name = "* " + self.name + " *"
        # print("After Name: ", self.name)
        return

    def demote_primary(self):
        self.primary = False
        # self.name = self.name[2:-2]
        return


class Test:
    def __init__(
        self,
        name: str,
        stress: str,
        color: PlotColors,
        active_state: ActiveState,
        test_data: TestData,
    ):
        # Stores the Name of the Test
        self.name = name

        # Stores the deviatoric stress of the test
        self.stress = stress

        # Stores the color that the test will be plotted at.
        self.color = color

        # Store the active state of the test.
        self.active_state = active_state

        # Stores the laboratory test data in the units [time_unit] and
        #   [stress_unit]
        self.test_data = test_data

        # Initialize the local fits list
        self.localfit_list: list[LocalFit] = []
        self.num_localfits: int = 0

        return

    def add_localfit(self, fit: LocalFit):
        self.localfit_list.append(fit)
        self.num_localfits += 1
        return

    def delete_localfit(self, localfit_index):
        self.localfit_list.pop(localfit_index)
        self.num_localfits -= 1
        return

    def get_localfit_names(self):
        names = []
        for i in range(self.num_localfits):
            names.append(self.localfit_list[i].name)

        return names


class TestSuite:
    def __init__(
        self,
    ):
        # This is a list imported creep tests. Will be updated
        #   when a new test is imported or deleted.
        self.test_list: list[Test] = []
        # This will store the number of imported tests. Will be updated
        #   when a new test is imported or deleted.
        self.num_tests: int = 0

        return

    def add_test(self, test: Test):
        self.test_list.append(test)
        self.num_tests += 1
        return

    def delete_test(self, test_index):
        self.test_list.pop(test_index)
        self.num_tests -= 1
        return

    def get_test_names(self):
        if self.num_tests == 0:
            test_name_list = []
        else:
            test_name_list = [test.name for test in self.test_list]

        return test_name_list


def empty_test_class():
    empty_test = Test(
        "empty",
        "0",
        PlotColors("Blue"),
        ActiveState("Off"),
        TestData([], [], [], []),
    )
    return empty_test
