import pandas as pd

# Specify the path to your file (make sure it’s a CSV)
file_path = r'C:\Users\ashir.afzal_ventured\OneDrive_1_06-10-2024\Procurement Monthly Report_1 (1).xls'

# Attempt to load the file
try:
    # Load the CSV file
    excel_data = pd.read_csv(file_path)

    # Display the first few rows to understand the structure (optional)
    print("Preview of the data:")
    print(excel_data.head())

    # List of target columns
    target_columns = ["AOG", "Urgent", "Normal"]

    # Ensure the target columns exist in the dataframe
    existing_columns = [col for col in target_columns if col in excel_data.columns]

    if existing_columns:
        # Calculate the total for each of the existing columns
        for column in existing_columns:
            total_value = excel_data[column].sum()  # Sum the values in the column
            print(f'Total value for "{column}": {total_value:.2f}')
    else:
        print(f'None of the target columns "{", ".join(target_columns)}" found in the dataset.')

except FileNotFoundError:
    print('The specified file was not found.')
except Exception as e:
    print(f'An error occurred: {e}')
