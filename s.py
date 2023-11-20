import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from typing import Any, Dict

class Logger:
    def __init__(self):
        self.log = []

    def log_entry(self, timestamp: Any, interaction: str, **kwargs: Any) -> None:
        """
        Logs an interaction with additional key-value pairs.

        :param timestamp: The timestamp of the interaction.
        :param interaction: Description of the interaction.
        :param kwargs: Additional key-value pairs relevant to the interaction.
        """
        entry = {'Timestamp': timestamp, 'Interaction': interaction, **kwargs}
        self.log.append(entry)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the log entries to a pandas DataFrame.

        :return: DataFrame of log entries.
        """
        return pd.DataFrame(self.log)

    def print_table(self) -> None:
        """
        Prints the log entries in a table format.
        """
        df = self.to_dataframe()
        print(df)

    def visualize(self, x_col: str, y_col: str, title: str, kind: str = 'line') -> None:
        """
        Visualizes the log data.

        :param x_col: The column to use for the x-axis.
        :param y_col: The column to use for the y-axis.
        :param title: The title of the visualization.
        :param kind: The kind of plot (e.g., 'line', 'scatter').
        """
        df = self.to_dataframe()

        if kind == 'line':
            plt.plot(df[x_col], df[y_col], '-o')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(title)
            plt.grid(True)
            plt.show()
        elif kind == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, color=y_col)
            fig.show()
        else:
            print(f"Visualization kind '{kind}' not supported.")

# Example usage
logger = Logger()
logger.log_entry("2023-01-01 10:00", "Started Process", Process="Cutting", Department="Manufacturing")
logger.log_entry("2023-01-01 10:05", "Completed Process", Process="Cutting", Department="Manufacturing")
logger.print_table()
logger.visualize(x_col='Timestamp', y_col='Process', title='Process Timeline', kind='line')
