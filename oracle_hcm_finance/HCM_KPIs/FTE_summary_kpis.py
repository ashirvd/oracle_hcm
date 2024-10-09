import pandas as pd

def filter_by_date(data, year=None, month=None, quarter=None):
    # Check if 'Date of Joining' column exists in the data
    if 'Date of Joining' in data.columns:
        # Convert 'Date of Joining' to datetime format
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        # Remove rows where 'Date of Joining' couldn't be parsed
        data = data.dropna(subset=['Date of Joining'])

        # Check for 'Actual Termination date' column and filter rows without termination dates
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            # Filter employees without a termination date
            filtered_data = data[data['Actual Termination date'].isna()]
        else:
            print('Actual Termination Date column is not in the dataset.')
            filtered_data = data

        # Apply year filter if specified
        if year is not None:
            # Ensure all employees who joined on or before the end of the specified year
            end_of_year = pd.Timestamp(year, 12, 31)
            filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_year]

            # If a month is specified, ensure employees joined on or before the end of that month
            if month is not None:
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_month]

        # Apply month filter if specified and no year is provided
        elif month is not None:
            filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month == month]

        # Apply quarter filter if specified
        if quarter is not None:
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            # Ensure the quarter is valid
            if quarter in quarters:
                filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month.isin(quarters[quarter])]

        # Filter out employees with specific Assignment Categories
        if 'Assignment Category' in filtered_data.columns:
            excluded_categories = ['Touring 6:6', 'Touring 8:4']
            filtered_data = filtered_data[~filtered_data['Assignment Category'].isin(excluded_categories)]

        # Return the filtered data
        return filtered_data

    else:
        print('Joining Date column is not in the dataset.')
        return pd.DataFrame()  # Return an empty DataFrame

def count_employees_by_joining_date(file_path, year=2024, month=None, quarter=None):
    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Count total employees
        total_employees = data.shape[0]

        # Filter data based on the criteria
        filtered_data = filter_by_date(data, year=year, month=month, quarter=quarter)

        # Count employees who meet the filter criteria
        filtered_count = filtered_data.shape[0]

        # Count terminated employees and check if they fall within the specified year
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            # Filter terminated employees within the specified year
            terminated_employees = data[(data['Actual Termination date'].notna()) & (data['Actual Termination date'].dt.year == year)].shape[0]
        else:
            terminated_employees = 0

        # Count employees with specific Assignment Categories
        if 'Assignment Category' in data.columns:
            categories_of_interest = ['Touring 6:6', 'Touring 8:4']
            category_counts = data[data['Assignment Category'].isin(categories_of_interest)].shape[0]

            # Count employees with specific Assignment Categories and a termination date
            category_and_termination_counts = data[(data['Assignment Category'].isin(categories_of_interest)) & (data['Actual Termination date'].notna())].shape[0]

            # Count employees with assignment categories other than "Touring 6:6" or "Touring 8:4"
            other_category_data = data[~data['Assignment Category'].isin(categories_of_interest)]
            other_category_count = other_category_data.shape[0]

            # Count employees with assignment categories other than "Touring 6:6" or "Touring 8:4" who have a blank termination date
            other_category_blank_termination_count = other_category_data[other_category_data['Actual Termination date'].isna()].shape[0]

        else:
            category_counts = 0
            category_and_termination_counts = 0
            other_category_count = 0
            other_category_blank_termination_count = 0

        print(f'Total number of employees in the sheet: {total_employees}')
        print(f'Total number of employees matching the filter criteria: {filtered_count}')
        print(f'Total number of terminated employees in {year}: {terminated_employees}')
        print(f'Total number of employees with Assignment Category "Touring 6:6" or "Touring 8:4": {category_counts}')
        print(f'Total number of employees with Assignment Categories other than "Touring 6:6" or "Touring 8:4": {other_category_count}')
        print(f'Total number of employees with Assignment Categories other than "Touring 6:6" or "Touring 8:4" who have a blank Actual Termination Date: {other_category_blank_termination_count}')

        return total_employees, filtered_count, terminated_employees, category_counts, category_and_termination_counts, other_category_count, other_category_blank_termination_count

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0, 0, 0, 0, 0, 0, 0

# Example usage
file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
total_employees, filtered_data_count, terminated_employees, category_counts, category_and_termination_counts, other_category_count, other_category_blank_termination_count = count_employees_by_joining_date(file_path, year=2024, month=9, quarter=None)
