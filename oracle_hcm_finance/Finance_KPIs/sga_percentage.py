import pandas as pd
import os
def sga_percentage(month):
    """Calculate SG&A % (SG&A Actual / Revenue Actual * 100) for a given month or all months."""

    # Month to sheet mapping
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

    # Month names for output
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September"
    }

    # Validate and handle 'all'
    if month == 'all':
        for month_num in range(1, 10):
            sga_percentage(month_num)  # Call the function recursively for each month
        return

    # Validate and get the sheet index for a specific month
    sheet_index = month_to_sheet.get(month.lower() if isinstance(month, str) else month)
    if sheet_index is None:
        print(f'Invalid month input: {month}. Please enter a valid month (1-9 or "january"-"september").')
        return

    # Path to the Excel file
    file_path = '../datasources/finance/P&L Report - Details by Reporting Hierarchy.xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    try:
        all_sheet_names = pd.ExcelFile(file_path).sheet_names
        csv_data = pd.read_excel(file_path, sheet_name=all_sheet_names[sheet_index], header=8)

        financial_terms = ['Revenue', 'SG&A']
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

        # Extract financial data
        for term in financial_terms:
            financial_row = csv_data[csv_data.iloc[:, 0].str.contains(term, case=False, na=False)]
            if not financial_row.empty:
                actual_value = clean_and_convert(financial_row.iloc[0, 2])
                financial_values[term] = {
                    'actual': actual_value / 1_000_000,  # Convert to millions
                }
            else:
                print(f'No row found with the term "{term}".')

        # Calculate SG&A %
        if 'Revenue' in financial_values and 'SG&A' in financial_values:
            revenue_actual = financial_values['Revenue']['actual']
            sga_actual = financial_values['SG&A']['actual']
            sga_percentage_value = (sga_actual / revenue_actual) * 100 if revenue_actual != 0 else 0.0
            month_name = month_names.get(month, str(month))  # Get the month name
            print(f'SG&A % for {month_name}: {sga_percentage_value:.2f}%')
        else:
            print('Required financial data not found.')

    except Exception as e:
        print(f'Error processing month: {month}. Reason: {str(e)}')


sga_percentage(2)
