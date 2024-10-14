import pandas as pd
import os

def fte_actual_total(month_input):
    file_path = '../data_hcm/Headcount Report-Cost Center-Final.xlsx'

    # Check if the file exists before attempting to read it
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is not found

    excel_data = pd.read_excel(file_path, header=None)

    # List of months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if month_input == 'all':
        month_indices = range(1, 13)  # 1 to 12 for all months
    else:
        if month_input < 1 or month_input > 12:
            print("Invalid month index. Please provide a number between 1 (January) and 12 (December) or 'all'.")
            return
        month_indices = [month_input]

    for month_index in month_indices:
        month = months[month_index - 1]  # Get the month name based on index
        total_actual_fte = 0

        # Collecting Actual Data (FTE)
        for col in range(1, excel_data.shape[1]):
            if (excel_data.iloc[10, col] == 'Actual' and
                    excel_data.iloc[12, col] == month):  # Check for the current month

                column_values = excel_data.iloc[13:, col]

                if excel_data.iloc[11, col] == 'FTE':
                    # Process Actual FTE
                    for value in column_values:
                        try:
                            actual_fte = float(value)
                            total_actual_fte += actual_fte
                        except ValueError:
                            pass

        print(f"FTE for {month}: {int(total_actual_fte)}")  # Convert to int for no decimal places


# Example usage:
fte_actual_total(1)  # Call the function for January
fte_actual_total('all')
