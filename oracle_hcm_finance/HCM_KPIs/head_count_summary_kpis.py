from datetime import datetime
import pandas as pd

def filter_by_date(data, year=None, month=None, quarter=None):
    # Check if 'Date of Joining' column exists in the data
    if 'Date of Joining' in data.columns:
        # Convert 'Date of Joining' to datetime format
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        # Remove rows where 'Date of Joining' couldn't be parsed
        data = data.dropna(subset=['Date of Joining'])

        # Exclude employees with 'Board Member' in the 'Job title - English' column
        if 'Job title - English' in data.columns:
            data = data[data['Job title - English'] != 'Board Member']

        # Check for 'Actual Termination date' column and filter rows without termination dates
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            # Filter employees without a termination date or with termination date greater than today
            today = pd.Timestamp(datetime.now().date())
            end_of_2024 = pd.Timestamp('2025-12-31')
            # Filter employees based on termination date criteria
            filtered_data = data[
                (data['Actual Termination date'].isna()) |
                ((data['Actual Termination date'] > today) &
                 (data['Actual Termination date'] < end_of_2024))
            ]
        else:
            print('Actual Termination Date column is not in the dataset.')
            filtered_data = data

        # Apply year filter if specified
        if year is not None:
            end_of_year = pd.Timestamp(year, 12, 31)
            filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_year]

            if month is not None:
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_month]

        elif month is not None:
            filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month == month]

        if quarter is not None:
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in quarters:
                filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month.isin(quarters[quarter])]

        return filtered_data

    else:
        print('Date of Joining column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame


def count_employees_by_joining_date(file_path, year=None, month=None, quarter=None):
    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Count total employees
        total_employees = data.shape[0]

        # Filter data based on the criteria
        filtered_data = filter_by_date(data, year=year, month=month, quarter=quarter)

        # Count employees who meet the filter criteria
        filtered_count = filtered_data.shape[0]

        # Count terminated employees
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            terminated_employees = data[data['Actual Termination date'].notna()].shape[0]

            # Define today's date and end of 2024
            today = pd.Timestamp(datetime.now().date())
            end_of_2024 = pd.Timestamp('2024-12-31')

            # Filter employees whose termination date is greater than today and before 2025
            employees_terminated_after_today_and_before_2025 = data[
                (data['Actual Termination date'].notna()) &
                (data['Actual Termination date'] > today) &
                (data['Actual Termination date'] <= end_of_2024)
            ]

        else:
            terminated_employees = 0

        print(f'Total number of employees in the sheet: {total_employees}')
        print(f'Total number of employees matching the filter criteria: {filtered_count}')
        print(f'Total number of terminated employees: {terminated_employees}')

        return total_employees, filtered_count, terminated_employees

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0, 0, 0, 0


# Example usage
file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'
total_employees, filtered_data_count, terminated_employees = count_employees_by_joining_date(
    file_path, year=2024, month=None, quarter=None)
