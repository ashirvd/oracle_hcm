import calendar
import pandas as pd
import os


def joiners_by_age_gender(month):
    """
    Function to filter employee data based on the month of joining in the year 2024,
    and group the data by age bands and gender, counting the number of joiners.

    Parameters:
    month (int or str): Month for which the data should be filtered (1 for January, 2 for February, etc.)
                        If 'all', the function will print the results for all months in 2024.

    Returns:
    None: The function prints the DataFrame showing the counts of employees by age band and gender.
    """
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'

    # Check if the file exists before attempting to read it
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    try:
        # Load the Excel file
        csv_data = pd.read_excel(file_path)

        # Convert 'Date of Joining' and 'Date of Birth' to datetime
        csv_data['Date of Joining'] = pd.to_datetime(csv_data['Date of Joining'], errors='coerce')
        csv_data['Date of Birth'] = pd.to_datetime(csv_data['Date of Birth'], errors='coerce')

        year = 2024

        # Define a function to process a specific month
        def process_month(month):
            # Set the start and end dates for the given month
            start_date = pd.Timestamp(year, month, 1)
            last_day_of_month = calendar.monthrange(year, month)[1]
            end_date = pd.Timestamp(year, month, last_day_of_month)

            # Filter for employees who joined in the given month of 2024
            filtered_data = csv_data[
                (csv_data['Date of Joining'] >= start_date) &
                (csv_data['Date of Joining'] <= end_date)
            ]

            # Exclude 'Board Member' job titles
            filtered_data = filtered_data[filtered_data['Job title - English'] != 'Board Member']

            # Calculate 'Age' in years from 'Date of Birth' relative to today's date
            current_date = pd.Timestamp.today()  # Use today's date for age calculation
            filtered_data['Age'] = (current_date - filtered_data['Date of Birth']).dt.days // 365

            # Define age bins and labels
            age_bins = [0, 24, 34, 44, 59, float('inf')]
            age_labels = ['<25', '25-34', '35-44', '44-59', '>=60']

            # Categorize ages into bins
            filtered_data['AgeBand'] = pd.cut(filtered_data['Age'], bins=age_bins, labels=age_labels, right=True)

            # Group by 'Gender' and 'AgeBand' and count the records
            age_gender_counts = filtered_data.groupby(['AgeBand', 'Gender'], observed=False).size().unstack(fill_value=0)

            # Add a total column that sums across rows
            age_gender_counts['Total'] = age_gender_counts.sum(axis=1)

            # Print the counts of employees by age band and gender for the selected month
            print(f"\nCounts of employees who joined in {pd.to_datetime(start_date).strftime('%B %Y')}:")
            print(age_gender_counts)

        # If 'all' is passed, process all months from January to December
        if month == 'all':
            for m in range(1, 13):  # Loop through months 1 to 12
                process_month(m)
        else:
            # If a specific month is passed, process that single month
            process_month(month)

    except Exception as e:
        print(f'An error occurred: {e}')

joiners_by_age_gender(2)
joiners_by_age_gender('all')
