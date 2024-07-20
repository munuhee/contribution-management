import os

# Define the paths to the test files
test_files = [
    "members/tests.py",
    "cases/tests.py",
    "penalties/tests.py",
    "mpesa/tests.py",
    "transactions/tests.py",
    "notifications/tests.py",
]

if __name__ == "__main__":
    # Run pytest on the specified test files
    pytest_args = " ".join(test_files)
    os.system(f"pytest {pytest_args}")
