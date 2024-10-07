import pandas as pd

def managed_spend(file_index):
    # Define file paths inside the function
    file_paths = [
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_1 (1).xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_2.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_3.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_4.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_5.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_6.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_7.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_8.xlsx',
        r'..\datasources\OneDrive_1_06-10-2024\Procurement Monthly Report_9.xlsx'
    ]

    # Month mapping for the output
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September"]

    if file_index == 'all':
        # Process all files
        for i in range(len(file_paths)):
            managed_spend(i + 1)  # Call itself for each file index
        return

    # Check if the index is valid
    if 1 <= file_index <= len(file_paths):
        file_path = file_paths[file_index - 1]  # Adjust index to be zero-based
        month = months[file_index - 1]  # Get the month corresponding to the index

        try:
            # Load the Excel file
            excel_data = pd.read_excel(file_path, header=19)  # Adjust header row if necessary

            # Ensure the necessary columns exist
            po_amount_column = "PO Amount (SAR)"
            po_types_column = "PO Types"

            if po_amount_column in excel_data.columns and po_types_column in excel_data.columns:
                # Clean and standardize data
                excel_data[po_types_column] = excel_data[po_types_column].str.strip().str.lower()
                excel_data[po_amount_column] = pd.to_numeric(excel_data[po_amount_column], errors='coerce')

                # Calculate the total sum of all PO amounts
                total_sum = excel_data[po_amount_column].sum()

                # Define the PO types to process
                po_types = ["direct purchase", "sole source", "single source", "competitive"]
                results = {}

                for po_type in po_types:
                    # Filter rows based on the PO type
                    filtered_data = excel_data.loc[excel_data[po_types_column] == po_type]

                    # Calculate the sum of the "PO Amount (SAR)" column for this PO type
                    total_po_amount = filtered_data[po_amount_column].sum()

                    # Calculate the percentage
                    percentage = (total_po_amount / total_sum * 100) if total_sum > 0 else 0

                    # Store the results formatted in millions
                    results[po_type] = (total_po_amount / 1_000_000, percentage)

                # Print results in desired format
                print(f'Month: {month}')
                for po_type, (amount_million, percentage) in results.items():
                    print(f'{po_type.title()} {amount_million:.2f}M ({percentage:.2f}%)')

            else:
                print(f'Columns "{po_amount_column}" or "{po_types_column}" not found in the dataset.')

        except FileNotFoundError:
            print('The specified file was not found.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print(f'Invalid file index. Please provide a number between 1 and {len(file_paths)}.')


managed_spend(1)
#managed_spend('all')  # For all files
