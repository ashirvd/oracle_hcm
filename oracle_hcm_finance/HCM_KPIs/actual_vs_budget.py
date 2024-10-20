import pandas as pd
import os
def actual_vs_budget(month_input):
    # Define the file path inside the function
    file_path = '../data_hcm/Headcount Report-Cost Center-Final.xlsx'
    # Check if the file exists before attempting to read it

    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    excel_data = pd.read_excel(file_path, header=None)

    # List of months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

    if month_input == 'all':
        month_indices = range(1, 11)
    else:
        # Check if the month index is valid
        if month_input < 1 or month_input > 12:
            print("Invalid month index. Please provide a number between 1 (January) and 12 (December) or 'all'.")
            return
        month_indices = [month_input]

    for month_index in month_indices:
        month = months[month_index - 1]  # Get the month name based on index
        total_budget_expense = 0  # Initialize total for the month
        total_actual_expense = 0  # Initialize total actual expense for the month

        # Collecting Budget Expenses
        for col in range(1, excel_data.shape[1]):
            if (excel_data.iloc[10, col] == 'Budget' and  # Row 11 is index 10 in pandas
                    excel_data.iloc[11, col] == 'Employees Expenses' and  # Row 12 is index 11
                    excel_data.iloc[12, col] == month):  # Row 13 is index 12 for the current month

                column_values = excel_data.iloc[13:, col]

                for value in column_values:
                    try:
                        budget_value = float(value)
                        total_budget_expense += budget_value  # Accumulate the total budget expense
                    except ValueError:
                        pass

        # Collecting Actual Expenses
        for col in range(1, excel_data.shape[1]):
            if (excel_data.iloc[10, col] == 'Actual' and  # Row 11 is index 10 in pandas
                    excel_data.iloc[11, col] == 'Employees Expenses' and  # Row 12 is index 11
                    excel_data.iloc[12, col] == month):  # Row 13 is index 12 for the current month

                column_values = excel_data.iloc[13:, col]

                for value in column_values:
                    try:
                        actual_value = float(value)
                        total_actual_expense += actual_value  # Accumulate the total actual expense
                    except ValueError:
                        pass

        # Calculate percentage
        if total_budget_expense > 0:  # Avoid division by zero
            percentage = (total_actual_expense / total_budget_expense) * 100
            print(f"\nMonth: {month}")
            print(f"Total Budget Expense: {total_budget_expense / 1_000_000:.2f}M")
            print(f"Total Actual Expense: {total_actual_expense / 1_000_000:.2f}M")
            print(f"Percentage of Actual Expenses to Budget: {percentage:.2f}%")
        else:
            print(f"\nMonth: {month}")
            print("No budget expenses recorded.")

# Example usage:
# Call the function for January (1)
actual_vs_budget(1)

# Call the function for all months
actual_vs_budget('all')
