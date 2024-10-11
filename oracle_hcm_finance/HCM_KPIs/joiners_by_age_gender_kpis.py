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
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
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
            # Set start_date for the given month
            start_date = f'{year}-{month:02d}-01'

            # Use the calendar module to get the last day of the month
            last_day_of_month = calendar.monthrange(year, month)[1]  # Returns a tuple (weekday, last_day)

            # Set end_date as the last day of the month (inclusive)
            end_date = f'{year}-{month:02d}-{last_day_of_month}'

            # Filter for employees who joined in the given month of 2024
            filtered_data = csv_data[(csv_data['Date of Joining'] >= start_date) & (csv_data['Date of Joining'] <= end_date)]

            # Exclude 'Board Member' job titles
            filtered_data = filtered_data[filtered_data['Job title - English'] != 'Board Member']

            # Calculate 'Age' in years from 'Date of Birth'
            current_date = pd.Timestamp(f'{year}-{month:02d}-{last_day_of_month}')  # Last day of the month
            filtered_data['Age'] = (current_date - filtered_data['Date of Birth']).dt.days // 365.25

            # Define age bins and labels
            age_bins = [0, 24, 34, 44, 59, float('inf')]
            age_labels = ['<25', '25-34', '35-44', '44-59', '>=60']

            # Categorize ages into bins
            filtered_data['AgeBand'] = pd.cut(filtered_data['Age'], bins=age_bins, labels=age_labels)

            # Group by 'Gender' and 'AgeBand' and count the records
            age_gender_counts = filtered_data.groupby(['AgeBand', 'Gender'], observed=False).size().unstack(fill_value=0)

            # Print the counts of employees by age band and gender for the selected month
            print(f"\nCounts of employees by age band and gender {pd.to_datetime(start_date).strftime('%B %Y')}:")
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

# Example usage: Print results for all months in 2024
joiners_by_age_gender('all')
joiners_by_age_gender(3)
