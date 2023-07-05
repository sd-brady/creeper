from enum import Enum

# TODO: Add unit tests for the unit conversion functions


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

    KELVIN = "K"
    CELSIUS = "\N{DEGREE SIGN}C"
    FAHRENHEIT = "\N{DEGREE SIGN}F"
    RANKINE = "R"


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


def convert_time_to_seconds(from_value: float, from_unit: UnitTime):
    if from_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif from_unit.name == UnitTime["DAYS"].name:
        to_value = from_value * 24.0 * 60.0 * 60.0
    elif from_unit.name == UnitTime["YEARS"].name:
        to_value = from_value * 365.0 * 24.0 * 60.0 * 60.0
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_time_from_seconds(from_value: float, to_unit: UnitTime):
    if to_unit.name == UnitTime["SECONDS"].name:
        to_value = from_value
    elif to_unit.name == UnitTime["DAYS"].name:
        to_value = from_value / (24.0 * 60.0 * 60.0)
    elif to_unit.name == UnitTime["YEARS"].name:
        to_value = from_value / (365.0 * 24.0 * 60.0 * 60.0)
    else:
        raise Exception("Invalid time unit.")
    return to_value


def convert_stress_to_mpa(from_value: float, from_unit: UnitStress):
    if from_unit.name == UnitStress["MPA"].name:
        to_value = from_value
    elif from_unit.name == UnitStress["PSI"]:
        to_value = from_value / 145.0377377
    else:
        raise Exception("Invalid stress unit.")
    return to_value


def convert_stress_from_mpa(from_value: float, to_unit: UnitStress):
    if to_unit.name == UnitStress["MPA"].name:
        to_value = from_value
    elif to_unit.name == UnitStress["PSI"].name:
        to_value = from_value * 145.0377377
    else:
        raise Exception("Invalid stress unit.")
    return to_value


def convert_temp_to_kelvin(from_value: float, from_unit: UnitTemp):
    if from_unit == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif from_unit == UnitTemp["CELSIUS"].name:
        to_value = from_value + 273.15
    elif from_unit == UnitTemp["FAHRENHEIT"].name:
        to_value = (from_value - 32) * (5.0 / 9.0) + 273.15
    elif from_unit == UnitTemp["RANKINE"].name:
        to_value = from_value * (5.0 / 9.0)
    else:
        raise Exception("Invalid temperature unit")
    return to_value


def convert_temp_from_kelvin(from_value: float, to_unit: UnitTemp):
    if to_unit == UnitTemp["KELVIN"].name:
        to_value = from_value
    elif to_unit == UnitTemp["CELSIUS"].name:
        to_value = from_value - 273.15
    elif to_unit == UnitTemp["FAHRENHEIT"].name:
        to_value = (from_value - 273.15) * (9.0 / 5.0) + 32
    elif to_unit == UnitTemp["RANKINE"].name:
        to_value = from_value / (5.0 / 9.0)
    else:
        raise Exception("Invalid temperature unit")
    return to_value
