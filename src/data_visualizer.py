"""Bokeh-based visualization helpers for database table data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.layouts import gridplot



class DataVisualizer:
    """
    Create Bokeh plots from pandas DataFrames.

    Parameters
    ----------
    output_directory:
        Directory where generated plot files should be stored.
    """

    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    OUTPUT_PATH = PROJECT_ROOT / "visualizations"

    def __init__(self, output_directory: str | Path=OUTPUT_PATH) -> None:
        """
        Initialize the visualizer.
        """
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def save_all_xy_plots(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        x_column: str = "x",
    ) -> None:
        """
        Save one HTML plot for every y-column in a DataFrame.

        Parameters
        ----------
        dataframe:
            Source data containing one x-column and one or more y-columns.
        table_name:
            Name used as prefix for generated plot files.
        x_column:
            Name of the x-axis column.
        """
        y_columns = [
            column
            for column in dataframe.columns
            if column != x_column
        ]

        for y_column in y_columns:
            self.save_xy_plot(
                dataframe=dataframe,
                table_name=table_name,
                x_column=x_column,
                y_column=y_column,
            )

    def save_xy_plot(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        x_column: str,
        y_column: str,
    ) -> Path:
        """
        Save a single x/y plot as an HTML file.

        Parameters
        ----------
        dataframe:
            Source data.
        table_name:
            Name used as prefix for the generated plot file.
        x_column:
            Name of the x-axis column.
        y_column:
            Name of the y-axis column.

        Returns
        -------
        pathlib.Path
            Path to the generated HTML file.
        """
        plot = self._create_xy_plot(
            dataframe=dataframe,
            title=f"{table_name}: {x_column} / {y_column}",
            x_column=x_column,
            y_column=y_column,
        )

        file_path = self.output_directory / f"{table_name}_{y_column}.html"
        output_file(file_path)
        save(plot)

        return file_path

    def show_xy_plot(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        x_column: str,
        y_column: str,
    ) -> None:
        """
        Show a single x/y plot directly in the browser.
        """
        plot = self._create_xy_plot(
            dataframe=dataframe,
            title=f"{table_name}: {x_column} / {y_column}",
            x_column=x_column,
            y_column=y_column,
        )

        show(plot)

    def _create_xy_plot(
        self,
        dataframe: pd.DataFrame,
        title: str,
        x_column: str,
        y_column: str,
    ):
        """
        Create a Bokeh figure for one x/y column pair.
        """
        plot = figure(
            title=title,
            x_axis_label=x_column,
            y_axis_label=y_column,
            width=900,
            height=500,
        )

        plot.line(
            dataframe[x_column],
            dataframe[y_column],
            line_width=2,
            legend_label=y_column,
        )

        plot.circle(
            dataframe[x_column],
            dataframe[y_column],
            size=4,
            alpha=0.5,
        )

        plot.legend.location = "top_left"

        return plot
    
    def save_table_grid_plot(
    self,
    dataframe: pd.DataFrame,
    table_name: str,
    x_column: str = "x",
    plots_per_row: int = 4,
    ) -> Path:
        """
        Save all y-columns of one table as separate plots in one HTML file.
        """
        y_columns = [
            column
            for column in dataframe.columns
            if column not in {"id", x_column}
        ]

        plots = []

        for y_column in y_columns:
            plot = figure(
                title=f"{table_name}: {x_column} / {y_column}",
                x_axis_label=x_column,
                y_axis_label=y_column,
                width=450,
                height=300,
            )

            plot.line(
                dataframe[x_column],
                dataframe[y_column],
                line_width=2,
            )

            plot.scatter(
                dataframe[x_column],
                dataframe[y_column],
                size=3,
                alpha=0.4,
            )

            plots.append(plot)

        grid = gridplot(plots, ncols=plots_per_row)

        file_path = self.output_directory / f"{table_name}_grid.html"
        output_file(file_path)
        save(grid)

        return file_path
