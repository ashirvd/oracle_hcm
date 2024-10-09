import pandas as pd
import os

def new_joiners(month, year=2024):
    """
    Count the number of new joiners for a specified month or for all months in a specified year from the employee data.

    Parameters:
    - month (int or str): The month to filter by (1 for January, 2 for February, etc.) or 'all' for all months.
    - year (int, optional): The year to filter by. Default is 2024.

    Returns:
    - dict or int: A dictionary with months as keys and counts as values if 'all' is specified, otherwise an int.
    """
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    try:
        # Load the Excel file
        csv_data = pd.read_excel(file_path)

        # Check if the 'Date of Joining' column exists
        if 'Date of Joining' in csv_data.columns:
            # Convert 'Date of Joining' to datetime format for filtering purposes
            csv_data['Date of Joining'] = pd.to_datetime(csv_data['Date of Joining'], format='%d-%b-%Y',
                                                         errors='coerce')

            # Remove rows where 'Date of Joining' couldn't be parsed
            csv_data = csv_data.dropna(subset=['Date of Joining'])

            if month == 'all':
                # Initialize a dictionary to hold counts for each month
                monthly_counts = {}

                for m in range(1, 13):  # Iterate over months 1 to 12
                    month_data = csv_data[
                        (csv_data['Date of Joining'].dt.year == year) & (csv_data['Date of Joining'].dt.month == m)]
                    monthly_counts[m] = month_data.shape[0]  # Count new joiners for each month

                # Print the results for each month without returning the dictionary
                for m, count in monthly_counts.items():
                    month_name = pd.Timestamp(year=year, month=m, day=1).strftime("%B")
                    print(f'Total number of new joiners for {month_name} {year}: {count}')

                return  # Return nothing

            else:
                # Filter data for the specified month and year
                month_data = csv_data[
                    (csv_data['Date of Joining'].dt.year == year) & (csv_data['Date of Joining'].dt.month == month)]

                # Get the count of new joiners for the specified month
                new_joiners_count = month_data.shape[0]
                print(
                    f'Total number of new joiners for {pd.Timestamp(year=year, month=month, day=1).strftime("%B %Y")}: {new_joiners_count}')
                return new_joiners_count  # Return the count for the specific month

        else:
            print('The "Date of Joining" column is not found in the Excel file.')
            return 0

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0

# Example usage
new_joiners(1)  # Count of new joiners for January 2024
new_joiners('all')  # Count of new joiners for all months in 2024
#jan 40, Feb 46 , mar 24, apr 22, may 44, june 36