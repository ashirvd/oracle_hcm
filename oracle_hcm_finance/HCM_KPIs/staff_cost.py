import pandas as pd

def staff_cost(month):
    # Define the file paths inside the function
    file_paths = [
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Jan.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Feb.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Mar.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Apr.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_May.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Jun.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Jul.xlsx',
        '../data_hcm/HCReportCC/Headcount Report-Cost Center_Aug.xlsx'
    ]

    # List of month names
    month_names = [
        "January", "February", "March", "April", "May", "June", "July","August"
    ]

    # Check if the month index is valid
    if month < 1 or month > len(file_paths):
        print(f'Invalid month index. Please provide a number between 1 and {len(file_paths)}.')
        return

    # Print the file being processed
    file_path = file_paths[month - 1]  # Adjust for zero-based index
    month_name = month_names[month - 1]  # Get the corresponding month name
    print(f"\nProcessing file for month: {month_name} ")

    # Read the Excel file, starting from row 14
    try:
        # Load the data starting from the 14th row
        excel_data = pd.read_excel(file_path, header=12, usecols=[0, 1, 2])

        # Rename the columns for easier access
        excel_data.columns = ['Data Name', 'Budget Expense', 'Actual Expense']

        # Calculate the totals before formatting
        total_budget_expense = excel_data['Budget Expense'].sum() / 1_000_000
        total_actual_expense = excel_data['Actual Expense'].sum() / 1_000_000

        # Convert 'Budget Expense' and 'Actual Expense' to millions, and format them to show two decimal places with 'M'
        excel_data['Budget Expense'] = (excel_data['Budget Expense'] / 1_000_000).map('{:.2f}M'.format)
        excel_data['Actual Expense'] = (excel_data['Actual Expense'] / 1_000_000).map('{:.2f}M'.format)

        # Sort the data by 'Data Name' in ascending alphabetical order
        excel_data = excel_data.sort_values(by='Data Name')

        # Print the dataframe with fixed-width formatting
        print("{:<30} {:>30} {:>30}".format("Data Name", "Budget Expense", "Actual Expense"))
        for index, row in excel_data.iterrows():
            print("{:<30} {:>30} {:>30}".format(row['Data Name'], row['Budget Expense'], row['Actual Expense']))

        # Print the totals
        print(f"\nTotal Budget Expense: {total_budget_expense:.2f}M")
        print(f"Total Actual Expense: {total_actual_expense:.2f}M")

    except FileNotFoundError:
        print(f'The file at path "{file_path}" was not found.')
    except Exception as e:
        print(f'An error occurred while reading the Excel file: {e}')

staff_cost(8)

