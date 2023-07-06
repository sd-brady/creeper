import unittest

import src.frontend.modules.unit_system as unit_system


class TestTimeConversion(unittest.TestCase):
    def test_convert_time_to_seconds_from_seconds(self) -> None:
        from_seconds = 100.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_seconds, unit_system.UnitTime["SECONDS"]
        )
        self.assertAlmostEqual(from_seconds, to_seconds)
        return

    def test_convert_time_to_seconds_from_days(self) -> None:
        from_days = 1.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_days, unit_system.UnitTime["DAYS"]
        )
        self.assertAlmostEqual(86400.0, to_seconds)
        return

    def test_convert_time_to_seconds_from_years(self) -> None:
        from_years = 1.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_years, unit_system.UnitTime["YEARS"]
        )
        self.assertAlmostEqual(31536000.0, to_seconds)
        return

    def test_convert_time_from_seconds_to_seconds(self) -> None:
        from_seconds = 100.0  # seconds
        to_seconds = unit_system.convert_time_from_seconds(
            from_seconds, unit_system.UnitTime["SECONDS"]
        )
        self.assertAlmostEqual(from_seconds, to_seconds)

        return

    def test_convert_time_from_seconds_to_days(self) -> None:
        from_seconds = 86400.0  # seconds
        to_days = unit_system.convert_time_from_seconds(
            from_seconds, unit_system.UnitTime["DAYS"]
        )
        self.assertAlmostEqual(1.0, to_days)
        return

    def test_convert_time_from_seconds_to_years(self) -> None:
        from_seconds = 31536000.0  # seconds
        to_years = unit_system.convert_time_from_seconds(
            from_seconds, unit_system.UnitTime["YEARS"]
        )
        self.assertAlmostEqual(1.0, to_years)
        return


if __name__ == "__main__":
    unittest.main()
