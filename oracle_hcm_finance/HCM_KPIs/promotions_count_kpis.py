import pandas as pd
import os

def promotion_count(month):
    """
    Filters the employee records based on Grade Change Date for the specified month in the year 2024.
    If 'all' is specified, it returns records for all months from January to December.

    Parameters:
    - month (int or str): The month to filter by (1 to 12) or 'all' for all months.

    Returns:
    - None: Prints the count of filtered employee records based on the specified criteria.
    """
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    try:
        # Load the Excel file
        csv_data = pd.read_excel(file_path)

        # Check if the 'Grade Change Date' column exists
        if 'Grade Change Date' not in csv_data.columns:
            print('The "Grade Change Date" column is not found in the CSV file.')
            return

        # Convert 'Grade Change Date' to datetime format
        csv_data['Grade Change Date'] = pd.to_datetime(csv_data['Grade Change Date'], format='%d-%b-%Y',
                                                       errors='coerce')

        # Filter records to include only those with a non-null 'Grade Change Date'
        csv_data = csv_data[csv_data['Grade Change Date'].notna()]

        # Hardcode the year to 2024
        year = 2024

        if month == 'all':
            # Initialize a dictionary to hold promotion counts for each month
            monthly_promotions = {}

            # Loop through each month from January to December
            for m in range(1, 13):
                # Filter for the specific month
                month_data = csv_data[(csv_data['Grade Change Date'].dt.year == year) &
                                      (csv_data['Grade Change Date'].dt.month == m)]
                monthly_promotions[m] = month_data.shape[0]
                print(
                    f'Number of promotions in month {pd.to_datetime(f"2024-{m}-01").strftime("%B")} = {monthly_promotions[m]}')

        else:
            # Filter by specified month
            month_data = csv_data[(csv_data['Grade Change Date'].dt.year == year) &
                                  (csv_data['Grade Change Date'].dt.month == month)]
            print(
                f'Number of promotions in month {pd.to_datetime(f"2024-{month}-01").strftime("%B")} = {month_data.shape[0]}')

    except Exception as e:
        print(f'An error occurred: {e}')



promotion_count(1)  # This will filter for January 2024
promotion_count('all')  # This will filter for all months in 2024
