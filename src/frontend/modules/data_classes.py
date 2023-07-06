from .unit_system import UnitSystem
from .plotting import PlotColors, ActiveState


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


class LocalFits:
    def __init__(self):
        return


class Test:
    def __init__(
        self,
        name: str,
        stress: str,
        color: PlotColors,
        active_state: ActiveState,
        test_data: TestData,
        local_fits: LocalFits,
        unit_system: UnitSystem,
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

        # Stores the local creep fits for the individual creep test
        self.local_fits = local_fits

        # Stores the unit system for the test
        self.unit_system = unit_system

        return


class TestSuite:
    def __init__(
        self,
    ):
        # This is a list imported creep tests. Will be updated
        #   when a new test is imported or deleted.
        self.test_list = []
        # This will store the number of imported tests. Will be updated
        #   when a new test is imported or deleted.
        self.num_tests = 0

        return

    def add_test(self, test):
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


def empty_testdata_class():
    empty_testdata = TestData(
        time_list=[], strain_list=[], stress_list=[], temperature_list=[]
    )

    return empty_testdata


def empty_localfits_class():
    empty_localfits = LocalFits()
    return empty_localfits


def empty_test_class():
    empty_test = Test(
        name="",
        stress=0,
        color="",
        time_unit="seconds",
        temp_unit="kelvin",
        stress_unit="mpa",
        active_state=True,
        test_data=empty_testdata_class(),
        local_fits=empty_localfits_class(),
    )
    return empty_test
