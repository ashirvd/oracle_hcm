import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def filter_all_employees_by_grade_change():
    try:
        # Load the CSV file
        csv_data = pd.read_excel(file_path)  # Try different encodings if necessary

        # Get the total number of rows
        total_rows = csv_data.shape[0]
        print(f'Total number of employee records in the CSV file: {total_rows}')

        # Check if the 'Joining Date' column exists
        if 'Grade Change Date' in csv_data.columns:
            grade_change_record = csv_data['Grade Change Date'].notna().sum()
            print(f'Total number of employees with promotions: {grade_change_record}')
        else:
            print('The "Grade Change Date" column is not found in the CSV file.')

    except Exception as e:
         print(f'An error occurred: {e}')

import pandas as pd

def filter_employees_by_grade_change(df, year=None, month=None, quarter=None):
    """
    Filters the employee records based on Grade Change Date for the specified year, month, or quarter.
    If all parameters are None, it will return records with non-null Grade Change Date.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing employee data.
    - year (int, optional): The year to filter by.
    - month (int, optional): The month to filter by (1 to 12).
    - quarter (int, optional): The quarter to filter by (1 to 4).

    Returns:
    - pd.DataFrame: The filtered DataFrame based on the specified criteria.
    """
    # Check if the 'Grade Change Date' column exists
    if 'Grade Change Date' not in df.columns:
        print('The "Grade Change Date" column is not found in the CSV file.')
        return pd.DataFrame()

    # Convert 'Grade Change Date' to datetime format
    df['Grade Change Date'] = pd.to_datetime(df['Grade Change Date'], format='%d-%b-%Y', errors='coerce')

    # Filter records to include only those with a non-null 'Grade Change Date'
    df = df[df['Grade Change Date'].notna()]

    # Debug: Print the number of rows after initial filtering
    print(f'Number of records with non-null "Grade Change Date": {df.shape[0]}')

    # Apply additional filters if specified
    if year is not None:
        df = df[df['Grade Change Date'].dt.year == year]
    if month is not None:
        df = df[df['Grade Change Date'].dt.month == month]

    if quarter is not None:
        # Filter by quarter
        quarters = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }
        # Ensure the quarter is valid
        if quarter in quarters:
            df = df[df['Grade Change Date'].dt.month.isin(quarters[quarter])]
        else:
            print(f'Invalid quarter value: {quarter}. Must be between 1 and 4.')

    # Debug: Print the number of rows after applying filters
    print(f'Number of records after filtering: {df.shape[0]}')

    return df

try:
    # Load the Excel file
    file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'
    csv_data = pd.read_excel(file_path)

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of employee records in the CSV file: {total_rows}')

    year = 2024
    month = None
    quarter = None

    # Filter data by grade change with no specific year, month, or quarter filter
    filtered_data = filter_employees_by_grade_change(csv_data, year=year, month=month, quarter=quarter)
    print(f'Total number of employees in year {year} with grade changes: {len(filtered_data)}')

except Exception as e:
    print(f'An error occurred: {e}')


# filter_all_employees_by_grade_change()