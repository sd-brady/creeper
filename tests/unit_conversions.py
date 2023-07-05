import unittest

import src.frontend.modules.unit_system as unit_system


class TestTimeConversion(unittest.TestCase):
    def test_seconds_to_seconds(self) -> None:
        from_seconds = 100.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_seconds, unit_system.UnitTime["SECONDS"]
        )
        self.assertAlmostEqual(from_seconds, to_seconds)
        return

    def test_days_to_seconds(self) -> None:
        from_days = 1.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_days, unit_system.UnitTime["DAYS"]
        )
        self.assertAlmostEqual(86400.0, to_seconds)
        return

    def test_years_to_seconds(self) -> None:
        from_years = 1.0
        to_seconds = unit_system.convert_time_to_seconds(
            from_years, unit_system.UnitTime["YEARS"]
        )
        self.assertAlmostEqual(31536000.0, to_seconds)
        return


if __name__ == "__main__":
    unittest.main()
