import pandas as pd
import os

def financial_metrics(month):
    """Process financial metrics for a given month and return EBIT Actual and Budget."""

    def get_sheet_index_by_month(month):
        month_to_sheet = {
            1: 0, "january": 0,
            2: 1, "february": 1,
            3: 2, "march": 2,
            4: 3, "april": 3,
            5: 4, "may": 4,
            6: 5, "june": 5,
            7: 6, "july": 6,
            8: 7, "august": 7,
            9: 8, "september": 8
        }
        return month_to_sheet.get(month) if isinstance(month, (int, str)) else None

    file_path = '../data_finance/finance/P&L Report - Details by Reporting Hierarchy.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    def process_month(month_num):
        """Process a single month's financial metrics."""
        sheet_index = get_sheet_index_by_month(month_num)
        if sheet_index is None:
            return

        try:
            all_sheet_names = pd.ExcelFile(file_path).sheet_names
            csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

            print(f'\nProcessing sheet: {all_sheet_names[sheet_index]}')
            month_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                          7: "July", 8: "August", 9: "September"}
            print(f'Processing financial metrics for: {month_name.get(month_num)}')

            # Initialize variables for EBIT Actual and Budget
            ebit_actual = None
            ebit_budget = None

            # Locate EBIT Actual and Budget
            for term in ['EBIT', 'Budget EBIT']:
                financial_row = csv_data[csv_data.iloc[:, 0].str.contains(term, case=False, na=False)]
                if not financial_row.empty:
                    if term == 'EBIT':
                        ebit_actual = float(
                            financial_row.iloc[0, 2].replace(',', '').replace('(', '-').replace(')', ''))
                    elif term == 'Budget EBIT':
                        ebit_budget = float(
                            financial_row.iloc[0, 3].replace(',', '').replace('(', '-').replace(')', ''))

            # Print EBIT Actual and Budget
            if ebit_actual is not None:
                print(f'EBIT Actual: {ebit_actual / 1_000_000:.2f}M')  # Convert to millions
            if ebit_budget is not None:
                print(f'EBIT Budget: {ebit_budget / 1_000_000:.2f}M')  # Convert to millions

        except Exception as e:
            print(f'Error processing month: {month_num}. Please check the data. Error: {str(e)}')
            pass

    if isinstance(month, (int, str)) and get_sheet_index_by_month(month) is not None:
        process_month(month)
    else:
        print(f'Invalid month input: {month}. Please enter a valid month (1-9).')


# Example call to the function
financial_metrics(7)
