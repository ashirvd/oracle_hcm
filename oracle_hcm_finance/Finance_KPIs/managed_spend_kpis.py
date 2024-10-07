import pandas as pd

file_path = '../datasources/finance/Procurement Monthly Report_latest.xlsx'

try:
    # Load the Excel file
    excel_data = pd.read_excel(file_path, header=19)  # Adjust header row if necessary

    # Get the total number of rows
    total_rows = excel_data.shape[0]
    print(f'Total number of records in the Excel file: {total_rows}')

    # Ensure the necessary columns exist
    po_amount_column = "PO Amount (SAR)"
    po_types_column = "PO Types"

    if po_amount_column in excel_data.columns and po_types_column in excel_data.columns:
        # Strip any leading/trailing whitespace and standardize case for comparison
        excel_data[po_types_column] = excel_data[po_types_column].str.strip().str.lower()

        # Clean and convert "PO Amount (SAR)" values to numeric
        excel_data[po_amount_column] = pd.to_numeric(excel_data[po_amount_column], errors='coerce')

        # Calculate the total sum of all PO amounts
        total_sum = excel_data[po_amount_column].sum()
        print(f'\nTotal sum of all "PO Amount (SAR)": {total_sum:.2f}')

        # Define the PO types to process
        po_types = ["direct purchase", "sole source", "single source", "competitive"]

        for po_type in po_types:
            # Filter rows based on the PO type
            filtered_data = excel_data.loc[excel_data[po_types_column] == po_type]

            # Calculate the sum of the "PO Amount (SAR)" column for this PO type
            total_po_amount = filtered_data[po_amount_column].sum()

            # Calculate the percentage
            percentage = (total_po_amount / total_sum * 100) if total_sum > 0 else 0

            # # Print the values in the "PO Amount (SAR)" column
            # print(f'\nValues in the "{po_amount_column}" column for "{po_type.title()}":')
            # print(filtered_data[po_amount_column].dropna().to_list())

            # Print the sum and percentage of the "PO Amount (SAR)" column
            print(f'\nSum of "PO Amount (SAR)" for "{po_type.title()}": {total_po_amount:.2f}')
            print(f'Percentage of total for "{po_type.title()}": {percentage:.2f}%')
    else:
        print(f'Columns "{po_amount_column}" or "{po_types_column}" not found in the dataset.')

except FileNotFoundError:
    print('The specified file was not found.')
except Exception as e:
    print(f'An error occurred: {e}')

import pandas as pd

def spend_percentage_by_source_type(df, po_amount_column, po_types_column, source_types, total_sum):
    """
    Calculates the sum of "PO Amount (SAR)" and percentage of total for specified PO types.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the procurement data.
    - po_amount_column (str): The column name for PO amounts.
    - po_types_column (str): The column name for PO types.
    - source_types (list): List of PO types to include in the sum.
    - total_sum (float): The total sum of "PO Amount (SAR)" for all records.

    Returns:
    - float: The combined sum of "PO Amount (SAR)" for the specified PO types.
    - float: The combined percentage of total for the specified PO types.
    """
    # Filter rows where PO types are in the specified source types
    filtered_data = df[df[po_types_column].isin(source_types)]

    # Calculate the sum of the "PO Amount (SAR)" column for the filtered data
    total_spend = filtered_data[po_amount_column].sum()

    # Calculate the percentage of the total sum
    percentage = (total_spend / total_sum * 100) if total_sum > 0 else 0

    return total_spend, percentage

# File path and data loading
file_path = '../datasources/finance/Procurement Monthly Report_latest.xlsx'

try:
    # Load the Excel file
    excel_data = pd.read_excel(file_path, header=19)  # Adjust header row if necessary

    # Get the total number of rows
    total_rows = excel_data.shape[0]
    print(f'Total number of records in the Excel file: {total_rows}')

    # Ensure the necessary columns exist
    po_amount_column = "PO Amount (SAR)"
    po_types_column = "PO Types"

    if po_amount_column in excel_data.columns and po_types_column in excel_data.columns:
        # Clean and standardize data
        excel_data[po_types_column] = excel_data[po_types_column].str.strip().str.lower()
        excel_data[po_amount_column] = pd.to_numeric(excel_data[po_amount_column], errors='coerce')

        # Calculate the total sum of all PO amounts
        total_sum = excel_data[po_amount_column].sum()
        print(f'\nTotal sum of all "PO Amount (SAR)": {total_sum:.2f}')

        # Define the PO types to process
        po_types = ["direct purchase", "sole source", "single source", "competitive"]

        for po_type in po_types:
            # Filter rows based on the PO type
            filtered_data = excel_data.loc[excel_data[po_types_column] == po_type]

            # Calculate the sum of the "PO Amount (SAR)" column for this PO type
            total_po_amount = filtered_data[po_amount_column].sum()

            # Calculate the percentage
            percentage = (total_po_amount / total_sum * 100) if total_sum > 0 else 0

            # Print the sum and percentage of the "PO Amount (SAR)" column
            print(f'\nSum of "PO Amount (SAR)" for "{po_type.title()}": {total_po_amount:.2f}')
            print(f'Percentage of total for "{po_type.title()}": {percentage:.2f}%')

        # Use the new function to get the sum and percentage for 'sole source' and 'single source' only
        source_types = ["sole source", "single source"]
        combined_spend, combined_percentage = spend_percentage_by_source_type(
            excel_data, po_amount_column, po_types_column, source_types, total_sum
        )

        print(f'\nCombined sum of "PO Amount (SAR)" for "Sole Source" and "Single Source": {combined_spend:.2f}')
        print(f'Combined percentage of total for "Sole Source" and "Single Source": {combined_percentage:.2f}%')

    else:
        print(f'Columns "{po_amount_column}" or "{po_types_column}" not found in the dataset.')

except FileNotFoundError:
    print('The specified file was not found.')
except Exception as e:
    print(f'An error occurred: {e}')
