import pandas as pd

def actual_vs_budget(month):
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
        "January", "February", "March", "April", "May", "June", "July", "August"
    ]

    # Check if the month index is valid
    if month < 1 or month > len(file_paths):
        print(f'Invalid month index. Please provide a number between 1 and {len(file_paths)}.')
        return

    # Read the Excel file, starting from row 14
    file_path = file_paths[month - 1]  # Adjust for zero-based index

    # Load the data starting from the 14th row
    try:
        # Read the data
        excel_data = pd.read_excel(file_path, header=12, usecols=[0, 1, 2])

        # Rename the columns for easier access
        excel_data.columns = ['Data Name', 'Budget Expense', 'Actual Expense']

        # Calculate the totals
        total_budget_expense = excel_data['Budget Expense'].sum()
        total_actual_expense = excel_data['Actual Expense'].sum()

        # Calculate the percentage
        if total_budget_expense == 0:  # Prevent division by zero
            print("Total Budget Expense is zero, cannot calculate percentage.")
            return

        percentage = (total_actual_expense / total_budget_expense) * 100

        month_name = month_names[month - 1]  # Get the corresponding month name
        print(f"Percentage for the {month_name} is {percentage:.2f}%")

    except FileNotFoundError:
        print(f'The file at path "{file_path}" was not found.')
    except Exception as e:
        print(f'An error occurred while reading the Excel file: {e}')

# Example usage
actual_vs_budget(1)
