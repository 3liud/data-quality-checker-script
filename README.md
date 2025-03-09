# Data Quality Checker

A simple yet Python-based data quality checking tool designed to automate common data quality validations on your datasets.

---

## **Purpose:**
This Python script automates the following data quality checks:

- **Missing Values Check**: Detects and reports the percentage of missing values per column.
- **Duplicate Rows Check**: Identifies duplicate rows within the dataset.
- **Data Types Validation**: Checks if the dataset columns match the expected data types defined in the data dictionary.
- **Numeric Range Validation**: Ensures numeric columns have values within the specified min and max ranges.

## **Prerequisites**

Make sure you have installed these Python packages:

```bash
pip install pandas numpy
```

---

## **Files Required**

- **Your Dataset** (`your_dataset.csv`)
- **Data Dictionary** (`data_dictionary.csv`): A CSV defining expected column metadata.

### **Data Dictionary Format**

The `data_dictionary.csv` should follow this structure:

| column_name | data_type | min_value | max_value |
|-------------|-----------|-----------|-----------|
| age         | int64     | 18        | 65        |
| salary      | float64   | 30000     | 200000    |
| join_date   | datetime  |           |           |

- Leave `min_value` and `max_value` empty for non-numeric fields.

---

## **Running the Script**

Open your terminal and run:

```bash
python checker.py your_dataset.csv
```

Ensure `checker.py`, `your_dataset.csv`, and `data_dictionary.csv` are in the same directory or specify the full paths accordingly.

---

## **Script Breakdown**

### **DataQualityChecker Class**

- **`check_missing_data()`**
  - Reports columns with missing data and their percentages.

- **`check_duplicates()`**
  - Reports duplicate rows if present.

- **`validate_data_types()`**
  - Compares actual column data types against expected types from the data dictionary and reports mismatches.

- **`validate_numeric_ranges()`**
  - Reports numeric columns with values outside specified minimum and maximum ranges.

---

## **Example Usage**

```bash
python checker.py Students_Grading_Dataset.csv
```

**Output Example:**
```
--- Data Quality Check Results ---

⚠️ Missing Data Report (%):
Attendance (%)            10.32
Assignments_Avg           10.34
Parent_Education_Level    35.88

No Duplicate Rows Found.

⚠️ Data Type Mismatches Found:
  - Age: Expected int64, got float64

⚠️ Columns with out-of-range numeric values:
Attendance (%): 2
```

---

## **Future Enhancements:**
- Integration with interactive dashboards.
- Automated reporting (PDF/HTML reports).
- Logging for historical tracking of data quality issues.

Feel free to customize this script for your specific data needs!

---
