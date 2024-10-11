import pandas as pd
import os

def leavers_by_age_gender(month):
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    year = 2024

    try:
        # Read the Excel file
        csv_data = pd.read_excel(file_path)

        termination_column = 'Termination / Resignation'

        # Convert 'Actual Termination date' to datetime
        termination_date_column = 'Actual Termination date'
        csv_data[termination_date_column] = pd.to_datetime(csv_data[termination_date_column], errors='coerce')

        # Convert 'Age' column to numeric, coercing errors
        age_column = 'Age'
        csv_data[age_column] = pd.to_numeric(csv_data[age_column], errors='coerce')

        # Define age bins and labels
        age_bins = [0, 24, 34, 44, 59, float('inf')]
        age_labels = ['<25', '25-34', '35-44', '45-59', '>60']

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

                # Count leavers by age category and gender without modifying the original DataFrame
                if total_leavers_month > 0:
                    # Create age category in memory
                    age_categories = pd.cut(
                        leavers_month[age_column],
                        bins=age_bins,
                        labels=age_labels,
                        right=True
                    )

                    # Group by age category and gender with observed parameter
                    age_gender_counts = leavers_month.groupby([age_categories, 'Gender'],
                                                              observed=False).size().unstack(fill_value=0)

                    # Add a Total column
                    age_gender_counts['Total'] = age_gender_counts.sum(axis=1)

                    print(f'Leavers in {month_names[m]} {year} by Age Category and Gender:')
                    print(age_gender_counts)
                    print()  # Add a blank line for better readability

        else:
            # Validate month input
            if month < 1 or month > 12:
                print("Invalid month. Please provide a month between 1 and 12.")
                return

            # Filter leavers in the specified month of 2024
            leavers_2024 = csv_data[
                (csv_data[termination_column].notna()) &
                (csv_data[termination_date_column].dt.year == year) &
                (csv_data[termination_date_column].dt.month == month)
                ]

            # Count leavers for the specified month
            total_leavers_month = leavers_2024.shape[0]
            print(f'Total number of leavers in {month_names[month]} {year}: {total_leavers_month}')

            # Count leavers by age category and gender
            if total_leavers_month > 0:
                # Create age category in memory
                age_categories = pd.cut(
                    leavers_2024[age_column],
                    bins=age_bins,
                    labels=age_labels,
                    right=True
                )

                # Group by age category and gender
                age_gender_counts = leavers_2024.groupby([age_categories, 'Gender'], observed=False).size().unstack(
                    fill_value=0)

                # Add a Total column
                age_gender_counts['Total'] = age_gender_counts.sum(axis=1)

                print(f'Leavers in {month_names[month]} {year} by Age Category and Gender:')
                print(age_gender_counts)
                print()  # Add a blank line for better readability

    except Exception as e:
        print(f'Failed to load file: {e}')


leavers_by_age_gender(1)  # Call the function to get leavers for January 2024
leavers_by_age_gender('all')  # Call the function to get leavers for all months in 2024
