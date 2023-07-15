from enum import Enum
from typing import TYPE_CHECKING

# TODO: Add unit tests for the unit conversion functions

if TYPE_CHECKING:
    from . import data_classes
    from . import mdmodel


class UnitTime(Enum):
    """
    Enum options are (reference them later by UnitTime['NAME']):
    1: SECONDS
    2: DAYS
    3: YEARS
    """

    SECONDS = "Seconds"
    DAYS = "Days"
    YEARS = "Years"


class UnitTemp(Enum):
    """
    Enum options are (reference them later by UnitTemp['NAME']):
    1: KELVIN
    2: CELSIUS
    3: FAHRENHEIT
    4: RANKINE
    """

    # CELSIUS = "\N{DEGREE SIGN}C"
    # FAHRENHEIT = "\N{DEGREE SIGN}F"

    KELVIN = "Kelvin"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"
    RANKINE = "Rankine"


class UnitStress(Enum):
    """
    Enum options are (reference them later by UnitStress['NAME']):
    1: MPA
    2: PSI
    """

    MPA = "MPa"
    PSI = "psi"


class UnitSystem:
    def __init__(self, time: UnitTime, temperature: UnitTemp, stress: UnitStress):
        """
        This class is used to store the set of units for various objects.

        Examples could include:
        1) The units for an imported test.
        2) The units for the active gui window (based on selected widget values)
        """
        self.time = time
        self.temperature = temperature
        self.stress = stress
        return


def convert_time_to_base(from_value: float, from_unit: UnitTime):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif from_unit.name == UnitTime["DAYS"].name:
        to_value = from_value * 24.0 * 60.0 * 60.0
    elif from_unit.name == UnitTime["YEARS"].name:
        to_value = from_value * 365.0 * 24.0 * 60.0 * 60.0
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_time_from_base(from_value: float, to_unit: UnitTime):
    if from_value == "":
        return from_value
    if to_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif to_unit.name == UnitTime["DAYS"].name:
        to_value = from_value / (24.0 * 60.0 * 60.0)
    elif to_unit.name == UnitTime["YEARS"].name:
        to_value = from_value / (365.0 * 24.0 * 60.0 * 60.0)
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_stress_to_base(from_value: float, from_unit: UnitStress):
    if from_value == "":
        return from_value
    if from_unit.name == UnitStress["MPA"].name:
        to_value = from_value
    elif from_unit.name == UnitStress["PSI"].name:
        to_value = from_value / 145.0377377
    else:
        raise Exception("Invalid stress unit.")
    return to_value


def convert_stress_from_base(from_value: float, to_unit: UnitStress):
    if from_value == "":
        return from_value
    if to_unit.name == UnitStress["MPA"].name:
        to_value = from_value
    elif to_unit.name == UnitStress["PSI"].name:
        to_value = from_value * 145.0377377
    else:
        raise Exception("Invalid stress unit.")
    return to_value


def convert_temp_to_base(from_value: float, from_unit: UnitTemp):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif from_unit.name == UnitTemp["CELSIUS"].name:
        to_value = from_value + 273.15
    elif from_unit.name == UnitTemp["FAHRENHEIT"].name:
        to_value = (from_value - 32) * (5.0 / 9.0) + 273.15
    elif from_unit.name == UnitTemp["RANKINE"].name:
        to_value = from_value * (5.0 / 9.0)
    else:
        raise Exception("Invalid temperature unit")
    return to_value


def convert_temp_from_base(from_value: float, to_unit: UnitTemp):
    if from_value == "":
        return from_value
    if to_unit.name == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif to_unit.name == UnitTemp["CELSIUS"].name:
        to_value = from_value - 273.15
    elif to_unit.name == UnitTemp["FAHRENHEIT"].name:
        to_value = (from_value - 273.15) * (9.0 / 5.0) + 32
    elif to_unit.name == UnitTemp["RANKINE"].name:
        to_value = from_value / (5.0 / 9.0)
    else:
        raise Exception("Invalid temperature unit")
    return to_value


def convert_testsuite_from_base(
    test_suite: "data_classes.TestSuite", gui_usys: UnitSystem
):
    for i in range(len(test_suite.test_list)):
        test_suite.test_list[i] = convert_test_from_base(
            test_suite.test_list[i], gui_usys
        )
    return test_suite


def convert_test_from_base(test: "data_classes.Test", gui_usys: UnitSystem):
    # Convert "Applied Deviatoric Stress" to gui units
    test.stress = convert_stress_from_base(float(test.stress), gui_usys.stress)

    # Convert "test.test_data.time" to base units
    for i in range(len(test.test_data.time)):
        test.test_data.time[i] = convert_time_from_base(
            test.test_data.time[i], gui_usys.time
        )

    # Convert "test.test_data.stress" list to gui units
    for i in range(len(test.test_data.stress)):
        test.test_data.stress[i] = convert_stress_from_base(
            test.test_data.stress[i], gui_usys.stress
        )

    # Convert "test.test_data.strain_rate" list to gui units
    for i in range(len(test.test_data.strainrate)):
        test.test_data.strainrate[i] = convert_strainrate_from_base(
            test.test_data.strainrate[i], gui_usys.time
        )

    # Convert "test.test_data.temp" list to gui units
    for i in range(len(test.test_data.temperature)):
        test.test_data.temperature[i] = convert_temp_from_base(
            test.test_data.temperature[i], gui_usys.temperature
        )

    # Convert local fits to gui units

    return test


def convert_strainrate_from_base(from_value: float, from_unit: UnitTime):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif from_unit.name == UnitTime["DAYS"].name:
        to_value = from_value * 24.0 * 60.0 * 60.0
    elif from_unit.name == UnitTime["YEARS"].name:
        to_value = from_value * 365.0 * 24.0 * 60.0 * 60.0
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_strainrate_to_base(from_value: float, from_unit: UnitTime):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif from_unit.name == UnitTime["DAYS"].name:
        to_value = from_value / (24.0 * 60.0 * 60.0)
    elif from_unit.name == UnitTime["YEARS"].name:
        to_value = from_value / (365.0 * 24.0 * 60.0 * 60.0)
    else:
        raise Exception("Invalid time unit.")
    return to_value


def get_base_unit_system():
    usys = UnitSystem(UnitTime["SECONDS"], UnitTemp["KELVIN"], UnitStress["MPA"])
    return usys


def convert_test_to_base(test: "data_classes.Test", test_usys: UnitSystem):
    # Convert "Applied Deviatoric Stress" to base units
    test.stress = convert_stress_to_base(float(test.stress), test_usys.stress)

    # Convert "test.test_data.time" to base units
    for i in range(len(test.test_data.time)):
        test.test_data.time[i] = convert_time_to_base(
            test.test_data.time[i], test_usys.time
        )

    # Convert "test.test_data.stress" list to gui units
    for i in range(len(test.test_data.stress)):
        test.test_data.stress[i] = convert_stress_to_base(
            test.test_data.stress[i], test_usys.stress
        )

    # Convert "test.test_data.strain_rate" list to gui units
    for i in range(len(test.test_data.strainrate)):
        test.test_data.strainrate[i] = convert_strainrate_to_base(
            test.test_data.strainrate[i], test_usys.time
        )

    # Convert "test.test_data.temp" list to gui units
    for i in range(len(test.test_data.temperature)):
        test.test_data.temperature[i] = convert_temp_to_base(
            test.test_data.temperature[i], test_usys.temperature
        )

    # Convert local fits to gui units
    return test


def convert_mdmodel_from_base(md_model: "mdmodel.MdModel", gui_usys: UnitSystem):
    print(md_model.a1)
    print(type(md_model.a1))
    # Convert Parameters with Time Units (a1, a2, b1, b2)
    md_model.a1 = convert_invtime_from_base(md_model.a1, gui_usys.time)
    md_model.a2 = convert_invtime_from_base(md_model.a2, gui_usys.time)
    md_model.b1 = convert_invtime_from_base(md_model.b1, gui_usys.time)
    md_model.b2 = convert_invtime_from_base(md_model.b2, gui_usys.time)

    # Convert Parameters with Temperature Units (q1divr, q2divr, c)
    md_model.q1divr = convert_temp_from_base(md_model.q1divr, gui_usys.temperature)
    md_model.q2divr = convert_temp_from_base(md_model.q2divr, gui_usys.temperature)
    md_model.c = convert_invtemp_from_base(md_model.c, gui_usys.temperature)

    # Convert Parameters with Stress Units (sig0, mu)
    md_model.sig0 = convert_stress_from_base(md_model.sig0, gui_usys.stress)
    md_model.mu = convert_stress_from_base(md_model.mu, gui_usys.stress)

    return md_model


def convert_mdmodel_to_base(md_model: "mdmodel.MdModel", usys: UnitSystem):
    # Convert Parameters with Time Units (a1, a2, b1, b2)
    md_model.a1 = convert_invtime_to_base(md_model.a1, usys.time)
    md_model.a2 = convert_invtime_to_base(md_model.a2, usys.time)
    md_model.b1 = convert_invtime_to_base(md_model.b1, usys.time)
    md_model.b2 = convert_invtime_to_base(md_model.b2, usys.time)

    # Convert Parameters with Temperature Units (q1divr, q2divr, c)
    md_model.q1divr = convert_temp_to_base(md_model.q1divr, usys.temperature)
    md_model.q2divr = convert_temp_to_base(md_model.q2divr, usys.temperature)
    md_model.c = convert_invtemp_to_base(md_model.c, usys.temperature)

    # Convert Parameters with Stress Units (sig0, mu)
    md_model.sig0 = convert_stress_to_base(md_model.sig0, usys.stress)
    md_model.mu = convert_stress_to_base(md_model.mu, usys.stress)

    return md_model


def convert_invtime_to_base(from_value: float, from_unit: UnitTime):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif from_unit.name == UnitTime["DAYS"].name:
        to_value = from_value / (24.0 * 60.0 * 60.0)
    elif from_unit.name == UnitTime["YEARS"].name:
        to_value = from_value / (365.0 * 24.0 * 60.0 * 60.0)
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_invtime_from_base(from_value: float, to_unit: UnitTime):
    if from_value == "":
        return from_value
    if to_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif to_unit.name == UnitTime["DAYS"].name:
        to_value = from_value * (24.0 * 60.0 * 60.0)
    elif to_unit.name == UnitTime["YEARS"].name:
        to_value = from_value * (365.0 * 24.0 * 60.0 * 60.0)
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_invtemp_to_base(from_value: float, from_unit: UnitTemp):
    if from_value == "":
        return from_value
    if from_unit.name == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif from_unit.name == UnitTemp["CELSIUS"].name:
        to_value = from_value
    elif from_unit.name == UnitTemp["FAHRENHEIT"].name:
        to_value = from_value * (1.0 / 0.5556)
    elif from_unit.name == UnitTemp["RANKINE"].name:
        to_value = from_value * (1.0 / 0.5556)
    else:
        raise Exception("Invalid temperature unit")

    print(
        f"{from_value} ({from_unit.name})^(-1) was converted to {to_value} (Kelvin)^(-1)."
    )
    return to_value


def convert_invtemp_from_base(from_value: float, to_unit: UnitTemp):
    if from_value == "":
        return from_value
    if to_unit.name == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif to_unit.name == UnitTemp["CELSIUS"].name:
        to_value = from_value
    elif to_unit.name == UnitTemp["FAHRENHEIT"].name:
        to_value = from_value * 0.5556
    elif to_unit.name == UnitTemp["RANKINE"].name:
        to_value = from_value * 0.5556
    else:
        raise Exception("Invalid temperature unit")

    print(
        f"{from_value} (Kelvin)^(-1) was converted to {to_value} ({to_unit.name})^(-1)."
    )

    return to_value
