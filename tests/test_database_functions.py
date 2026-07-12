"""
Tests for importing CSV input files into the database.
"""

from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.import_csv_data import ImportCsvData


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILES_PATH = PROJECT_ROOT / "input"


@pytest.fixture
def import_csv_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ImportCsvData:
    """
    Create an ImportCsvData instance with an isolated test database.
    """
    database_path = tmp_path / "test_project.sqlite3"

    monkeypatch.setattr(ImportCsvData, "INPUTFILES_PATH", INPUT_FILES_PATH)

    repository = ImportCsvData(database_path=database_path)
    yield repository
    repository.close()


def assert_database_table_matches_csv(
    import_csv_data: ImportCsvData,
    csv_path: Path,
    table_name: str,
) -> None:
    """
    Assert that a database table contains the same data as a CSV file.
    """
    expected_dataframe = pd.read_csv(csv_path)
    expected_dataframe = expected_dataframe.sort_values(by="x").reset_index(drop=True)
    actual_dataframe = import_csv_data.read_table_by_name(table_name)

    assert_frame_equal(
        actual_dataframe,
        expected_dataframe,
        check_dtype=False,
    )


def test_load_all_inputs_stores_train_csv(
    import_csv_data: ImportCsvData,
) -> None:
    """
    Test that train CSV data is stored correctly.
    """
    import_csv_data.load_all_inputs()

    assert_database_table_matches_csv(
        import_csv_data=import_csv_data,
        csv_path=INPUT_FILES_PATH / "train.csv",
        table_name=ImportCsvData.TRAIN_TABLE_NAME,
    )


def test_load_all_inputs_stores_ideal_csv(
    import_csv_data: ImportCsvData,
) -> None:
    """
    Test that ideal CSV data is stored correctly.
    """
    import_csv_data.load_all_inputs()

    assert_database_table_matches_csv(
        import_csv_data=import_csv_data,
        csv_path=INPUT_FILES_PATH / "ideal.csv",
        table_name=ImportCsvData.IDEAL_TABLE_NAME,
    )


def test_load_all_inputs_stores_test_csv(
    import_csv_data: ImportCsvData,
) -> None:
    """
    Test that test CSV data is stored correctly.
    """
    import_csv_data.load_all_inputs()

    assert_database_table_matches_csv(
        import_csv_data=import_csv_data,
        csv_path=INPUT_FILES_PATH / "test.csv",
        table_name=ImportCsvData.TEST_TABLE_NAME,
    )