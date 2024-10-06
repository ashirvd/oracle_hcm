import pandas as pd

def ebit(month):
    # Function to map month numbers to sheet indices (0-based index)
    def get_sheet_index_by_month(month):
        month_to_sheet = {
            1: ("January", 0),
            2: ("February", 1),
            3: ("March", 2),
            4: ("April", 3),
            5: ("May", 4),
            6: ("June", 5),
            7: ("July", 6),
            8: ("August", 7),
            9: ("September", 8),
        }
        return month_to_sheet.get(month, (None, None))

    file_path = '../datasources/finance/P&L Report - Details by Reporting Hierarchy.xlsx'  # File path

    # Helper function to process a single month
    def process_month(month_name, sheet_index):
        try:
            # Get all sheet names
            all_sheet_names = pd.ExcelFile(file_path).sheet_names

            # Check if the month corresponds to a valid sheet
            if sheet_index < len(all_sheet_names):
                # Load the specified sheet into a DataFrame
                csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

                print(f"\nProcessing sheet for {month_name}: {all_sheet_names[sheet_index]}")

                # Get the total number of rows for the current sheet
                total_rows = csv_data.shape[0]
                print(f'Total number of records in the sheet "{all_sheet_names[sheet_index]}": {total_rows}')

                # Print the column names
                print("Column names in the sheet:")
                print(csv_data.columns.tolist())

                # Ensure the target column "Account" exists
                target_column = "Account"
                if target_column in csv_data.columns:
                    # Locate the row with "EBIT Consolidated"
                    ebit_row = csv_data[csv_data.iloc[:, 0].str.contains('EBIT', case=False, na=False)]

                    if not ebit_row.empty:
                        # Extract the value from the target column
                        ebit_value = ebit_row[target_column].values[0]
                        print(f'Value against "EBIT" in "{target_column}": {ebit_value}')

                        # Print all values in the row
                        print("\nValues in the 'EBIT Consolidated' row:")
                        print(ebit_row.iloc[0].to_dict())

                        # Take budget and actual columns by index (1 = Budget, 2 = Actual)
                        budget_column = csv_data.columns[1]
                        actual_column = csv_data.columns[2]

                        # Ensure the Budget and Actual columns exist
                        if budget_column in csv_data.columns and actual_column in csv_data.columns:
                            # Extract the Budget and Actual values
                            budget_value = float(ebit_row[budget_column].values[0])
                            actual_value = float(ebit_row[actual_column].values[0])

                            print("Budget Value:", budget_value)
                            print("Actual Value:", actual_value)

                            # Convert to millions
                            budget_value_million = budget_value / 1_000_000
                            actual_value_million = actual_value / 1_000_000

                            total_value = budget_value + actual_value

                            # Calculate the percentage for each
                            if total_value != 0:
                                budget_percentage = (budget_value / total_value) * 100
                                actual_percentage = (actual_value / total_value) * 100
                            else:
                                budget_percentage = 0
                                actual_percentage = 0

                            # Print the results
                            print(f'Budget value in millions: {budget_value_million:.0f}M')
                            print(f'Actual value in millions: {actual_value_million:.0f}M')
                            print(f'Percentage of Budget: {budget_percentage:.2f}%')
                            print(f'Percentage of Actual: {actual_percentage:.2f}%')
                        else:
                            print('Budget and/or Actual columns not found in the dataset.')
                    else:
                        print(f'No row found with "EBIT Consolidated" in sheet "{all_sheet_names[sheet_index]}".')
                else:
                    print(f'Column "{target_column}" not found in the dataset for sheet "{all_sheet_names[sheet_index]}".')

            else:
                print(f"No sheet found for the month of {month_name}. Please check the available sheets.")

        except UnicodeDecodeError:
            print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')

    # Process all months if 'all' is passed
    if isinstance(month, str) and month.lower() == 'all':
        for month_num in range(1, 10):  # January (1) to September (9)
            month_name, sheet_index = get_sheet_index_by_month(month_num)
            if sheet_index is not None:
                process_month(month_name, sheet_index)
    else:
        # Process individual month based on integer input
        month_name, sheet_index = get_sheet_index_by_month(month)
        if sheet_index is not None:
            print(f"Using data for the month: {month_name}")
            process_month(month_name, sheet_index)
        else:
            # List all valid months if the input month is invalid
            valid_months = ", ".join(["1: January", "2: February", "3: March", "4: April", "5: May", "6: June",
                                      "7: July", "8: August", "9: September"])
            print(f"Invalid month entered.\nPlease enter a valid month number: {valid_months}")

# Examples:
ebit(9)
#ebit('all')  # Processes all months from January to September
