import pandas as pd
import os
def receivables_ageing(month_index):
    # Define file paths for each month
    file_paths = [
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_JAN2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_FEB2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_MAR2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_APR2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_MAY2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_JUN2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_JUL2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_AUG2024.xlsx',
        r'..\data_finance\AR Aging Summary Report_monthwiseoutput11092024\AR Aging Summary Report_Customer Level Detail_till11SEP2024.xlsx'
    ]
    month_names = ["January", "February", "March","April", "May", "June", "July", "August", "September"]  # Corresponding month names

    # Check if 'all' is passed to process all months
    if month_index == 'all':
        for index, (file_path, month_name) in enumerate(zip(file_paths, month_names)):
            print(f"\nProcessing file of month: {month_name}")
            process_file(file_path)

    else:
        # Convert to zero-based index for accessing file_paths
        file_index = month_index - 1
        if 0 <= file_index < len(file_paths):
            print(f"\nProcessing file of month: {month_names[file_index]}")
            process_file(file_paths[file_index])
        else:
            print("Invalid month index. Please provide a valid index or 'all'.")


def process_file(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    # Attempt to load the Excel file with the header on the specified row
    try:
        # Load the Excel file (assuming the 15th row, index 14, contains headers)
        xls_data = pd.read_excel(file_path, header=14)

        # Ensure the "Not Due", "Outstanding", and "Customer Name" columns exist
        not_due_column = "Not Due"
        outstanding_column = "Outstanding"

        if not_due_column in xls_data.columns and outstanding_column in xls_data.columns:
            # Function to clean and convert values to float
            def clean_and_convert(value):
                value = str(value).replace(',', '')
                if '(' in value and ')' in value:
                    value = '-' + value.replace('(', '').replace(')', '')
                try:
                    return float(value)
                except ValueError:
                    return 0.0  # Return 0.0 for any non-numeric entries

            # Clean and convert the "Not Due" and "Outstanding" values to numeric
            xls_data[not_due_column] = xls_data[not_due_column].apply(clean_and_convert)
            xls_data[outstanding_column] = xls_data[outstanding_column].apply(clean_and_convert)

            # Exclude the last three rows (assumed total row)
            xls_data = xls_data[:-3]  # This drops the last three rows

            # Sum the "Not Due" and "Outstanding" columns
            total_not_due = xls_data[not_due_column].sum()
            total_outstanding = xls_data[outstanding_column].sum()

            # Calculate totals in millions and round
            current_amount_millions = round(total_not_due / 1_000_000)
            overdue_final_amount_millions = round((total_outstanding - total_not_due) / 1_000_000)

            # Calculate percentages
            if total_outstanding > 0:
                current_percentage = (total_not_due / total_outstanding) * 100
                overdue_percentage = 100 - current_percentage
            else:
                current_percentage = 0
                overdue_percentage = 0

            # Display final results
            print(f'Current Amount: {current_amount_millions}M ({current_percentage:.2f}%)')
            print(f'Overdue Amount: {overdue_final_amount_millions}M ({overdue_percentage:.2f}%)')

        else:
            print(f'Columns "{not_due_column}" or "{outstanding_column}" not found in the dataset.')

    except Exception as e:
        print(f'An error occurred: {e}')


receivables_ageing(1)
receivables_ageing('all')