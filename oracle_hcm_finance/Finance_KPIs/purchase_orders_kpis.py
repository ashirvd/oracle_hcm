import pandas as pd
import os
def purchase_orders(month):
    # List of file paths
    file_paths = [
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_1 (1).xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_2.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_3.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_4.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_5.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_6.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_7.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_8.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_9.xlsx'
    ]

    # Check if the input is 'all'
    if month == 'all':
        for i in range(1, 10):
            purchase_orders(i)
            print()  # Add a line break after each month
        return

    # Check if the month is valid
    if month < 1 or month > 9:
        print("Invalid month number. Please provide a month between 1 and 9 or 'all'.")
        return

    # Get the corresponding file path
    file_path = file_paths[month - 1]
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    try:
        # Load the Excel file, specifying the header row (row 11)
        excel_data = pd.read_excel(file_path, header=10, engine='openpyxl')

        # Print the month name based on the month number
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September"
        ]
        print(f'Month: {month_names[month - 1]}')

        # List of target columns
        target_columns = ["AOG", "Urgent", "Normal"]

        # Ensure the target columns exist in the dataframe
        existing_columns = [col for col in target_columns if col in excel_data.columns]

        if existing_columns:
            # Get the values from the first row for the existing target columns
            row_values = excel_data.loc[0, existing_columns]

            # Convert values to numeric and handle missing values
            row_values = pd.to_numeric(row_values, errors='coerce')

            # Sum the values for the row
            row_sum = row_values.sum()

            # Print values and percentages in the desired format
            for column in existing_columns:
                if column in row_values:
                    value = row_values[column]
                    if row_sum > 0:
                        percentage = (value / row_sum) * 100
                        print(f'{column} {value:} ({percentage:.2f}%)')
                    else:
                        print(f'{column} {value:} (0%)')
        else:
            print(f'None of the target columns "{", ".join(target_columns)}" found in the dataset.')

    except FileNotFoundError:
        print(f'The specified file was not found: {file_path}')
    except Exception as e:
        print(f'An error occurred while processing {file_path}: {e}')

# Example usage:
purchase_orders(1)  # Call the function for January
#purchase_orders('all')  # Call the function for all months
