import pandas as pd


def financial_metrics(month):
    """Process financial metrics for a given month."""

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

    file_path = '../datasources/finance/P&L Report - Details by Reporting Hierarchy.xlsx'

    def process_month(month_num):
        """Process a single month's financial metrics."""
        sheet_index = get_sheet_index_by_month(month_num)
        if sheet_index is None:
            return

        try:
            all_sheet_names = pd.ExcelFile(file_path).sheet_names
            csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

            print(f'\nProcessing sheet: {all_sheet_names[sheet_index]}')
            month_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                          8: "August", 9: "September"}
            print(f'Processing financial metrics for: {month_name.get(month_num)}')

            total_rows = csv_data.shape[0]
            print(f'Total number of records in the sheet "{all_sheet_names[sheet_index]}": {total_rows}')

            financial_terms = ['Revenue', 'Cost Revenue', 'SG&A', 'Gross Profit', 'EBIT', 'Net Income']
            financial_values = {}

            def clean_and_convert(value):
                if isinstance(value, (int, float)):
                    return float(value)
                value = value.replace(',', '')
                if value.strip() == '-' or value.strip() == '':
                    return 0.0
                if '(' in value and ')' in value:
                    value = '-' + value.replace('(', '').replace(')', '')
                return float(value)

            for term in financial_terms:
                financial_row = csv_data[csv_data.iloc[:, 0].str.contains(term, case=False, na=False)]
                if not financial_row.empty:
                    actual_value = clean_and_convert(financial_row.iloc[0, 2])
                    variance_value = -clean_and_convert(financial_row.iloc[0, 3])  # Assuming this is the variance value
                    financial_values[term] = {
                        'actual': actual_value / 1_000_000,
                        'variance': variance_value / 1_000_000
                    }
                else:
                    print(f'No row found with the term "{term}".')

            # Calculate Revenue percentages
            if 'Revenue' in financial_values:
                revenue_actual = financial_values['Revenue']['actual']
                if revenue_actual != 0:  # Prevent division by zero
                    # Cost of Revenue to Revenue % Calculation
                    if 'Cost Revenue' in financial_values:
                        cost_of_revenue_actual = financial_values['Cost Revenue']['actual']
                        financial_values['Cost of Revenue %'] = {
                            'actual': (cost_of_revenue_actual / revenue_actual) * 100
                        }

                    # **Insert SG&A to Revenue % Calculation Here**
                    if 'SG&A' in financial_values:
                        sga_actual = financial_values['SG&A']['actual']
                        sga_percentage = (sga_actual / revenue_actual) * 100
                        financial_values['SG&A to Revenue %'] = {
                            'actual': sga_percentage
                        }

            # Print Financial Metrics
            print("\nFinancial metrics (in millions):")
            for term, values in financial_values.items():
                if term == 'Cost Revenue':  # Skip printing Cost Revenue
                    continue
                if term == 'SG&A':
                    continue  # Skip printing the actual SG&A values
                if term == 'Cost of Revenue %':
                    print(f'{term}: Actual = {values["actual"]:.2f}%')  # Format as percentage
                elif term == 'SG&A to Revenue %':
                    print(f'{term}: Actual = {values["actual"]:.2f}%')  # Format as percentage
                else:
                    print(f'{term}: Actual = {values["actual"]:.2f}M, Variance = {values["variance"]:.2f}M')

            return financial_values

        except Exception as e:
            # Show error message only for actual exceptions
            # print(f'Error processing month: {month_num}. Please check the data. Error: {str(e)}')
            pass

    if isinstance(month, str) and month.lower() == 'all':
        for month_num in range(1, 10):
            process_month(month_num)
    elif isinstance(month, (int, str)) and get_sheet_index_by_month(month) is not None:
        process_month(month)
    else:
        print(f'Invalid month input: {month}. Please enter a valid month (1-9) or "all".')


financial_metrics(1)
