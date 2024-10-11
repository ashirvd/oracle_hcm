import pandas as pd
import calendar
import os


def promotion_by_ageband_gender(month):
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    try:
        # Load the data
        csv_data = pd.read_excel(file_path)  # Adjust encoding as necessary

        # Define the year for filtering
        year = 2024

        # Define age categories
        age_bins = [float('-inf'), 24, 34, 44, 59, float('inf')]
        age_labels = ['<25', '25-34', '35-44', '45-59', '>60']

        # Convert Age column to numeric, handle errors if any
        csv_data['Age'] = pd.to_numeric(csv_data['Age'], errors='coerce')

        # Filter for Grade Change Date
        if 'Grade Change Date' in csv_data.columns:
            csv_data['Grade Change Date'] = pd.to_datetime(csv_data['Grade Change Date'], format='%d-%b-%Y',
                                                           errors='coerce')  # Adjust format as necessary
            csv_data = csv_data.dropna(subset=['Grade Change Date'])  # Remove rows where date couldn't be parsed

            # Check if all months or a specific month is requested
            if month == 'all':
                months = range(1, 13)  # Loop through all months
            else:
                months = [month]  # Create a list with the specified month

            for month_num in months:
                # Filter by year and month
                filtered_data = csv_data[(csv_data['Grade Change Date'].dt.year == year) &
                                         (csv_data[
                                              'Grade Change Date'].dt.month == month_num)].copy()  # Use .copy() to avoid SettingWithCopyWarning

                # Get the total number of employees with a non-empty 'Grade Change Date'
                total_promoted = filtered_data.shape[0]
                month_name = calendar.month_name[month_num]  # Get month name
                print(f'Total number of employees who got promoted in {month_name} {year}: {total_promoted}')

                # Add age category column using .loc
                filtered_data['Age Category'] = pd.cut(filtered_data['Age'], bins=age_bins, labels=age_labels)

                # Count employees in each age category by gender
                age_gender_counts = filtered_data.groupby(['Age Category', 'Gender'], observed=False).size().unstack(
                    fill_value=0)

                # Print results for age categories only
                print(f'\nMonth: {month_name} {year}')
                for age_category in age_gender_counts.index:
                    male_count = age_gender_counts.loc[age_category].get('Male', 0)
                    female_count = age_gender_counts.loc[age_category].get('Female', 0)
                    print(f'Age Category {age_category}: Male = {male_count}, Female = {female_count}')
                print()  # Print a new line for better readability
        else:
            print('Grade Change Date column is not in the dataset')

    except UnicodeDecodeError:
        print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')


# Example usage
promotion_by_ageband_gender('all')
promotion_by_ageband_gender(3)
