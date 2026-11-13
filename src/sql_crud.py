from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, delete, insert, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.sql.elements import ColumnElement

from src.constants import PATHS



class SqlCrud:
    """
    Wrapper class providing generic CRUD operations for SQL databases.

    Parameters
    ----------
    database_path:
        Path to the SQLite database file.
        To retrieve the project root folder use:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        (assuming the module lays under "project_root/src/module")
    """

    def __init__(self, database_path: str | Path) -> None:
        """
        Initialize the database engine and metadata container.
        """
        
        self.database_path = Path(database_path)
        self.engine: Engine = create_engine(f"sqlite:///{self.database_path}")
        self.metadata = MetaData()

    def create_table(self, table: Table) -> None:
        """
        Create a database table if it does not already exist.

        Parameters
        ----------
        table:
            SQLAlchemy table definition to create.
        """
        table.create(bind=self.engine, checkfirst=True)

    def drop_table(self, table: Table) -> None:
        """
        Drop a database table if it exists.

        Parameters
        ----------
        table:
            SQLAlchemy table definition to drop.
        """
        table.drop(bind=self.engine, checkfirst=True)

    def insert_records(self, table: Table, records: list[dict[str, Any]]) -> None:
        """
        Insert multiple records into a table.

        Parameters
        ----------
        table:
            Target database table.
        records:
            Records to insert as dictionaries.
        """
        if not records:
            return

        with self.engine.begin() as connection:
            connection.execute(insert(table), records)

    def get_table(self, table_name: str) -> Table:
        """
        Get an existing database table by name.

        Parameters
        ----------
        table_name:
            Name of the database table.

        Returns
        -------
        sqlalchemy.Table
            Reflected SQLAlchemy table object.  
        """
        metadata = MetaData()
        return Table(table_name, metadata, autoload_with=self.engine)

    def update_records(
        self,
        table: Table,
        values: dict[str, Any],
        condition: ColumnElement[bool],
    ) -> None:
        """
        Update records matching a condition.

        Parameters
        ----------
        table:
            Target database table.
        values:
            Column values to update.   
        condition:
            SQLAlchemy condition selecting affected rows.
        """
        statement = update(table).where(condition).values(**values)

        with self.engine.begin() as connection:
            connection.execute(statement)

    def delete_records(self, table: Table, condition: ColumnElement[bool]) -> None:
        """
        Delete records matching a condition.

        Parameters
        ----------
        table:
            Target database table.    
        condition:
            SQLAlchemy condition selecting affected rows.
        """
        statement = delete(table).where(condition)

        with self.engine.begin() as connection:
            connection.execute(statement)

    def read_table(self, table: Table) -> pd.DataFrame:
        """
        Read all rows from a table into a pandas DataFrame.
        """
        statement = select(table)

        with self.engine.connect() as connection:
            return pd.read_sql(statement, connection)
        
    def read_table_by_name(self, table_name: str) -> pd.DataFrame:
        table = self.get_table(table_name)
        return self.read_table(table)
    
    def close(self) -> None:
        """
        Close all pooled database connections.
        """
        self.engine.dispose()
