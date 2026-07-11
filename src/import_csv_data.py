from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import Column, Float, MetaData, Table

from src.sql_crud import SqlCrud


class ImportCsvData(SqlCrud):
    """
    Handle database operations for the assignment input datasets.

    The expected input files are:
    - 'train.csv' with one 'x' column and multiple training function columns.
    - 'ideal.csv' with one 'x' column and multiple ideal function columns.
    - 'test.csv' with one 'x' column and one function column

    Parameters
    ----------
    database_path:
        Path to the SQLite database file.
    """

    TRAIN_TABLE_NAME = "train_data"
    IDEAL_TABLE_NAME = "ideal_functions"
    TEST_TABLE_NAME = "test_data"
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATABASE_PATH = PROJECT_ROOT / "database" / "project.sqlite3"
    INPUTFILES_PATH = PROJECT_ROOT / "input"

    def __init__(self, database_path: str | Path=DATABASE_PATH) -> None:
        """
        Initialize the database.
        """
        super().__init__(database_path)

    def load_all_inputs(self) -> None:
        """
        Load all expected CSV input files into the database.

        Parameters
        ----------
        input_directory:
            Directory expected to contain 'train.csv', 'ideal.csv', and 'test.csv'.
        """

        self._load_data(self.TRAIN_TABLE_NAME, self.INPUTFILES_PATH / "train.csv")
        self._load_data(self.IDEAL_TABLE_NAME, self.INPUTFILES_PATH / "ideal.csv")
        self._load_data(self.TEST_TABLE_NAME, self.INPUTFILES_PATH / "test.csv")

    def _load_data(self, table_name: str, csv_path: str | Path) -> None:
        """
        Load test data from CSV into the database.

        Parameters
        ----------
        csv_path:
            Path to 'test.csv'.
        """
        dataframe = pd.read_csv(csv_path)
        table = self._create_numeric_table(table_name, dataframe)

        self.drop_table(table)
        self.create_table(table)
        self.insert_records(table, dataframe.to_dict(orient="records"))

    def _create_numeric_table(self, table_name: str, dataframe: pd.DataFrame) -> Table:
        """
        Create a SQLAlchemy table definition from numeric CSV columns.
        """
        metadata = MetaData()

        columns = []

        for column_name in dataframe.columns:
            columns.append(Column(column_name, Float, nullable=False))

        return Table(table_name, metadata, *columns)