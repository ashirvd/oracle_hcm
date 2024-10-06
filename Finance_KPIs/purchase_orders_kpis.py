import pandas as pd

file_path = '../datasources/finance/Procurement Monthly Report_latest.xlsx'

# Attempt to load the Excel file
try:
    # Load the Excel file
    excel_data = pd.read_excel(file_path, header=10)  # Adjust header row if necessary

    # Get the total number of rows
    total_rows = excel_data.shape[0]
    print(f'Total number of records in the Excel file: {total_rows}')

    # Print the column names
    print("Column names in the Excel file:")
    print(excel_data.columns.tolist())

    # List of target columns
    target_columns = ["AOG", "Urgent", "Normal"]

    # Ensure the target columns exist in the dataframe
    existing_columns = [col for col in target_columns if col in excel_data.columns]

    if existing_columns:
        # Get the values from the first row
        row_values = excel_data.loc[0, existing_columns]

        # Print the values from the first row
        print(f'\nValues in the first row for columns {existing_columns}:')
        print(row_values)

        # Convert values to numeric and handle missing values
        row_values = pd.to_numeric(row_values, errors='coerce')

        # Sum the values for the row
        row_sum = row_values.sum()
        print(f'\nSum of values for the first row: {row_sum:.2f}')

        # Calculate percentages for each column
        if row_sum > 0:
            for column in existing_columns:
                percentage = (row_values[column] / row_sum) * 100
                print(f'Percentage of "{column}": {percentage:.2f}%')
        else:
            print('Total sum for the row is zero or no valid values found.')

    else:
        print(f'None of the target columns "{", ".join(target_columns)}" found in the dataset.')

except FileNotFoundError:
    print('The specified file was not found.')
except Exception as e:
    print(f'An error occurred: {e}')
