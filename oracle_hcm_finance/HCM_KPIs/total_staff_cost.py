import pandas as pd
import os


def total_staff_cost_summary(month_input):
    file_path = '../data_hcm/Headcount Report-Cost Center-Final.xlsx'

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    excel_data = pd.read_excel(file_path, header=None)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if month_input == 'all':
        month_indices = range(1, 11)
    elif 1 <= month_input <= 12:
        month_indices = [month_input]
    else:
        print("Invalid month index. Please provide a number between 1 and 12 or 'all'.")
        return

    for month_index in month_indices:
        month = months[month_index - 1]
        total_budget_expense = total_actual_expense = 0

        # Collect budget and actual expenses for the month
        for col in range(1, excel_data.shape[1]):
            if excel_data.iloc[12, col] == month:
                try:
                    value = excel_data.iloc[13:, col].astype(float).sum()
                    if excel_data.iloc[10, col] == 'Budget' and excel_data.iloc[11, col] == 'Employees Expenses':
                        total_budget_expense += value
                    elif excel_data.iloc[10, col] == 'Actual' and excel_data.iloc[11, col] == 'Employees Expenses':
                        total_actual_expense += value
                except ValueError:
                    pass

        print(f"Month: {month}")
        print(f"Total Budget Expense: {total_budget_expense / 1_000_000:.2f}M")
        print(f"Total Actual Expense: {total_actual_expense / 1_000_000:.2f}M\n")


# Example usage:
total_staff_cost_summary(1)  # January
total_staff_cost_summary('all')  # All months
