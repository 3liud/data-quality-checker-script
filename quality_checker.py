import os
import sys

import numpy as np
import pandas as pd


class DataQualityChecker:
    def __init__(self, df, data_dict_df):
        """
        Initializes the DataQualityChecker with the given dataset and data
        dictionary.

        Parameters:
        df (pd.DataFrame): The dataset to be checked for quality issues.
        data_dict_df (pd.DataFrame): The data dictionary containing metadata
        such as column names, expected data types, and numeric ranges
        for validation.
        """

        self.df = df
        self.data_dict = data_dict_df

    def _generate_report(self, report, message):
        if report.empty:
            print(message)
        else:
            print(f"⚠️ {message}:\n", report)

    def check_missing_data(self):
        """
        Checks the dataset for missing values and generates a report of the
        percentage of missing values in each column.

        Returns:
        pd.Series: A Series containing the percentage of missing values in
        each column.
        """
        missing_summary = self.df.isnull().mean() * 100
        missing_report = missing_summary[missing_summary > 0].sort_values(
            ascending=False
        )
        self._generate_report(missing_report, "Missing Data Report (%)")
        return missing_report

    def check_duplicates(self):
        """
        Checks the dataset for duplicate rows and generates a report of the
        first few duplicate rows.

        Returns:
        pd.DataFrame: A DataFrame containing the duplicate rows.
        """
        duplicates = self.df[self.df.duplicated()]
        num_duplicates = duplicates.shape[0]
        if num_duplicates > 0:
            print(f"⚠️ Total Duplicate Rows: {num_duplicates}")
            print(duplicates.head())
        else:
            self._generate_report(duplicates, "No Duplicate Rows Found.")
        return duplicates

    def validate_data_types(self):
        """
        Checks the dataset for columns with data types that do not match the
        expected data type in the data dictionary.

        Iterates over each column in the data dictionary, checking if the
        data type of the column in the dataset matches the expected data type.
        If any mismatches are found, the function logs the column name,
        expected data type, and actual data type.

        Returns:
        dict: A dictionary where keys are column names with mismatched data
        types, and values are dictionaries containing the expected and actual
        data types.
        """
        incorrect_types = {}
        for _, row in self.data_dict.iterrows():
            col, expected_type = row["column_name"], row["data_type"]
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                if expected_type == "datetime":
                    if not pd.api.types.is_datetime64_any_dtype(self.df[col]):
                        incorrect_types[col] = {
                            "expected": "datetime",
                            "actual": actual_type,
                        }
                elif actual_type != expected_type:
                    incorrect_types[col] = {
                        "expected": expected_type,
                        "actual": actual_type,
                    }

        if incorrect_types:
            print("⚠️ Data Type Mismatches Found:")
            for col, types in incorrect_types.items():
                print(f"  - {col}: Expected {types['expected']}, got {types['actual']}")
        else:
            print("All column data types are correct.")
        return incorrect_types

    def validate_numeric_ranges(self):
        """
        Validates that numeric values in the dataset fall within the specified
        minimum and maximum ranges as defined in the data dictionary.

        Iterates over each column defined in the data dictionary, checking if
        numeric values in the dataset are within the specified range. If any
        values are found outside the range, the function logs the column name
        and the count of out-of-range values.

        Returns:
        dict: A dictionary where keys are column names with out-of-range values,
        and values are the counts of such values.
        """

        out_of_range_values = {}
        for _, row in self.data_dict.iterrows():
            column_name = row["column_name"]
            min_value = row["min_value"]
            max_value = row["max_value"]

            if (
                pd.notnull(min_value)
                and pd.notnull(max_value)
                and column_name in self.df.columns
            ):
                invalid_values = self.df[
                    (self.df[column_name] < min_value)
                    | (self.df[column_name] > max_value)
                ]

                if not invalid_values.empty:
                    num_invalid_values = invalid_values.shape[0]
                    out_of_range_values[column_name] = num_invalid_values

        if out_of_range_values:
            print("⚠️ Columns with out-of-range numeric values:")
            for col, count in out_of_range_values.items():
                print(f"  - {col}: {count} out-of-range values")
        else:
            print("All numeric values within specified ranges.")
        return out_of_range_values

    def load_data_dict(path="data_dictionary.csv"):
        """
        Loads a data dictionary from the specified CSV file and returns it as a DataFrame.

        The data dictionary should contain the following columns:
        - column_name: The name of the column to be checked.
        - data_type: The expected data type for the column. Can be one of:
            - datetime
            - numeric (int or float)
            - string
        - min_value: The minimum allowed value for the column. Ignored if data_type is not numeric.
        - max_value: The maximum allowed value for the column. Ignored if data_type is not numeric.

        If the data dictionary file does not exist, an error message is printed and the program exits.

        Parameters:
        path (str): Path to the CSV file containing the data dictionary. Defaults to 'data_dictionary.csv'.

        Returns:
        pd.DataFrame: The data dictionary as a DataFrame.
        """
        if not os.path.exists(path):
            print(f"Data dictionary file '{path}' not found!")
            sys.exit(1)
        data_dict_df = pd.read_csv(path)
        data_dict_df["min_value"] = pd.to_numeric(
            data_dict_df.get("min_value", np.nan), errors="coerce"
        )
        data_dict_df["max_value"] = pd.to_numeric(
            data_dict_df.get("max_value", np.nan), errors="coerce"
        )
        return data_dict_df


def main():
    """
    Main function to run the data quality checks on a dataset.

    The script expects a single command-line argument specifying the path to the
    dataset CSV file. It loads the dataset and a data dictionary, then performs
    various data quality checks including missing data, duplicate rows, data type
    mismatches, and numeric range violations. The results are printed to the console.

    Usage:
    python qualityChecker.py your_dataset.csv

    Raises:
    SystemExit: If incorrect number of arguments is provided or if the dataset file
    does not exist.
    """

    if len(sys.argv) != 2:
        print("Usage: python qualityChecker.py your_dataset.csv")
        sys.exit(1)

    dataset_path = os.path.join("data", sys.argv[1])

    if not os.path.exists(dataset_path):
        print(f"File '{dataset_path}' not found.")
        sys.exit(1)

    df = pd.read_csv(dataset_path)
    data_dict_df = load_data_dictionary()

    checker = DataQualityChecker(df, data_dict_df)
    print("\n--- Data Quality Check Results ---\n")
    checker.check_missing_data()
    checker.check_duplicates()
    checker.validate_data_types()
    checker.validate_numeric_ranges()


def load_data_dictionary(file_path="data/data_dictionary.csv"):
    """
    Loads a data dictionary from the specified CSV file and returns it as a DataFrame.

    The data dictionary should contain the following columns:
    - column_name: The name of the column to be checked.
    - data_type: The expected data type for the column. Can be one of:
        - datetime
        - numeric (int or float)
        - string
    - min_value: The minimum allowed value for the column. Ignored if data_type is not numeric.
    - max_value: The maximum allowed value for the column. Ignored if data_type is not numeric.

    If the data dictionary file does not exist, an error message is printed and the program exits.

    Parameters:
    file_path (str): Path to the CSV file containing the data dictionary. Defaults to 'data_dictionary.csv'.

    Returns:
    pd.DataFrame: The data dictionary as a DataFrame.
    """
    if not os.path.exists(file_path):
        print(f"Data dictionary file '{file_path}' not found!")
        sys.exit(1)
    data_dict_df = pd.read_csv(file_path)
    data_dict_df["min_value"] = pd.to_numeric(
        data_dict_df.get("min_value", np.nan), errors="coerce"
    )
    data_dict_df["max_value"] = pd.to_numeric(
        data_dict_df.get("max_value", np.nan), errors="coerce"
    )
    return data_dict_df


if __name__ == "__main__":
    main()
