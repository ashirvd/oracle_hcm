from datetime import datetime
import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def saudization_filter_by_date(df, year=None, month=None, quarter=None):
    if 'Date of Joining' in df.columns:
        # Convert 'Date of Joining' to datetime format for filtering purposes
        df = df.copy()  # Make a copy to avoid modifying the original DataFrame
        df['Date of Joining'] = pd.to_datetime(df['Date of Joining'], format='%d-%b-%Y')

        if year is not None:
            # Extract the year part from the date
            df['Year'] = df['Date of Joining'].dt.year
            df = df[df['Year'] == year]

        if month is not None:
            # Extract the month part from the date
            df['Month'] = df['Date of Joining'].dt.month
            df = df[df['Month'] == month]

        if quarter is not None:
            # Extract the month part from the date
            df['Month'] = df['Date of Joining'].dt.month
            # Define months in each quarter
            months_in_quarter = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in months_in_quarter:
                df = df[df['Month'].isin(months_in_quarter[quarter])]

    return df


def analyze_nationality(df):
    # Define today's date and end of 2024
    today = pd.Timestamp(datetime.now().date())
    end_of_2024 = pd.Timestamp('2024-12-31')

    if 'Actual Termination date' in df.columns:
        df['Actual Termination date'] = pd.to_datetime(df['Actual Termination date'], format='%d-%b-%Y',
                                                       errors='coerce')

        # Filter employees based on termination date criteria
        filtered_data = df[
            (df['Actual Termination date'].isna()) |
            ((df['Actual Termination date'] > today) &
             (df['Actual Termination date'] <= end_of_2024))
            ]

        # Get the total number of rows after filtering by termination date
        filtered_total_rows = filtered_data.shape[0]
        print(f'Total number of records after date filtering: {filtered_total_rows}')

        # Check if the Nationality column exists
        if 'Nationality' in filtered_data.columns:
            saudia_count = filtered_data[filtered_data['Nationality'] == 'Saudi Arabia'].shape[0]
            non_saudia_count = filtered_total_rows - saudia_count

            # Calculate the percentage of Saudi nationals
            saudia_percentage = (saudia_count / filtered_total_rows) * 100

            # Print the counts and the percentage
            print(f'Total number of Saudia employees: {saudia_count}')
            print(f'Total number of Non-Saudi employees: {non_saudia_count}')
            print(f'Percentage of Saudia employees: {saudia_percentage:.1f}%')

        else:
            print('Nationality column not found in the dataset.')
    else:
        print('Actual Termination Date column not found in the dataset.')


try:
    csv_data = pd.read_excel(file_path)  # Try different encodings if necessary

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    year = None
    month = None
    quarter = None

    # Filter data by date
    filtered_data = saudization_filter_by_date(csv_data, year=year, month=month, quarter=quarter)

    # Analyze nationality for filtered data
    analyze_nationality(filtered_data)

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')