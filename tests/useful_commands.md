# pytest tests/ --cov=dev --cov-report=term-missing -v

    Runs test suite with coverage reporting:
    - `pytest tests/`: Executes all tests in the tests/ directory
    - `--cov=dev`: Measures code coverage for the dev package
    - `--cov-report=term-missing`: Shows coverage report in terminal with uncovered lines
    - `-v`: Provides verbose output showing individual test cases