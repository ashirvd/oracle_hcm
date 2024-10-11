from datetime import datetime
import pandas as pd
import calendar
import os


def management_vs_staff(month):
    """
    Calculates the management-to-staff ratio for a given month of the year 2024.
    If the month is 'all', calculates for all months.

    Parameters:
    - month (int or str): The month (1 for January, 2 for February, etc.) or 'all' for all months.

    Prints the management vs staff ratio for the specified month or all months.
    """
    year = 2024
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    try:
        # Load the Excel file
        employee_data = pd.read_excel(file_path)

        # Check if 'Date of Joining' column exists in the data
        if 'Date of Joining' in employee_data.columns:
            # Convert 'Date of Joining' to datetime format
            employee_data['Date of Joining'] = pd.to_datetime(employee_data['Date of Joining'], format='%d-%b-%Y',
                                                              errors='coerce')

            # Remove rows where 'Date of Joining' couldn't be parsed
            employee_data = employee_data.dropna(subset=['Date of Joining'])

            # Check for 'Actual Termination Date' column and filter rows
            if 'Actual Termination date' in employee_data.columns:
                employee_data['Actual Termination date'] = pd.to_datetime(employee_data['Actual Termination date'],
                                                                          format='%d-%b-%Y', errors='coerce')

                # Filter employees where Actual Termination Date is null or greater than today
                today = pd.Timestamp(datetime.now().date())
                end_of_year = pd.Timestamp(f'{year}-12-31')

                # Filter employees based on termination date criteria
                employee_data = employee_data[
                    (employee_data['Actual Termination date'].isna()) |
                    ((employee_data['Actual Termination date'] > today) &
                     (employee_data['Actual Termination date'] < end_of_year))
                    ]
            else:
                print('Actual Termination Date column is not in the dataset.')

            # Define a function to calculate and print the ratio for a specific month
            def calculate_ratio(month):
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                filtered_data = employee_data[employee_data['Date of Joining'] <= end_of_month]

                # Check if the Grade column exists in the filtered data
                if 'Grade' in filtered_data.columns:
                    # Define grades for Management
                    management_grades = ['C2', 'T5', '6', '7', '8', '9', '10', '11', '12', 'CEO']

                    # Filter the data for Management and Staff
                    management_data = filtered_data[filtered_data['Grade'].isin(management_grades)]
                    staff_data = filtered_data[~filtered_data['Grade'].isin(management_grades)]

                    # Count the number of Management and Staff employees
                    management_count = management_data.shape[0]
                    staff_count = staff_data.shape[0]

                    # Calculate the ratio of Management to total employees (Management + Staff)
                    total_count = management_count + staff_count
                    if total_count > 0:
                        ratio = (management_count / total_count) * 100
                    else:
                        ratio = float('inf')  # Avoid division by zero

                    # Get the month name from the month number
                    month_name = calendar.month_name[month]

                    # Print the result for the specified month
                    print(f'Management vs Staff ratio of {month_name} {year}: {ratio:.2f}%')
                else:
                    print(f'Grade column not found in the dataset for month {month}.')

            # If month is 'all', calculate for all months
            if month == 'all':
                for m in range(1, 13):
                    calculate_ratio(m)
            else:
                # Call the ratio calculation for the specified month
                calculate_ratio(month)

        else:
            print('Date of Joining column is not in the dataset.')

    except Exception as e:
        print(f'An error occurred: {e}')


management_vs_staff(1)
management_vs_staff('all')
