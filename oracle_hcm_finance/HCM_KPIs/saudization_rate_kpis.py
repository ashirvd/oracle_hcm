from datetime import datetime
import pandas as pd
import os

def saudization_filter(month):
    """
    Calculates the Saudization rate for a given month of the year 2024.
    If the month is 'all', calculates for all months.

    Parameters:
    - month (int or str): The month (1 for January, 2 for February, etc.) or 'all' for all months.

    Prints the Saudization rate for the specified month or all months.
    """
    # File path to the Excel file
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    year = 2024

    # List of month names for formatting the output
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    try:
        # Load the Excel file into a DataFrame
        csv_data = pd.read_excel(file_path)

        # Convert date columns to datetime for proper filtering
        csv_data['Actual Termination date'] = pd.to_datetime(
            csv_data['Actual Termination date'], format='%d-%b-%Y', errors='coerce'
        )
        csv_data['Date of Joining'] = pd.to_datetime(
            csv_data['Date of Joining'], format='%d-%b-%Y', errors='coerce'
        )

        # Define a function to calculate and print the Saudization rate for a specific month
        def calculate_saudization(month):
            # Define start and end date for the given month
            start_date = pd.Timestamp(f'{year}-{month:02d}-01')
            end_date = start_date + pd.offsets.MonthEnd(1)

            # Filter the data based on the specified conditions
            filtered_data = csv_data[
                (csv_data['Job title - English'] != 'Board Member') &  # Exclude 'Board Member' job title
                (csv_data['Actual Termination date'].isna() | (csv_data['Actual Termination date'] > end_date)) &  # Include active employees or those whose termination date is after the end of the month
                (csv_data['Nationality'].notnull()) &  # Include only rows where Nationality is not null
                (csv_data['Date of Joining'] <= end_date)  # Include employees who joined before or during the current month
            ]

            # Calculate Saudization percentage
            saudization_rate = (
                (filtered_data['Nationality'].eq('Saudi Arabia').sum() / len(filtered_data) * 100)
                if not filtered_data.empty  # Avoid division by zero
                else 0
            )

            # Get the month name for output formatting
            month_name = month_names[month - 1]

            # Print the Saudization rate for the specified month and year
            print(f'Saudization Rate for {month_name} {year}: {saudization_rate:.2f}%')

        # If month is 'all', calculate for all months
        if month == 'all':
            for m in range(1, 13):
                calculate_saudization(m)
        else:
            # Call the Saudization calculation for the specified month
            calculate_saudization(month)

    except Exception as e:
        # Print any errors that occur during processing
        print(f'Error: {str(e)}')

# Example usage
saudization_filter(1)  # For January
saudization_filter('all')  # For all months
