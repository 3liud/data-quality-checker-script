import pandas as pd
import numpy as np
import sys
import os

class DataQualityChecker:
    def __init__(self, df, data_dict_df):
        self.df = df
        self.data_dict = data_dict_df

    def check_missing_data(self):
        missing_summary = self.df.isnull().mean() * 100
        missing_report = missing_summary = missing_summary[missing_summary > 0].sort_values(ascending=False)
        if missing_report.empty:
            print("✅ No Missing Data Detected.")
        else:
            print("⚠️ Missing Data Report (%):\n", missing_report)
        return missing_report

    def check_duplicates(self):
        duplicates = self.df[self.df.duplicated()]
        num_duplicates = duplicates.shape[0]
        if num_duplicates > 0:
            print(f"⚠️ Total Duplicate Rows: {num_duplicates}")
            print(duplicates.head())
        else:
            print("✅ No Duplicate Rows Found.")
        return duplicates

    def validate_data_types(self):
        incorrect_types = {}
        for _, row in self.data_dict.iterrows():
            col, expected_type = row['column_name'], row['data_type']
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                if expected_type == 'datetime':
                    if not pd.api.types.is_datetime64_any_dtype(self.df[col]):
                        incorrect_types[col] = {'expected': 'datetime', 'actual': actual_type}
                elif actual_type != expected_type:
                    incorrect_types[col] = {'expected': expected_type, 'actual': actual_type}

        if incorrect_types:
            print("⚠️ Data Type Mismatches Found:")
            for col, types in incorrect_types.items():
                print(f"  - {col}: Expected {types['expected']}, got {types['actual']}")
        else:
            print("✅ All column data types are correct.")
        return incorrect_types

    def validate_numeric_ranges(self):
        out_of_range = {}
        for _, row in self.data_dict.iterrows():
            col, min_val, max_val = row['column_name'], row['min_value'], row['max_value']
            if pd.notnull(min_val) and pd.notna(max_val) and col in self.df.columns:
                invalid = self.df[
                    (self.df[col] < min_val) | (self.df[col] > max_val)
                ]
                if not invalid.empty:
                    out_of_range[col] = invalid.shape[0]
                    print(f"⚠️ Column '{col}' has {invalid.shape[0]} values out of range [{min_val}, {max_val}]")
        if not out_of_range:
            print("✅ All numeric values within specified ranges.")
        return out_of_range

def load_data_dict(path='data_dictionary.csv'):
    if not os.path.exists(path):
        print(f"Data dictionary file '{path}' not found!")
        sys.exit(1)
    data_dict_df = pd.read_csv(path)
    data_dict_df['min_value'] = pd.to_numeric(data_dict_df.get('min_value', np.nan), errors='coerce')
    data_dict_df['max_value'] = pd.to_numeric(data_dict_df.get('max_value', np.nan), errors='coerce')
    return data_dict_df

def main():
    if len(sys.argv) != 2:
        print("Usage: python checker.py your_dataset.csv")
        sys.exit(1)

    dataset_path = sys.argv[1]

    if not os.path.exists(dataset_path):
        print(f"❌ File '{sys.argv[1]}' not found.")
        sys.exit(1)

    df = pd.read_csv(sys.argv[1])
    data_dict_df = load_data_dictionary()

    checker = DataQualityChecker(df, data_dict_df)
    print("\n--- Data Quality Check Results ---\n")
    checker.check_missing_data()
    checker.check_duplicates()
    checker.validate_data_types()
    checker.validate_numeric_ranges()


def load_data_dictionary(file_path='data_dictionary.csv'):
    if not os.path.exists(file_path):
        print(f"❌ Data dictionary file '{file_path}' not found!")
        sys.exit(1)
    return pd.read_csv(file_path)


if __name__ == "__main__":
    main()
