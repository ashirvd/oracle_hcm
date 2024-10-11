import pandas as pd
import calendar
import os

def new_joiners_pipeline(month=None):
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    year = 2024

    try:
        # Load the Excel file
        csv_data = pd.read_excel(file_path)

        # Check if the 'Date of Joining' column exists
        if 'Date of Joining' in csv_data.columns:
            # Count the number of employees with a non-null and non-empty Joining Date
            joining_date_count = csv_data['Date of Joining'].notna().sum()
        else:
            print('The "Date of Joining" column is not found in the Excel file.')

        def filter_by_date(df, year=None, month=None, status=None):
            if 'Date of Joining' in df.columns:
                # Convert 'Date of Joining' to datetime format for filtering purposes
                df = df.copy()  # Make a copy to avoid modifying the original DataFrame
                df['Date of Joining'] = pd.to_datetime(df['Date of Joining'], format='%d-%b-%Y', errors='coerce')

                # Remove rows where 'Date of Joining' couldn't be parsed
                df = df.dropna(subset=['Date of Joining'])

                if year is not None:
                    # Filter by year
                    df = df[df['Date of Joining'].dt.year == year]

                if month is not None:
                    # Filter by month
                    df = df[df['Date of Joining'].dt.month == month]

                if status is not None and 'Status' in df.columns:  # Check if 'Status' column exists
                    # Filter by employee status
                    df = df[df['Status'] == status]

            else:
                print('Joining Date column is not in dataset')

            return df

        def calculate_monthly_records(df, year, month):
            """Calculate the number of records for new joiners and in-progress employees for the specified year and month."""
            if month == 'all':
                for month in range(1, 13):  # Loop from January (1) to December (12)
                    new_joiners = filter_by_date(df, year=year, month=month, status='Active')  # New joiners
                    in_progress = filter_by_date(df, year=year, month=month, status='In Progress')  # In-progress employees

                    month_name = calendar.month_name[month]  # Get month name
                    print(f'Total new joiners for {month_name} {year}: {new_joiners.shape[0]}')
                    print(f'Total in-progress employees for {month_name} {year}: {in_progress.shape[0]}')
            elif month is not None and 1 <= month <= 12:  # Check if the month is valid
                new_joiners = filter_by_date(df, year=year, month=month, status='Active')  # New joiners
                in_progress = filter_by_date(df, year=year, month=month, status='In Progress')  # In-progress employees

                month_name = calendar.month_name[month]  # Get month name
                print(f'Total new joiners for {month_name} {year}: {new_joiners.shape[0]}')
                print(f'Total in-progress employees for {month_name} {year}: {in_progress.shape[0]}')
            else:
                print("Invalid month input. Please enter a number from 1 to 12 or 'all'.")

        # Calculate monthly records for the hardcoded year
        calculate_monthly_records(csv_data, year=year, month=month)

    except Exception as e:
        print(f'An error occurred: {e}')


new_joiners_pipeline(3)
new_joiners_pipeline('all')