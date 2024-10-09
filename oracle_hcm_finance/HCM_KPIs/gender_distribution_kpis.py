import pandas as pd
from datetime import datetime

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

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
    data = pd.read_excel(file_path)

    # Filter data based on termination date
    filtered_data = filter_by_termination_date(data)

    # Get the total number of rows after filtering by termination date
    total_rows_filtered = filtered_data.shape[0]
    print(f'Total number of records after filtering by termination date: {total_rows_filtered}')

    # Check if the Gender column exists
    if 'Gender' in filtered_data.columns:
        # Count the number of employees by gender
        gender_counts = filtered_data['Gender'].value_counts()

        # Calculate and print counts and percentages
        total_gender_counts = {
            'Male': gender_counts.get('Male', 0),
            'Female': gender_counts.get('Female', 0),
        }
        other_gender_count = total_rows_filtered - sum(total_gender_counts.values())

        print(f'Total number of employees with gender Male: {total_gender_counts["Male"]}')
        print(f'Total number of employees with gender Female: {total_gender_counts["Female"]}')
        print(f'Total number of employees with other genders: {other_gender_count}')

        # Calculate percentages
        percentage_male = (total_gender_counts['Male'] / total_rows_filtered) * 100
        percentage_female = (total_gender_counts['Female'] / total_rows_filtered) * 100

        print(f'Percentage of employees with gender Male: {percentage_male:.2f}%')
        print(f'Percentage of employees with gender Female: {percentage_female:.2f}%')

    else:
        print('Gender column not found in the filtered data.')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')