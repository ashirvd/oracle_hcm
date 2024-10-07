import pandas as pd

file_path = '../datasources/finance/AR Aging Summary Report_Customer Level Detail.csv'

# Attempt to load the CSV file with the header on the specified row
try:
    # Load the CSV file with the correct header row (assuming the 15th row, index 14, contains headers)
    csv_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1', header=14)

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    # Print the column names
    print("Column names in the CSV file:")
    print(csv_data.columns.tolist())

    # Ensure the "Not Due", "Outstanding", and "Customer Name" columns exist
    not_due_column = "Not Due"  # Update with the correct column name if necessary
    outstanding_column = "Outstanding"  # Update with the correct column name if necessary
    customer_name_column = "Customer Name"  # Update with the correct column name if necessary

    if not_due_column in csv_data.columns and outstanding_column in csv_data.columns and customer_name_column in csv_data.columns:
        # Function to clean and convert values to float
        def clean_and_convert(value):
            # Remove commas and handle parentheses for negative values
            value = str(value).replace(',', '')
            if '(' in value and ')' in value:
                value = '-' + value.replace('(', '').replace(')', '')
            try:
                return float(value)
            except ValueError:
                return 0.0  # Return 0.0 for any non-numeric entries

        # Clean and convert the "Not Due" and "Outstanding" values to numeric
        csv_data[not_due_column] = csv_data[not_due_column].apply(clean_and_convert)
        csv_data[outstanding_column] = csv_data[outstanding_column].apply(clean_and_convert)

        # Initialize the sum variables
        running_total_not_due = 0.0
        running_total_outstanding = 0.0

        # Print each value and the running total for "Not Due" and "Outstanding"
        print("\nValues in the 'Not Due' column and running sum:")
        for index, row in csv_data.iterrows():
            if pd.notna(row[customer_name_column]) and row[customer_name_column].strip():  # Check if Customer Name is valid
                not_due_value = row[not_due_column]
                outstanding_value = row[outstanding_column]

                running_total_not_due += not_due_value
                running_total_outstanding += outstanding_value

                print(f'Row {index + 1} | Not Due: {not_due_value:.2f} | Outstanding: {outstanding_value:.2f} | Running Total Not Due: {running_total_not_due:.2f} | Running Total Outstanding: {running_total_outstanding:.2f}')
            else:
                break  # Stop summing if an invalid customer name is encountered

        running_total_not_due_millions= running_total_not_due/ 1_000_000
        running_total_outstanding_millions= running_total_outstanding/ 1_000_000
        overdue_final_amount= running_total_outstanding_millions - running_total_not_due_millions

        # Final sums
        print(f'\nNot Due Amount: {running_total_not_due:.2f}')
        print(f'Outstanding Amount: {running_total_outstanding:.2f}')
        print(f'\nCurrent Amount: {running_total_not_due_millions:.2f}M')
        print(f'\nOverDue Amount: {overdue_final_amount:.2f}M')

    else:
        print(f'Columns "{not_due_column}", "{outstanding_column}", or "{customer_name_column}" not found in the dataset.')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
