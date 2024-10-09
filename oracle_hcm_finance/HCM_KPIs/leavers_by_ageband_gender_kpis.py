import pandas as pd
import os

def leavers(month):
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    year = 2024

    try:
        # Read the Excel file
        csv_data = pd.read_excel(file_path)  # Changed to read_excel for .xlsx files

        # Get the total number of records
        total_rows = csv_data.shape[0]
        # print(f'Total number of records in the Excel file: {total_rows}')

        termination_column = 'Termination / Resignation'
        non_empty_count = csv_data[termination_column].notna().sum()
        # print(f'Total number of leavers are: {non_empty_count}')

        # Convert 'Actual Termination date' to datetime
        termination_date_column = 'Actual Termination date'  # Updated to correct column name
        csv_data[termination_date_column] = pd.to_datetime(csv_data[termination_date_column], errors='coerce')

        # Month names for display
        month_names = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

        if month == 'all':
            # Iterate through each month (1 to 12)
            for m in range(1, 13):
                leavers_month = csv_data[
                    (csv_data[termination_column].notna()) &
                    (csv_data[termination_date_column].dt.year == year) &
                    (csv_data[termination_date_column].dt.month == m)
                    ]

                # Count leavers for the specified month
                total_leavers_month = leavers_month.shape[0]
                print(f'Total number of leavers in {month_names[m]} {year}: {total_leavers_month}')
        else:
            # Validate month input
            if month < 1 or month > 12:
                print("Invalid month. Please provide a month between 1 and 12.")
                return

            # Filter leavers in the specified month of 2024
            leavers_2024 = csv_data[
                (csv_data[termination_column].notna()) &
                (csv_data[termination_date_column].dt.year == year) &  # Year is hardcoded to 2024
                (csv_data[termination_date_column].dt.month == month)
                ]

            # Count leavers for the specified month
            total_leavers_month = leavers_2024.shape[0]
            print(f'Total number of leavers in {month_names[month]} {year}: {total_leavers_month}')

        # Convert 'Age' column to numeric, coercing errors
        age_column = 'Age'
        csv_data[age_column] = pd.to_numeric(csv_data[age_column], errors='coerce')

        # Define age bins and labels
        age_bins = [0, 24, 34, 44, 59, float('inf')]
        age_labels = ['<25', '25-34', '35-44', '45-59', '>60']

        # Create a new column for age categories
        csv_data['Age Category'] = pd.cut(csv_data[age_column], bins=age_bins, labels=age_labels, right=True)

        # Filter rows where 'Termination / Resignation' is not empty
        filtered_data = csv_data[csv_data[termination_column].notna()]

        # Count records based on age category and gender
        age_gender_counts = filtered_data.groupby(['Age Category', 'Gender'], observed=False).size().unstack(
            fill_value=0)

        # Print age and gender distribution
        # print(age_gender_counts)

    except Exception as e:
        print(f'Failed to load file: {e}')


#leavers('all')  # Call the function to get leavers for all months in 2024
leavers(1)  # Call the function to get leavers for January 2024
