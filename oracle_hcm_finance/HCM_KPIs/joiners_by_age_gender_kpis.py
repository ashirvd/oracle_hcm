import pandas as pd

file_path = '../datasources/PromotionbyGender.csv'

try:
    # Load the CSV file
    csv_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')  # Try different encodings if necessary

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of employee records in the CSV file: {total_rows}')

    # Filter rows where 'Date of Joining' is not empty
    joining_date_data = csv_data[csv_data['Date of Joining'].notna()].copy()

    # Convert 'Age' column to numeric, handling errors by coercing to NaN
    joining_date_data['Age'] = pd.to_numeric(joining_date_data['Age'], errors='coerce')

    # Define age bins and labels
    age_bins = [0, 24, 34, 44, 59, float('inf')]
    age_labels = ['<25', '25-34', '35-44', '45-59', '>=60']

    # Categorize ages into bins
    joining_date_data['Age Category'] = pd.cut(joining_date_data['Age'], bins=age_bins, labels=age_labels)

    # Group by 'Gender' and 'Age Category' and count the records, explicitly setting observed=False
    age_gender_counts = joining_date_data.groupby(['Age Category', 'Gender'], observed=False).size().unstack(fill_value=0)

    # Display the counts of employees by age category and gender
    print("Counts of employees by age category and gender:")
    print(age_gender_counts)

except Exception as e:
    print(f'An error occurred: {e}')
