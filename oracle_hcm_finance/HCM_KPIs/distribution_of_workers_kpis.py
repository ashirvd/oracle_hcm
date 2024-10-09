import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

# Attempt to load the CSV file with a different encoding
try:
    csv_data = pd.read_excel(file_path)  # Try different encodings if necessary

    # Ensure the 'Age' column is treated as numeric, converting errors to NaN
    csv_data['Age'] = pd.to_numeric(csv_data['Age'], errors='coerce')

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    # Count records with empty Age
    empty_age_count = csv_data['Age'].isna().sum()
    # Count employees with Age < 25
    age_under_25_count = csv_data[csv_data['Age'] < 25].shape[0]
    # Count employees with Age 25-34
    age_25_34_count = csv_data[(csv_data['Age'] >= 25) & (csv_data['Age'] <= 34)].shape[0]
    # Count employees with Age 35-44
    age_35_44_count = csv_data[(csv_data['Age'] >= 35) & (csv_data['Age'] <= 44)].shape[0]
    # Count employees with Age 45-59
    age_45_59_count = csv_data[(csv_data['Age'] >= 45) & (csv_data['Age'] <= 59)].shape[0]
    # Count employees with Age > 60
    age_over_60_count = csv_data[csv_data['Age'] >= 60].shape[0]

    # Calculate percentages
    empty_age_percentage = (empty_age_count / total_rows) * 100
    age_under_25_percentage = (age_under_25_count / total_rows) * 100
    age_25_34_percentage = (age_25_34_count / total_rows) * 100
    age_35_44_percentage = (age_35_44_count / total_rows) * 100
    age_45_59_percentage = (age_45_59_count / total_rows) * 100
    age_over_60_percentage = (age_over_60_count / total_rows) * 100

    # Print results
    print(f'Number of records with empty Age: {empty_age_count} ({empty_age_percentage:.2f}%)')
    print(f'Number of employees with Age < 25: {age_under_25_count} ({age_under_25_percentage:.2f}%)')
    print(f'Number of employees with Age 25-34: {age_25_34_count} ({age_25_34_percentage:.2f}%)')
    print(f'Number of employees with Age 35-44: {age_35_44_count} ({age_35_44_percentage:.2f}%)')
    print(f'Number of employees with Age 45-59: {age_45_59_count} ({age_45_59_percentage:.2f}%)')
    print(f'Number of employees with Age >= 60: {age_over_60_count} ({age_over_60_percentage:.2f}%)')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
