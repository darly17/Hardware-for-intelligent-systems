from binary_translator import *

import unittest
import os
import coverage

# Настройка путей
test_loader = unittest.TestLoader()
test_suite = test_loader.discover(TEST_DIR, pattern='test_*.py')

# Запускаем тесты
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(test_suite)