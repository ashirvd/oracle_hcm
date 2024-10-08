import pandas as pd
import os

def variance_to_budget(month):
    """Extract and display variance to budget for financial terms, optionally for all months."""

    def get_sheet_index_by_month(month):
        """Map month number or name to sheet index."""
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

    def clean_and_convert(value):
        """Clean and convert financial value."""
        if isinstance(value, (int, float)):
            return float(value)
        value = value.replace(',', '')
        if value.strip() == '-' or value.strip() == '':
            return 0.0
        if '(' in value and ')' in value:
            value = '-' + value.replace('(', '').replace(')', '')
        return float(value)

    file_path = '../datasources/finance/P&L Report - Details by Reporting Hierarchy.xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    def process_single_month(month_num):
        """Process and display variance for a single month."""
        sheet_index = get_sheet_index_by_month(month_num)
        if sheet_index is None:
            print(f"Invalid month input: {month_num}.")
            return

        try:
            all_sheet_names = pd.ExcelFile(file_path).sheet_names
            csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

            print(f'\nProcessing sheet: {all_sheet_names[sheet_index]} for month {month_num}')

            # Financial terms to extract variance for, excluding 'Cost Revenue' and 'SG&A'
            financial_terms = ['Revenue', 'Gross Profit', 'EBIT', 'Net Income']

            financial_variances = {}

            for term in financial_terms:
                financial_row = csv_data[csv_data.iloc[:, 0].str.contains(term, case=False, na=False)]
                if not financial_row.empty:
                    variance_value = -clean_and_convert(financial_row.iloc[0, 3])  # Assuming variance is in column 3
                    financial_variances[term] = variance_value / 1_000_000  # Convert to millions
                else:
                    print(f'No row found with the term "{term}".')

            # Print Variance for each financial term (excluding 'Cost Revenue' and 'SG&A')
            print("\nFinancial variances (in millions):")
            for term, variance in financial_variances.items():
                print(f'{term}: Variance = {variance:.2f}M')

        except Exception as e:
            print(f"Error processing month {month_num}: {str(e)}")

    if isinstance(month, str) and month.lower() == 'all':
        # Process all months (from January to September)
        for month_num in range(1, 10):
            process_single_month(month_num)
    else:
        # Process a single month
        process_single_month(month)


# Example usage
variance_to_budget('all')  # Process all months
