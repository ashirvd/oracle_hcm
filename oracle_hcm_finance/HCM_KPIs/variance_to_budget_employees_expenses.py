import pandas as pd
import os

def variance_to_budget(month_input):
    # Define the file path inside the function
    file_path = '../data_hcm/Headcount Report-Cost Center-Final.xlsx'

    # Check if the file exists before attempting to read it
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    excel_data = pd.read_excel(file_path, header=None)

    # List of months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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

        results = []  # Store the category name and variance for sorting

        # Loop through each category in column 1 (starting from row 13)
        for row in range(13, excel_data.shape[0]):
            category_name = excel_data.iloc[row, 0]  # Category names are in column 1

            total_budget_expense = 0
            total_actual_expense = 0

            # Collecting Budget Expenses for the category
            for col in range(1, excel_data.shape[1]):
                if (excel_data.iloc[10, col] == 'Budget' and  # Row 11 is index 10 in pandas
                        excel_data.iloc[11, col] == 'Employees Expenses' and  # Row 12 is index 11
                        excel_data.iloc[12, col] == month):  # Row 13 is index 12 for the current month

                    try:
                        budget_value = float(excel_data.iloc[row, col])  # Get budget value for the category
                        total_budget_expense += budget_value
                    except ValueError:
                        pass

            # Collecting Actual Expenses for the category
            for col in range(1, excel_data.shape[1]):
                if (excel_data.iloc[10, col] == 'Actual' and  # Row 11 is index 10 in pandas
                        excel_data.iloc[11, col] == 'Employees Expenses' and  # Row 12 is index 11
                        excel_data.iloc[12, col] == month):  # Row 13 is index 12 for the current month

                    try:
                        actual_value = float(excel_data.iloc[row, col])  # Get actual value for the category
                        total_actual_expense += actual_value
                    except ValueError:
                        pass

            # Calculate variance for this category
            variance = total_actual_expense - total_budget_expense

            # Append the result for sorting later
            results.append((category_name, variance / 1_000_000))  # Store in millions (M)

        # Sort the results by variance (most negative values first)
        results_sorted = sorted(results, key=lambda x: x[1])  # Sorting by variance (x[1]) in ascending order

        # Print the month and table header
        print(f"\nMonth: {month}")
        print(f"{'Category Name':<30} {'Variance':>15}")
        print("-" * 50)

        # Output the sorted results in table format
        for category_name, variance in results_sorted:
            print(f"{category_name:<30} {variance:>15.2f}M")

# Example usage:
# Call the function for January (1)
variance_to_budget(1)

# Call the function for all months
variance_to_budget('all')
