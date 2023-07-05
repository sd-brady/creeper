from enum import Enum


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
