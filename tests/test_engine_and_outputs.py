"""Contract tests for removal of numeric-delta environmental scoring."""
import unittest
from core.cvss_environmental_engine import calculate


class TestEnvironmentalAdapterContract(unittest.TestCase):
    def test_numeric_only_input_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate({"base_score": "9.8"})

    def test_v3_vector_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate({"cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"})


if __name__ == "__main__":
    unittest.main()
