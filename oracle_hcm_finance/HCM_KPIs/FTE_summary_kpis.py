import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd
import os


def calculate_fte(month):
    """
    Calculate the total Full-Time Equivalent (FTE) for a given month or for all months.

    Parameters:
    month (int or str): The month for which to calculate FTE (1 for January, 2 for February, etc.) or 'all' for all months.
    """

    # Load employee data into a pandas DataFrame
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'

    # Check if the file exists before attempting to read it
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    # Attempt to read the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return  # Exit the function if there is an error reading the file

    # Convert date columns to datetime format
    df['Actual_Termination_Date'] = pd.to_datetime(df['Actual Termination date'], errors='coerce')
    df['Date_of_Joining'] = pd.to_datetime(df['Date of Joining'], errors='coerce')

    # Define the year for the calculation
    year = 2024

    # Filter out employees who are board members
    filtered_df = df[df['Job title - English'] != 'Board Member'].copy()

    # Calculate FTE based on the assignment category
    # 0.6 for 'Touring 6:6' and 1 for all others
    filtered_df['FTE'] = filtered_df['Assignment Category'].apply(lambda x: 0.6 if x == 'Touring 6:6' else 1)

    # Function to calculate FTE for a specific month
    def calculate_fte_for_month(m):
        # Determine the last day of the specified month
        end_date = (datetime(year, m, 1) + MonthEnd(0))

        # Determine the first day of the next month for termination cutoff
        termination_cutoff_date = (datetime(year, m + 1, 1) if m < 12 else datetime(year + 1, 1, 1))

        # Filter employees based on joining and termination dates
        month_filtered_df = filtered_df[
            (filtered_df['Date_of_Joining'] <= end_date) &  # Joined on or before end of month
            ((filtered_df['Actual_Termination_Date'].isna()) |  # Not terminated
             (filtered_df['Actual_Termination_Date'] >= termination_cutoff_date))  # Or terminated after the cutoff
        ]

        # Calculate total FTE and convert to integer
        total_fte = int(month_filtered_df['FTE'].sum())

        # Print the total FTE for the given month
        print(f'Total FTE for {end_date.strftime("%B, %Y")}: {total_fte}')

    # If 'all' is passed, iterate over all months
    if month == 'all':
        for m in range(1, 13):
            calculate_fte_for_month(m)
    else:
        # Calculate FTE for the specified month
        calculate_fte_for_month(month)


# Example usage:
calculate_fte(1)
calculate_fte('all')  # Calculate FTE for all months
