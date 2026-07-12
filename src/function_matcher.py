"""Match training and test data to ideal functions."""

from __future__ import annotations

from math import sqrt
from typing import Any

from src.import_csv_data import ImportCsvData
from src.data_visualizer import DataVisualizer

import pandas as pd


class FunctionMatcher:
    """
    Match training functions and test data to ideal functions.
    """
    def __init__(self, db: ImportCsvData, visualizer: DataVisualizer):
        self.db = db
        self.visualizer = visualizer

    def select_best_ideal_functions(
        self,
        train_data: pd.DataFrame,
        ideal_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Find the best matching ideal function for each training function.
        """
        train_data = self._prepare_function_data(train_data)
        ideal_data = self._prepare_function_data(ideal_data)

        training_columns = self._get_y_columns(train_data)
        ideal_columns = self._get_y_columns(ideal_data)

        results = []

        for training_column in training_columns:
            best_match = self._find_best_ideal_for_training_column(
                train_data=train_data,
                ideal_data=ideal_data,
                training_column=training_column,
                ideal_columns=ideal_columns,
            )
            results.append(best_match)

        return pd.DataFrame(results)

    def match_test_data(
        self,
        test_data: pd.DataFrame,
        ideal_data: pd.DataFrame,
        selected_functions: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Match each test point to the best selected ideal function.
        """
        test_data = test_data.copy()
        test_data["x"] = pd.to_numeric(test_data["x"])
        test_data["y"] = pd.to_numeric(test_data["y"])

        ideal_data = self._prepare_function_data(ideal_data)

        results = []

        for _, test_row in test_data.iterrows():
            match = self._match_single_test_point(
                test_x=float(test_row["x"]),
                test_y=float(test_row["y"]),
                ideal_data=ideal_data,
                selected_functions=selected_functions,
            )

            if match is not None:
                results.append(match)

        return pd.DataFrame(
            results,
            columns=["x", "y", "delta_y", "ideal_function"],
        )

    def _find_best_ideal_for_training_column(
        self,
        train_data: pd.DataFrame,
        ideal_data: pd.DataFrame,
        training_column: str,
        ideal_columns: list[str],
    ) -> dict[str, Any]:
        """
        Find the ideal function with the lowest squared error.
        """
        best_ideal_function = ""
        best_squared_error = float("inf")
        best_max_deviation = float("inf")

        for ideal_column in ideal_columns:
            delta = train_data[training_column] - ideal_data[ideal_column]
            squared_error = float((delta**2).sum())

            if squared_error < best_squared_error:
                best_ideal_function = ideal_column
                best_squared_error = squared_error
                best_max_deviation = float(delta.abs().max())

        return {
            "training_function": training_column,
            "ideal_function": best_ideal_function,
            "squared_error": best_squared_error,
            "max_deviation": best_max_deviation,
        }

    def _match_single_test_point(
        self,
        test_x: float,
        test_y: float,
        ideal_data: pd.DataFrame,
        selected_functions: pd.DataFrame,
    ) -> dict[str, Any] | None:
        """
        Match one test point to the best selected ideal function.
        """

        if test_x not in ideal_data.index:            
            return None

        best_match = None
        best_delta_y = float("inf")

        for _, selected_function in selected_functions.iterrows():
            ideal_function = selected_function["ideal_function"]
            ideal_y = ideal_data.loc[test_x, ideal_function]
            delta_y = abs(float(ideal_y) - test_y)

            max_allowed_delta = sqrt(2) * selected_function["max_deviation"]

            if delta_y <= max_allowed_delta and delta_y < best_delta_y:
                best_delta_y = delta_y
                best_match = {
                    "x": test_x,
                    "y": test_y,
                    "delta_y": delta_y,
                    "ideal_function": ideal_function,
                }

        return best_match

    def _prepare_function_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare function data by sorting it and using x as index.
        """
        dataframe = dataframe.copy()

        dataframe["x"] = pd.to_numeric(dataframe["x"])

        for column in self._get_y_columns(dataframe):
            dataframe[column] = pd.to_numeric(dataframe[column])

        return dataframe.sort_values("x").set_index("x")

    def _get_y_columns(self, dataframe: pd.DataFrame) -> list[str]:
        """
        Return all y columns from a DataFrame.
        """
        return [
            column
            for column in dataframe.columns
            if column not in {"id", "x"}
        ]