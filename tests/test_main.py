import unittest
from main import py_modbus

class TestMain(unittest.TestCase):
    def test_py_modbus(self):
        # Act
        result = py_modbus()

        # Assert
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
