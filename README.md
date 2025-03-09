# Data Quality Checker

A simple yet powerful Python-based data quality checking tool designed to automate common data quality validations on your datasets.

---

## Purpose:
This Python script automates the following data quality checks:

- **Missing Values Check**: Detects and reports the percentage of missing values per column.
- **Duplicate Rows Check**: Identifies duplicate rows within the dataset.
- **Data Types Validation**: Checks if the dataset columns match the expected data types defined in the data dictionary.
- **Numeric Range Validation**: Ensures numeric columns have values within the specified min and max ranges.

## Prerequisites

Make sure you have installed these Python packages:

```bash
pip install pandas numpy dash plotly
```

---

## Project Structure

```
project_name/
│
├── data/
│   ├── Students_Grading_Dataset.csv
│   └── data_dictionary.csv
│
├── quality_checker.py
├── dashboard.py
├── README.md
└── requirements.txt
```

---

## Files Required

- **Your Dataset** (`Students_Grading_Dataset.csv`)
- **Data Dictionary** (`data_dictionary.csv`): A CSV defining expected column metadata.

### Data Dictionary Format

The `data_dictionary.csv` should follow this structure:

| column_name | data_type | min_value | max_value |
|-------------|-----------|-----------|-----------|
| age         | int64     | 18        | 65        |
| salary      | float64   | 30000     | 200000    |
| join_date   | datetime  |           |           |

- Leave `min_value` and `max_value` empty for non-numeric fields.

---

## Running the Script

Open your terminal and run:

```bash
python quality_checker.py Students_Grading_Dataset.csv
```

Ensure you execute this command from the project's root directory.

---

## Launching the Dashboard

To run the interactive data quality dashboard, execute:

```bash
python dashboard.py
```

Then, open a browser and navigate to the provided local address (typically `http://127.0.0.1:8050`).

---

## Script Breakdown

### DataQualityChecker Class

- **`check_missing_data()`**
  - Reports columns with missing data and their percentages.

- **`check_duplicates()`**
  - Reports duplicate rows if present.

- **`validate_data_types()`**
  - Compares actual column data types against expected types from the data dictionary and reports mismatches.

- **`validate_numeric_ranges()`**
  - Reports numeric columns with values outside specified minimum and maximum ranges.

---

## Example Usage

```bash
python quality_checker.py Students_Grading_Dataset.csv
```

**Output Example:**
```
--- Data Quality Check Results ---

Missing Data Report (%):
Attendance (%)            10.32
Assignments_Avg           10.34
Parent_Education_Level    35.88

No Duplicate Rows Found.

Data Type Mismatches Found:
  - Age: Expected int64, got float64

Columns with out-of-range numeric values:
Attendance (%): 2
```

---

## Future Enhancements:
- Integration with interactive dashboards.
- Automated reporting (PDF/HTML reports).
- Logging for historical tracking of data quality issues.

Feel free to customize this script for your specific data needs!

---

## Author

Your Name  
Your Email  
Your LinkedIn or GitHub URL
