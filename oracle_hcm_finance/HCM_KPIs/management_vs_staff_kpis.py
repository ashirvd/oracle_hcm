from datetime import datetime

import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def filter_by_date_and_termination(data, year=None, month=None, quarter=None):
    """
    Filters employees where 'Date of Joining' is available and 'Actual Termination Date' is either null or
    greater than today. Additional filters can be applied based on year, month, and quarter.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing employee data.
    - year (int, optional): Year filter.
    - month (int, optional): Month filter.
    - quarter (int, optional): Quarter filter.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    # Check if 'Date of Joining' column exists in the data
    if 'Date of Joining' in data.columns:
        # Convert 'Date of Joining' to datetime format
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        # Remove rows where 'Date of Joining' couldn't be parsed
        data = data.dropna(subset=['Date of Joining'])

        # Check for 'Actual Termination Date' column and filter rows
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')

            # Filter employees where Actual Termination Date is null or greater than today
            today = pd.Timestamp(datetime.now().date())
            end_of_2024 = pd.Timestamp('2024-12-31')

            # Filter employees based on termination date criteria
            data = data[
                (data['Actual Termination date'].isna()) |
                ((data['Actual Termination date'] > today) &
                 (data['Actual Termination date'] < end_of_2024))
                ]
            print(f"Total number of employees with 'Actual Termination Date' null or greater than today: {data.shape[0]}")
        else:
            print('Actual Termination Date column is not in the dataset.')

        # Apply year filter if specified
        if year is not None:
            end_of_year = pd.Timestamp(year, 12, 31)
            data = data[data['Date of Joining'] <= end_of_year]

            # Apply month filter if specified
            if month is not None:
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                data = data[data['Date of Joining'] <= end_of_month]

        # Apply month filter if no year is provided
        elif month is not None:
            data = data[data['Date of Joining'].dt.month == month]

        # Apply quarter filter if specified
        if quarter is not None:
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in quarters:
                data = data[data['Date of Joining'].dt.month.isin(quarters[quarter])]

        return data

    else:
        print('Date of Joining column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame


try:
    # Load the Excel file
    csv_data = pd.read_excel(file_path)

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the dataset: {total_rows}')

    # Step 1: Filter employees based on joining date and termination date
    filtered_data = filter_by_date_and_termination(csv_data, year=2024, month=None, quarter=None)

    # Step 2: Check if the Grade column exists in the filtered data
    if 'Grade' in filtered_data.columns:
        # Define grades for Management
        management_grades = ['C2', 'T5', '6', '7', '8', '9', '10', '11', '12', 'CEO']

        # Step 3: Filter the data for Management and Staff
        management_data = filtered_data[filtered_data['Grade'].isin(management_grades)]
        staff_data = filtered_data[~filtered_data['Grade'].isin(management_grades)]

        # Step 4: Count the number of Management and Staff employees
        management_count = management_data.shape[0]
        staff_count = staff_data.shape[0]

        # Step 5: Calculate the ratio of Management to Staff
        if staff_count > 0:
            ratio = (management_count / staff_count) * 100
        else:
            ratio = float('inf')  # Avoid division by zero

        # Print the results
        print(f'Total number of Management employees: {management_count}')
        print(f'Total number of Staff employees: {staff_count}')
        print(f'Ratio of Management to Staff: {ratio:.2f}%')
    else:
        print('Grade column not found in the filtered dataset.')

except Exception as e:
    print(f'An error occurred: {e}')

