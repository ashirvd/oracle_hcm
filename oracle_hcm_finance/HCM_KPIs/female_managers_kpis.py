import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

try:
    # Load the CSV file with specified delimiter and encoding
    csv_data = pd.read_excel(file_path)

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    # Ensure that the Gender and Grade columns exist and are formatted correctly
    gender_column = 'Gender'
    grade_column = 'Grade'

    # Define the grades to filter
    valid_grades = ['C2', 'T5' ,'6', '7', '8', '9', '10', '11', '12', 'CEO']

    # Filter the DataFrame for female employees with specific grades
    filtered_data = csv_data[(csv_data[gender_column].str.lower() == 'female') &
                             (csv_data[grade_column].astype(str).isin(valid_grades))]

    # Get the count of filtered rows
    female_grade_count = filtered_data.shape[0]
    print(f'Number of female employees with grades 6-12 or CEO: {female_grade_count}')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')


import pandas as pd

def filter_employees(data, year=None, month=None, quarter=None):
    # Check if 'Date of Joining' column exists in the data
    if 'Date of Joining' in data.columns:
        # Convert 'Date of Joining' to datetime format
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        # Remove rows where 'Date of Joining' couldn't be parsed
        data = data.dropna(subset=['Date of Joining'])

        # Filter employees with Date of Joining up to the end of 2024
        if year is not None:
            end_of_year = pd.Timestamp(year, 12, 31)
            filtered_data = data[data['Date of Joining'] <= end_of_year]
        else:
            filtered_data = data

        # Check for 'Actual Termination date' column and filter rows with blank termination dates
        if 'Actual Termination date' in filtered_data.columns:
            filtered_data['Actual Termination date'] = pd.to_datetime(filtered_data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            # Keep employees with a blank termination date
            filtered_data = filtered_data[filtered_data['Actual Termination date'].isna()]
        else:
            print('Actual Termination Date column is not in the dataset.')

        # Filter by valid grades
        grade_column = 'Grade'
        valid_grades = ['C2', 'T5', '6', '7', '8', '9', '10', '11', '12', 'CEO']
        if grade_column in filtered_data.columns:
            filtered_data = filtered_data[filtered_data[grade_column].astype(str).isin(valid_grades)]
        else:
            print('Grade column is not in the dataset.')

        # Filter by gender (female)
        gender_column = 'Gender'
        if gender_column in filtered_data.columns:
            filtered_data = filtered_data[filtered_data[gender_column].str.lower() == 'female']
        else:
            print('Gender column is not in the dataset.')

        return filtered_data

    else:
        print('Date of Joining column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame

def count_filtered_employees(file_path, year=None, month=None, quarter=None):
    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Count total employees
        total_employees = data.shape[0]

        # Filter data based on the criteria
        filtered_data = filter_employees(data, year=year, month=month, quarter=quarter)

        # Count employees who meet the filter criteria
        filtered_count = filtered_data.shape[0]

        # Count terminated employees
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            terminated_employees = data[data['Actual Termination date'].notna()].shape[0]
        else:
            terminated_employees = 0

        # Display filtered data count
        print(f'Total number of employees in the sheet: {total_employees}')
        print(f'Total number of employees matching the filter criteria (joined up to 2024, specific grades, female, no termination date): {filtered_count}')

        return total_employees, filtered_count, terminated_employees

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0, 0, 0

# Example usage
file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'
total_employees, filtered_count, terminated_employees = count_filtered_employees(file_path, year=2024)
