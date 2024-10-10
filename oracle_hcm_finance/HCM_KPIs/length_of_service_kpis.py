import pandas as pd
from datetime import datetime

file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'

def filter_by_termination_date(data):
    # Convert 'Actual Termination date' to datetime format
    if 'Actual Termination date' in data.columns:
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')

        today = pd.Timestamp(datetime.now().date())
        end_of_2024 = pd.Timestamp('2024-12-31')

        # Filter employees based on termination date criteria
        filtered_data = data[
            (data['Actual Termination date'].isna()) |
            ((data['Actual Termination date'] > today) &
             (data['Actual Termination date'] <= end_of_2024))
        ]
        return filtered_data
    else:
        print('Actual Termination Date column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame

try:
    # Load the Excel file
    csv_data = pd.read_excel(file_path)

    # Filter data based on termination date
    filtered_data = filter_by_termination_date(csv_data)

    # Get the total number of rows after filtering by termination date
    total_rows_filtered = filtered_data.shape[0]
    print(f'Total number of records after filtering by termination date: {total_rows_filtered}')

    # Convert the Joining Date column to datetime format
    joining_date_column = 'Date of Joining'
    filtered_data[joining_date_column] = pd.to_datetime(filtered_data[joining_date_column], format='%d-%b-%Y', errors='coerce', dayfirst=True)

    # Check for missing or invalid dates
    invalid_dates = filtered_data[filtered_data[joining_date_column].isna()]
    print(f'Number of records with missing or invalid dates after filtering: {invalid_dates.shape[0]}')

    # Filter rows for various date ranges
    count_2024 = filtered_data[filtered_data[joining_date_column].dt.year == 2024].shape[0]
    count_filtered_1_3 = filtered_data[filtered_data[joining_date_column].dt.year.isin([2023, 2022, 2021])].shape[0]
    count_filtered_3_5 = filtered_data[filtered_data[joining_date_column].dt.year.isin([2020, 2019, 2018])].shape[0]
    count_filtered_5_9 = filtered_data[(filtered_data[joining_date_column].dt.year >= 2015) & (filtered_data[joining_date_column].dt.year <= 2019)].shape[0]
    count_filtered_15_plus = filtered_data[filtered_data[joining_date_column].dt.year <= 2009].shape[0]

    # Calculate percentages
    percentage_2024 = (count_2024 / total_rows_filtered) * 100
    percentage_filtered_1_3 = (count_filtered_1_3 / total_rows_filtered) * 100
    percentage_filtered_3_5 = (count_filtered_3_5 / total_rows_filtered) * 100
    percentage_filtered_5_9 = (count_filtered_5_9 / total_rows_filtered) * 100
    percentage_filtered_15_plus = (count_filtered_15_plus / total_rows_filtered) * 100

    # Print results
    print(f'Number of employees with a joining date in the year 2024: {count_2024}')
    print(f'Percentage of employees with a joining date in 2024: {percentage_2024:.2f}%')

    print(f'Number of employees with joining dates in the years 2021, 2022, 2023: {count_filtered_1_3}')
    print(f'Percentage of employees with joining dates in 2021-2023: {percentage_filtered_1_3:.2f}%')

    print(f'Number of employees with joining dates in the years 2018, 2019, 2020: {count_filtered_3_5}')
    print(f'Percentage of employees with joining dates in 2018-2020: {percentage_filtered_3_5:.2f}%')

    print(f'Number of employees with joining dates between 2015 and 2019 (5-9 years of service): {count_filtered_5_9}')
    print(f'Percentage of employees with joining dates in 2015-2019: {percentage_filtered_5_9:.2f}%')

    print(f'Number of employees with joining dates in 2008 or earlier (greater than 15 years): {count_filtered_15_plus}')
    print(f'Percentage of employees with joining dates in 2008 or earlier: {percentage_filtered_15_plus:.2f}%')

    # Verify summed counts
    total_count_computed = (count_2024 + count_filtered_1_3 + count_filtered_3_5 + count_filtered_5_9 + count_filtered_15_plus)
    print("Sum of all Employees computed above", total_count_computed)

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
