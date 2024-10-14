import pandas as pd
import os
def staff_cost(month_input):
    file_path = '../data_hcm/Headcount Report-Cost Center-Final.xlsx'
    # Check if the file exists before attempting to read it
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    excel_data = pd.read_excel(file_path, header=None)

    # List of months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Function to extract values starting from row 14 in column 1
    def get_column_1_from_row_14():
        return excel_data.iloc[13:, 0]  # Row 14 in Excel is index 13 in pandas

    if month_input == 'all':
        month_indices = range(1, 11)
    else:
        if month_input < 1 or month_input > 12:
            print("Invalid month index. Please provide a number between 1 (January) and 12 (December) or 'all'.")
            return
        month_indices = [month_input]

    for month_index in month_indices:
        month = months[month_index - 1]  # Get the month name based on index
        month_data = []
        total_budget_expense = total_actual_expense = 0
        total_budget_fte = total_actual_fte = 0

        # Collecting Budget Data (Expense and FTE)
        for col in range(1, excel_data.shape[1]):
            if (excel_data.iloc[10, col] == 'Budget' and
                excel_data.iloc[12, col] == month):  # Check for the current month

                column_values = excel_data.iloc[13:, col]
                category_names = get_column_1_from_row_14().tolist()

                if excel_data.iloc[11, col] == 'Employees Expenses':
                    # Process Budget Expenses
                    for idx, value in enumerate(column_values):
                        try:
                            budget_value = float(value)
                            category = category_names[idx] if idx < len(category_names) else 'Unknown Category'
                            month_data.append({
                                'Data Name': category,
                                'Budget Expense': f"{budget_value / 1_000_000:.2f}M",
                                'Actual Expense': 'N/A',  # Placeholder for actual expense
                                'FTE Budget': 'N/A',  # Placeholder for FTE
                                'FTE Actual': 'N/A'  # Placeholder for FTE
                            })
                            total_budget_expense += budget_value
                        except ValueError:
                            pass

                elif excel_data.iloc[11, col] == 'FTE':
                    # Process Budget FTE
                    for idx, value in enumerate(column_values):
                        try:
                            budget_fte = float(value)
                            if idx < len(month_data):
                                month_data[idx]['FTE Budget'] = f"{budget_fte:.2f}"
                            total_budget_fte += budget_fte
                        except ValueError:
                            pass

        # Collecting Actual Data (Expense and FTE)
        for col in range(1, excel_data.shape[1]):
            if (excel_data.iloc[10, col] == 'Actual' and
                excel_data.iloc[12, col] == month):  # Check for the current month

                column_values = excel_data.iloc[13:, col]

                if excel_data.iloc[11, col] == 'Employees Expenses':
                    # Process Actual Expenses
                    for idx, value in enumerate(column_values):
                        try:
                            actual_value = float(value)
                            if idx < len(month_data):
                                month_data[idx]['Actual Expense'] = f"{actual_value / 1_000_000:.2f}M"
                            total_actual_expense += actual_value
                        except ValueError:
                            pass

                elif excel_data.iloc[11, col] == 'FTE':
                    # Process Actual FTE
                    for idx, value in enumerate(column_values):
                        try:
                            actual_fte = float(value)
                            if idx < len(month_data):
                                month_data[idx]['FTE Actual'] = f"{actual_fte:.2f}"
                            total_actual_fte += actual_fte
                        except ValueError:
                            pass

        # Add total row for the month
        month_data.append({
            'Data Name': 'Total',
            'Budget Expense': f"{total_budget_expense / 1_000_000:.2f}M",
            'Actual Expense': f"{total_actual_expense / 1_000_000:.2f}M",
            'FTE Budget': f"{total_budget_fte:.2f}",
            'FTE Actual': f"{total_actual_fte:.2f}"
        })

        # Create DataFrame, sort by 'Data Name', and print results
        df = pd.DataFrame(month_data)
        df_sorted = df.sort_values(by='Data Name')  # Sort by 'Data Name'
        print(f"\nMonth: {month}")
        print(df_sorted.to_string(index=False))

# Example usage:
staff_cost(1)  # Call the function for January
staff_cost('all')