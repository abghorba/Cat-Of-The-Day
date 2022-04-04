import logging
import pytest

logging.basicConfig(filename='logs/unittests.log', encoding='utf-8', level=logging.INFO)
pytest.main(["tests/unit_tests.py"])