import pandas as pd

file_path = '../datasources/PromotionbyGender.csv'

try:
    csv_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    termination_column = 'Termination / Resignation'
    non_empty_count = csv_data[termination_column].notna().sum()
    print(f'Total number of leavers are : {non_empty_count}')

    # Convert 'Age' column to numeric, coercing errors
    age_column = 'Age'
    csv_data[age_column] = pd.to_numeric(csv_data[age_column], errors='coerce')

    # Define age bins and labels
    age_bins = [0, 24, 34, 44, 59, float('inf')]
    age_labels = ['<25', '25-34', '35-44', '45-59', '>60']

    # Create a new column for age categories
    csv_data['Age Category'] = pd.cut(csv_data[age_column], bins=age_bins, labels=age_labels, right=True)

    # Filter rows where 'Termination/ Resignation' is not empty
    filtered_data = csv_data[csv_data[termination_column].notna()]

    # Count records based on age category and gender
    age_gender_counts = filtered_data.groupby(['Age Category', 'Gender'], observed=False).size().unstack(fill_value=0)

    # Print results
    print(age_gender_counts)

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
