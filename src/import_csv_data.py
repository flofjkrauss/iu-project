from __future__ import annotations
from pathlib import Path
import pandas as pd
from sqlalchemy import Column, Float, MetaData, Table, String
from src.sql_crud import SqlCrud
from src.constants import PATHS, TABLE_NAMES


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

    def __init__(self, database_path: str | Path=PATHS["db"]) -> None:
        """
        Initialize the database.
        """
        if not Path(PATHS["db_folder"]).is_dir():
            db_folder = Path(PATHS["db_folder"])
            db_folder.mkdir()
        super().__init__(database_path)

    def load_all_inputs(self) -> None:
        """
        Load all expected CSV input files into the database.
        """

        self._load_data(TABLE_NAMES["train"], PATHS["input"] / "train.csv")
        self._load_data(TABLE_NAMES["ideal"], PATHS["input"] / "ideal.csv")
        self._load_data(TABLE_NAMES["test"], PATHS["input"] / "test.csv")

    def _load_data(self, table_name: str, csv_path: str | Path) -> None:
        """
        Load test data from CSV into the database.

        Parameters
        ----------
        csv_path:
            Path to CSV file
        """
        dataframe = pd.read_csv(csv_path)
        dataframe = dataframe.sort_values(by="x").reset_index(drop=True)
        table = self._create_numeric_table(table_name, dataframe)

        self.drop_table(table)
        self.create_table(table)
        self.insert_records(table, dataframe.to_dict(orient="records"))

    def _create_numeric_table(self, table_name: str, dataframe: pd.DataFrame) -> Table:
        """
        Create a SQLAlchemy table definition from numeric dataframe
        """
        metadata = MetaData()
        columns = []

        for column_name in dataframe.columns:
            columns.append(Column(column_name, Float, nullable=False))

        return Table(table_name, metadata, *columns)
    
    def _create_selection_table(self, dataframe: pd.DataFrame, table_name: str) -> Table:
        """
        Create a SQLAlchemy table definition from dataframe
        """
        metadata = MetaData()
        columns = []

        for column_name in dataframe.columns:
            if "function" in column_name:
                columns.append(Column(column_name, String, nullable=False))
            else:
                columns.append(Column(column_name, Float, nullable=False))

        return Table(table_name, metadata, *columns)
    
    def insert_selection(self, table_name: str, dataframe: pd.DataFrame) -> None:
            """
            Insert function selection into database

            Parameters
            ----------
            table_name:
                table name
            dataframe:
                selected best ideal functions.
            """
            table = self._create_selection_table(table_name=table_name, dataframe=dataframe)

            self.drop_table(table)
            self.create_table(table)
            self.insert_records(table, dataframe.to_dict(orient="records"))