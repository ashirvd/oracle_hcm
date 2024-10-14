from datetime import datetime
import pandas as pd
import os


def management_vs_staff(month):
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    year = 2024

    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Ensure 'Date of Joining' exists and convert it to datetime
        if 'Date of Joining' in data.columns:
            data = data.copy()
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')
            data = data.dropna(subset=['Date of Joining'])  # Drop rows where 'Date of Joining' couldn't be parsed

            # Exclude 'Board Members' if necessary
            if 'Job title - English' in data.columns:
                data = data[data['Job title - English'] != 'Board Member']

            # If 'Actual Termination date' exists, filter based on that
            if 'Actual Termination date' in data.columns:
                data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y',
                                                                 errors='coerce')
                today = pd.Timestamp(datetime.now().date())

                # Define management grades
                management_grades = ['6', '7', '8', '9', '10', '11', '12', '13', 'C2', 'CEO']

                # Function to calculate headcount for a specific month
                def calculate_management_percentage_for_month(month):
                    # Get the end of the month
                    end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)

                    # Filter for employees who joined on or before the end of the month and are still active
                    filtered_data = data[
                        (data['Date of Joining'] <= end_of_month) &  # Employees joined on or before the month end
                        ((data['Actual Termination date'].isna()) | (data['Actual Termination date'] > end_of_month))
                    ].copy()

                    # Use .loc[] to avoid the SettingWithCopyWarning
                    filtered_data.loc[:, 'Category'] = filtered_data['Grade'].apply(
                        lambda grade: 'Management' if grade in management_grades else 'Staff'
                    )

                    # Calculate total and management headcount
                    total_count = filtered_data.shape[0]
                    management_count = filtered_data[filtered_data['Category'] == 'Management'].shape[0]

                    # Calculate the percentage of management employees
                    management_percentage = (management_count / total_count) * 100 if total_count > 0 else 0

                    return management_count, management_percentage

                # If 'all' is passed, calculate for every month
                if month == 'all':
                    results = {}
                    for month_number in range(1, 13):
                        month_name = pd.Timestamp(year=year, month=month_number, day=1).strftime('%B')
                        management_count, management_percentage = calculate_management_percentage_for_month(month_number)
                        results[month_name] = {
                            'Management Count': management_count,
                            'Management Percentage': f"{management_percentage:.2f}%"
                        }
                        print(f"The Ratio of {month_name} is {management_percentage:.2f}%")
                    return results

                # Otherwise, calculate for a specific month
                else:
                    if month < 1 or month > 12:
                        print("Invalid month index. Please provide a number between 1 (January) and 12 (December) or 'all'.")
                        return
                    management_count, management_percentage = calculate_management_percentage_for_month(month)
                    month_name = pd.Timestamp(year=year, month=month, day=1).strftime('%B')
                    print(f"The Ratio of {month_name} is {management_percentage:.2f}%")
                    return management_count, management_percentage

            else:
                print('Actual Termination Date column is not in the dataset.')
                return 0

        else:
            print('Date of Joining column is not in the dataset.')
            return 0

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0


# Example usage:
management_vs_staff(1)  # January
management_vs_staff('all')  # All months
