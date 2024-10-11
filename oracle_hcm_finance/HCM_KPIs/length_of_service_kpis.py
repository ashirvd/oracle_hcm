import pandas as pd
from datetime import datetime
import os

# Define the function to calculate length of service
def length_of_service(month):
    target_year = 2024
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    # List of month names
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    def filter_by_termination_and_joining_date(data, target_year, month):
        # Convert 'Actual Termination date' and 'Date of Joining' to datetime format
        if 'Actual Termination date' in data.columns and 'Date of Joining' in data.columns:
            data = data.copy()  # Make a copy to avoid modifying the original DataFrame
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y',
                                                             errors='coerce')
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce',
                                                     dayfirst=True)

            target_date = pd.Timestamp(f'{target_year}-{month}-01')

            # Filter active employees:
            # - Joining date must be before the target date
            # - Termination date must be after the target date or null
            filtered_data = data[
                (data['Date of Joining'] < target_date) &
                ((data['Actual Termination date'].isna()) | (data['Actual Termination date'] >= target_date))
            ]

            # Filter out employees whose 'Job title - English' is 'Board Member'
            if 'Job title - English' in data.columns:
                filtered_data = filtered_data[filtered_data['Job title - English'] != 'Board Member']
            else:
                print('Job title - English column is not in the dataset.')

            return filtered_data
        else:
            print('Actual Termination Date or Date of Joining column is not in the dataset.')
            return pd.DataFrame()  # Return an empty DataFrame

    def calculate_service_bins(filtered_data):
        # Get today's date for service length calculation
        today = pd.Timestamp(datetime.now().date())

        def calculate_exact_service(joining_date):
            year_diff = today.year - joining_date.year

            # Check if the anniversary has passed this year
            if (today.month > joining_date.month) or (
                    today.month == joining_date.month and today.day >= joining_date.day):
                return year_diff  # Anniversary has passed or is today
            else:
                return year_diff - 1  # Anniversary hasn't passed yet

        # Apply the logic for exact service years calculation
        filtered_data['Exact Service Years'] = filtered_data['Date of Joining'].apply(calculate_exact_service)

        # Define bins for service lengths (<1 year, 1-3 years, 3-5 years, 5+ years)
        bins = [0, 1, 3, 5, float('inf')]  # Upper limit is now infinity for 5+ years
        labels = ['<1 year', '1-3 years', '3-5 years', '5+ years']

        # Categorize employees into bins based on their exact service length
        filtered_data['Service Category'] = pd.cut(filtered_data['Exact Service Years'], bins=bins, labels=labels,
                                                   right=False)

        # Check for employees with exactly 3 years of service to adjust categories
        filtered_data.loc[filtered_data['Exact Service Years'] == 3, 'Service Category'] = '1-3 years'

        # Count employees in each category
        service_counts = filtered_data['Service Category'].value_counts(sort=False)

        # Calculate the percentages
        service_percentages = (service_counts / filtered_data.shape[0]) * 100
        service_percentages = service_percentages.round(2)  # Round to 2 decimal places

        return service_counts, service_percentages

    def combine_service_bins(service_counts, service_percentages):
        # Combine '3-5 years' and '5+ years' into '3+ years'
        combined_count = service_counts['3-5 years'] + service_counts['5+ years']
        combined_percentage = service_percentages['3-5 years'] + service_percentages['5+ years']

        # Create new series with the combined category
        new_counts = service_counts.drop(['3-5 years', '5+ years'])
        new_percentages = service_percentages.drop(['3-5 years', '5+ years'])

        # Add the combined '3+ years' category
        new_counts['3+ years'] = combined_count
        new_percentages['3+ years'] = combined_percentage

        return new_counts, new_percentages

    try:
        # Load the Excel file
        csv_data = pd.read_excel(file_path)

        if month == 'all':
            # Loop through all months and calculate service lengths
            results = {}
            for month in range(1, 13):
                filtered_data = filter_by_termination_and_joining_date(csv_data, target_year, month)

                # Get the total number of rows after filtering
                total_rows_filtered = filtered_data.shape[0]
                print(
                    f'Total number of active employees as of {month_names[month - 1]}/{target_year} (excluding Board Members): {total_rows_filtered}')

                # Calculate the service bins and percentages
                service_counts, service_percentages = calculate_service_bins(filtered_data)

                # Combine the '3-5 years' and '5+ years' bins into '3+ years'
                combined_counts, combined_percentages = combine_service_bins(service_counts, service_percentages)

                # Store the results
                results[month] = (combined_counts, combined_percentages)

                # Print the results for the month
                print(f"\nService Length Distribution for {month_names[month - 1]}/{target_year}:")
                for label, count, percentage in zip(combined_counts.index, combined_counts, combined_percentages):
                    print(f'{label}: {count} employees ({percentage:.2f}%)')

                # Verify the total number of computed employees
                total_count_computed = combined_counts.sum()
                print("\nSum of all Employees computed:", total_count_computed)

            return results  # Return results for all months

        else:
            # Filter data based on termination date, joining date, and job title for the target month
            filtered_data = filter_by_termination_and_joining_date(csv_data, target_year, month)

            # Get the total number of rows after filtering
            total_rows_filtered = filtered_data.shape[0]
            print(
                f'Total number of active employees as of {month_names[month - 1]}/{target_year} (excluding Board Members): {total_rows_filtered}')

            # Calculate the service bins and percentages
            service_counts, service_percentages = calculate_service_bins(filtered_data)

            # Combine the '3-5 years' and '5+ years' bins into '3+ years'
            combined_counts, combined_percentages = combine_service_bins(service_counts, service_percentages)

            # Print the results for the specified month
            print("\nService Length Distribution:")
            for label, count, percentage in zip(combined_counts.index, combined_counts, combined_percentages):
                print(f'{label}: {count} employees ({percentage:.2f}%)')

            # Verify the total number of computed employees
            total_count_computed = combined_counts.sum()
            print("\nSum of all Employees computed:", total_count_computed)

    except UnicodeDecodeError:
        print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')

# Example usage
length_of_service('all')
