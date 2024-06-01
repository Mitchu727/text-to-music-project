import pytest
import os

from src.utils import get_project_root

def output_test_directory():
    return get_project_root() / "test" / "outputs"

def remove_all_files_from_directory(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


@pytest.fixture()
def clean_outputs():
    # remove_all_files_from_directory(output_test_directory())
    yield
    # remove_all_files_from_directory(output_test_directory())
