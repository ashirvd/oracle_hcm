import pandas as pd
from datetime import datetime

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def filter_by_date(data, year=None, month=None, quarter=None):
    if 'Date of Joining' in data.columns:
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        data = data.dropna(subset=['Date of Joining'])

        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            today = pd.Timestamp(datetime.now().date())
            end_of_2024 = pd.Timestamp('2025-12-31')
            filtered_data = data[
                (data['Actual Termination date'].isna()) |
                ((data['Actual Termination date'] > today) &
                 (data['Actual Termination date'] <= end_of_2024))
                ]
        else:
            print('Actual Termination Date column is not in the dataset.')
            filtered_data = data

        if year is not None:
            end_of_year = pd.Timestamp(year, 12, 31)
            filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_year]

            if month is not None:
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_month]

        elif month is not None:
            filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month == month]

        if quarter is not None:
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in quarters:
                filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month.isin(quarters[quarter])]

        return filtered_data
    else:
        print('Date of Joining column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame

try:
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Filter the data by date criteria
    filtered_data = filter_by_date(data, year=None, month=None, quarter=None)

    # Get the total number of rows after filtering by date
    total_rows = filtered_data.shape[0]
    print(f'Total number of records after filtering by date: {total_rows}')

    # Check if the Gender and Grade columns exist
    if 'Gender' in filtered_data.columns and 'Grade' in filtered_data.columns:
        # Filter the data to include only Male and Female genders
        filtered_data = filtered_data[filtered_data['Gender'].isin(['Male', 'Female'])]

        # Group by Grade and Gender, then count occurrences
        grade_gender_counts = filtered_data.groupby(['Grade', 'Gender']).size().unstack(fill_value=0)

        # Calculate total count per grade and add it as a column
        grade_gender_counts['Total'] = grade_gender_counts.sum(axis=1)

        # Sort the DataFrame by the Total column in descending order
        sorted_counts = grade_gender_counts.sort_values(by='Total', ascending=False)

        # Print counts of Male and Female by Grade with the Total column
        print('Count of employees by Grade and Gender')
        print(sorted_counts)
    else:
        print('Missing columns Gender or Grade in the dataset.')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
