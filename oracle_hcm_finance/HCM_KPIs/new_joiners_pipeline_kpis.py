import pandas as pd

file_path = '../datasources/finance/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1.xlsx'

def record_without_filter():
    try:
        # Load the CSV file
        csv_data = pd.read_excel(file_path)  # Try different encodings if necessary

        # Get the total number of rows
        total_rows = csv_data.shape[0]
        print(f'Total number of employee records in the CSV file: {total_rows}')

        # Check if the 'Joining Date' column exists
        if 'Date of Joining' in csv_data.columns:
            # Count the number of employees with a non-null and non-empty Joining Date
            joining_date_count = csv_data['Date of Joining'].notna().sum()
            print(f'Total number of employees with a joining date: {joining_date_count}')
        else:
            print('The "Joining Date" column is not found in the CSV file.')

    except Exception as e:
        print(f'An error occurred: {e}')

def filter_by_date(df, year=None, month=None, quarter=None):
    """
    Filter the DataFrame based on year, month, and quarter.
    Only records with valid 'Date of Joining' will be considered.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing employee data.
    - year (int, optional): The year to filter by.
    - month (int, optional): The month to filter by (1 to 12).
    - quarter (int, optional): The quarter to filter by (1 to 4).

    Returns:
    - pd.DataFrame: The filtered DataFrame based on the specified criteria.
    """
    if 'Date of Joining' in df.columns:
        # Convert 'Date of Joining' to datetime format for filtering purposes
        df = df.copy()  # Make a copy to avoid modifying the original DataFrame
        df['Date of Joining'] = pd.to_datetime(df['Date of Joining'], format='%d-%b-%Y', errors='coerce')  # Use 'coerce' to handle errors

        # Remove rows where 'Date of Joining' couldn't be parsed
        df = df.dropna(subset=['Date of Joining'])

        if year is not None:
            # Filter by year
            df = df[df['Date of Joining'].dt.year == year]

        if month is not None:
            # Filter by month
            df = df[df['Date of Joining'].dt.month == month]

        if quarter is not None:
            # Filter by quarter
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            # Ensure the quarter is valid
            if quarter in quarters:
                df = df[df['Date of Joining'].dt.month.isin(quarters[quarter])]

    else:
        print('Joining Date column is not in dataset')

    return df

try:
    csv_data = pd.read_excel(file_path)  # Adjust encoding as necessary

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    # Filter data by date
    filtered_data = filter_by_date(csv_data, year=2024, month=None, quarter=None)

    # Print filtered results
    print(f'Total number of records after filtering: {filtered_data.shape[0]}')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')

