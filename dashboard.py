import os

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_dataset(filename):
    """
    Loads a dataset from a CSV file in the 'data' directory.

    Parameters
    ----------
    filename : str
        The name of the CSV file to load.

    Returns
    -------
    pd.DataFrame
        The loaded dataset as a Pandas DataFrame.
    """
    return pd.read_csv(os.path.join(BASE_DIR, "data", filename))


data = load_dataset("Students_Grading_Dataset.csv")
data_dict_df = load_dataset("data_dictionary.csv")

numeric_columns = data_dict_df[data_dict_df["data_type"].isin(["int64", "float64"])][
    "column_name"
]

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Dynamic Data Quality Dashboard"),
        dcc.Dropdown(
            id="column-dropdown",
            options=[{"label": col, "value": col} for col in numeric_columns],
            value=numeric_columns.iloc[0],
            clearable=False,
        ),
        dcc.Graph(id="numeric-distribution"),
        html.Div(id="missing-values"),
        html.Div(id="duplicates"),
    ]
)


@app.callback(
    Output("numeric-distribution", "figure"), Input("column-dropdown", "value")
)
def update_graph(column_name):
    """
    Updates the histogram figure for the numeric distribution based on the selected column.

    Parameters
    ----------
    column_name : str
        The name of the column to visualize in the histogram.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A Plotly figure object representing the histogram of the selected column.
    """

    fig = px.histogram(
        data_frame=data, x=column_name, title=f"Distribution of {column_name}"
    )
    return fig


@app.callback(
    Output("missing-values", "children"), Input("numeric-distribution", "figure")
)
def update_missing_values(_):
    """
    Updates the missing values count based on the input data.

    Parameters
    ----------
    _ : unused input (the figure from the numeric distribution graph)

    Returns
    -------
    html.Ul or str
        A list of all columns with missing values and their percentage of missing values,
        or a string saying "No missing data!" if there are no missing values.
    """
    missing_report = data.isnull().mean() * 100
    missing_report = missing_report[missing_report > 0].round(2)
    if missing_report.empty:
        return "No missing data!"
    return html.Ul(
        [html.Li(f"{col}: {val}% missing") for col, val in missing_report.items()]
    )


@app.callback(Output("duplicates", "children"), Input("numeric-distribution", "figure"))
def update_duplicates(_):
    """
    Updates the duplicates count based on the input data.

    Parameters
    ----------
    _

    Returns
    -------
    str
        The number of duplicate rows in the dataset, or a message indicating that there are no duplicates.
    """
    num_duplicates = data.duplicated().sum()
    return (
        f"Total Duplicate Rows: {num_duplicates}"
        if num_duplicates
        else "No duplicate rows found."
    )


if __name__ == "__main__":
    app.run_server(debug=True)
