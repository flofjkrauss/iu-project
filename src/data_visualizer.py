"""Bokeh-based visualization helpers for database table data."""

from __future__ import annotations

import pandas as pd
from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.layouts import gridplot, row, column
from bokeh.models import Div
from pathlib import Path

from src.constants import PATHS, VALID_PLOT_OUTPUT_OPTIONS
from exceptions.VisualizerExceptions import InvalidPlotOutputOptions

class DataVisualizer:
    """
    Create Bokeh plots from pandas DataFrames.
    """

    def __init__(self) -> None:
        """
        Initialize the visualizer.
        """
        if not Path(PATHS["visualization"]).is_dir():
            vis_folder = Path(PATHS["visualization"])
            vis_folder.mkdir()

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
        y_columns = []
        for col in dataframe.columns:
            if col != x_column:
                y_columns.append(col)
        
        for y_column in y_columns:
            self.xy_plot(
                dataframe=dataframe,
                table_name=table_name,
                x_column=x_column,
                y_column=y_column,
                output="save"
            )

    def xy_plot(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        x_column: str,
        y_column: str,
        output: str,
    ) -> None:
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
        output:
            Possible options: "show", "save" or "both"
        """
        plot = self._create_xy_plot(
            dataframe=dataframe,
            title=f"{table_name}: {x_column} / {y_column}",
            x_column=x_column,
            y_column=y_column,
        )

        file_path = PATHS["visualization"] / f"{table_name}_{y_column}.html"
        output_file(file_path)
        if output == "save" or output == "both":
            save(plot)
        if output == "show" or output == "both":
            show(plot)
        if output not in VALID_PLOT_OUTPUT_OPTIONS:
            raise InvalidPlotOutputOptions

        return None

    def _create_xy_plot(
        self,
        dataframe: pd.DataFrame,
        title: str,
        x_column: str,
        y_column: str,
        width: int = 900,
        height: int = 500
    ):
        """
        Create a Bokeh figure for one x/y column pair.
        """
        plot = figure(
            title=title,
            x_axis_label=x_column,
            y_axis_label=y_column,
            width=width,
            height=height,
        )

        plot.line(
            dataframe[x_column],
            dataframe[y_column],
            line_width=2,
            legend_label=y_column,
        )

        plot.scatter(
            dataframe[x_column],
            dataframe[y_column],
            size=4,
            alpha=0.5,
            marker="circle"
        )        

        plot.legend.location = "top_left"

        return plot
    
    def table_grid_plot(
    self,
    dataframe: pd.DataFrame,
    table_name: str,
    x_column: str = "x",
    plots_per_row: int = 4,
    ) -> None:
        """
        Save/Show all y-columns of one table as separate plots in one HTML file.
        """
        y_columns = []
        for col in dataframe.columns:
            if col != x_column:
                y_columns.append(col)
        
        plots = []

        for y_column in y_columns:
            plot = self._create_xy_plot(
                dataframe=dataframe,
                title=table_name,
                x_column=x_column,
                y_column=y_column,
                width=450,
                height=300
            )
            plots.append(plot)

        grid = gridplot(plots, ncols=plots_per_row)

        file_path = PATHS["visualization"] / f"{table_name}_grid.html"
        output_file(file_path)
        save(grid)
        show(grid)

        return None
    
    def selection_grid_plot(
        self,
        selection: pd.DataFrame,
        train_data: pd.DataFrame,
        ideal_data:pd.DataFrame        
        ) -> None:
            """
            Save/Show all train-ideal function pairs in one grid plot
            """
                
            rows=[]

            for _, data_row in selection.iterrows():                
                y_train = data_row["training_function"]
                y_ideal = data_row["ideal_function"]
                layout_row = []
                train_plot = self._create_xy_plot(train_data,
                                            f"train_{data_row["training_function"]}",
                                            x_column="x",
                                            y_column=y_train,
                                            width=450,
                                            height=300
                                            )
                layout_row.append(train_plot)
                ideal_plot = self._create_xy_plot(ideal_data,
                                            f"ideal_{data_row["ideal_function"]}",
                                            x_column="x",
                                            y_column=y_ideal,
                                            width=450,
                                            height=300
                                            )
                layout_row.append(ideal_plot)

                description = Div(
                    text=f"""<h3>Squared Error and max. deviation</h3>
                        <p>{data_row["squared_error"], data_row["max_deviation"]}</p>""",
                    width=300
                    )
                layout_row.append(description)
                rows.append(row(layout_row))

            

            layout = column(*rows)
            file_path = PATHS["visualization"] / "selection_grid.html"
            output_file(file_path)
            save(layout)
            show(layout)

            return None
