import pandas as pd


def cost_of_revenue(month):
    """Process cost of revenue metrics for a given month or all months."""

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
        return month_to_sheet.get(month.lower() if isinstance(month, str) else month)

    file_path = '../datasources/finance/P&L Report - Details by Reporting Hierarchy.xlsx'

    def process_month(month_num):
        """Process a single month's cost of revenue metrics."""
        sheet_index = get_sheet_index_by_month(month_num)
        if sheet_index is None:
            return

        try:
            all_sheet_names = pd.ExcelFile(file_path).sheet_names
            csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

            print(f'\nProcessing sheet: {all_sheet_names[sheet_index]}')
            month_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
                          6: "June", 7: "July", 8: "August", 9: "September"}
            print(f'Processing financial metrics for: {month_name.get(month_num)}')

            financial_terms = ['Revenue', 'Cost Revenue']
            financial_values = {}

            def clean_and_convert(value):
                """Clean and convert financial value to float."""
                if isinstance(value, (int, float)):
                    return float(value)
                value = value.replace(',', '')
                if value.strip() == '-' or value.strip() == '':
                    return 0.0
                if '(' in value and ')' in value:
                    value = '-' + value.replace('(', '').replace(')', '')
                return float(value)

            # Extract financial data
            for term in financial_terms:
                financial_row = csv_data[csv_data.iloc[:, 0].str.contains(term, case=False, na=False)]
                if not financial_row.empty:
                    actual_value = clean_and_convert(financial_row.iloc[0, 2])
                    financial_values[term] = {
                        'actual': actual_value / 1_000_000,
                    }
                else:
                    print(f'No row found with the term "{term}".')

            # Calculate Cost of Revenue %
            if 'Revenue' in financial_values and 'Cost Revenue' in financial_values:
                revenue_actual = financial_values['Revenue']['actual']
                cost_of_revenue_actual = financial_values['Cost Revenue']['actual']
                cost_of_revenue_percentage = (
                                                         cost_of_revenue_actual / revenue_actual) * 100 if revenue_actual != 0 else 0.0

                print(f'Cost of Revenue % for {month_name.get(month_num)}: Actual = {cost_of_revenue_percentage:.2f}%')
            else:
                print('Required financial data not found.')

        except Exception as e:
            print(f'Error processing month: {month_num}. Reason: {str(e)}')

    # Handle month input
    if isinstance(month, str) and month.lower() == 'all':
        for month_num in range(1, 10):
            process_month(month_num)  # Process each month
    elif isinstance(month, (int, str)) and get_sheet_index_by_month(month) is not None:
        process_month(month)  # Process for a specific month
    else:
        print(f'Invalid month input: {month}. Please enter a valid month (1-9) or "all".')


# Usage to print Cost of Revenue % for January

cost_of_revenue('all')  # For all months
