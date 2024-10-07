import pandas as pd
from datetime import datetime

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def filter_all_employees_by_termination_date():

    try:
        # Load the CSV file
        csv_data = pd.read_excel(file_path)  # Try different encodings if necessary

        # Get the total number of rows
        total_rows = csv_data.shape[0]
        print(f'Total number of employee records in the CSV file: {total_rows}')

        # Check if the 'Joining Date' column exists
        if 'Termination / Resignation' in csv_data.columns:
            # Count the number of employees with a non-null and non-empty Joining Date
            resgignation_count = csv_data['Termination / Resignation'].notna().sum()
            print(f'Total number of employees with a resignation/termination: {resgignation_count}')
        else:
            print('The "Ternimation" column is not found in the CSV file.')

    except Exception as e:
        print(f'An error occurred: {e}')

filter_all_employees_by_termination_date()

def filter_terminated_employee_by_date(df, year=None, month=None, quarter=None):
    """
    Filters the employee records based on the Actual Termination Date for the specified year, month, or quarter.
    If all parameters are None, it will return records with non-null Actual Termination Date.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing employee data.
    - year (int, optional): The year to filter by.
    - month (int, optional): The month to filter by (1 to 12).
    - quarter (int, optional): The quarter to filter by (1 to 4).

    Returns:
    - pd.DataFrame: The filtered DataFrame based on the specified criteria.
    """
    # Check if the 'Actual Termination date' column exists
    if 'Actual Termination date' not in df.columns:
        print('The "Actual Termination date" column is not found in the dataset.')
        return pd.DataFrame()

    # Convert 'Actual Termination date' to datetime format
    df['Actual Termination date'] = pd.to_datetime(df['Actual Termination date'], errors='coerce')

    # Filter out rows with Actual Termination Date greater than today's date
    today = pd.Timestamp(datetime.now().date())
    df = df[df['Actual Termination date'] <= today]

    # Apply additional filters if specified
    if year is not None:
        df = df[df['Actual Termination date'].dt.year == year]
    if month is not None:
        df = df[df['Actual Termination date'].dt.month == month]

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
            df = df[df['Actual Termination date'].dt.month.isin(quarters[quarter])]

    return df

# Example usage
try:
    # Load the Excel file
    file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'
    csv_data = pd.read_excel(file_path)  # Load the file

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of employee records in the dataset: {total_rows}')

    # Specify filter parameters
    year = 2024
    month = None
    quarter = None

    # Filter data by termination date
    filtered_data = filter_terminated_employee_by_date(csv_data, year=year, month=month, quarter=quarter)

    # Count the filtered employees
    print(f'Total number of employees with termination date till today in {year}: {len(filtered_data)}')

except Exception as e:
    print(f'An error occurred: {e}')