import pandas as pd

def filter_by_date(data, year=None, month=None, quarter=None):
    if 'Date of Joining' in data.columns:
        data = data.copy()  # Make a copy to avoid modifying the original DataFrame
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        data = data.dropna(subset=['Date of Joining'])

        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
            filtered_data = data[data['Actual Termination date'].isna()]
        else:
            print('Actual Termination Date column is not in the dataset.')
            filtered_data = data

        if year is not None:
            end_of_year = pd.Timestamp(year, 12, 31)
            filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_year]

            if month is not None:
                end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                filtered_data = filtered_data[filtered_data['Date of Joining'] <= end_of_month]

        elif month is not None:
            filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month == month]

        if quarter is not None:
            quarters = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in quarters:
                filtered_data = filtered_data[filtered_data['Date of Joining'].dt.month.isin(quarters[quarter])]

        if 'Assignment Category' in filtered_data.columns:
            excluded_categories = ['Touring 6:6', 'Touring 8:4']
            filtered_data = filtered_data[~filtered_data['Assignment Category'].isin(excluded_categories)]

        return filtered_data

    else:
        print('Joining Date column is not in the dataset.')
        return pd.DataFrame()

def count_employees_by_joining_date(file_path, year=2024, month=None):
    try:
        data = pd.read_excel(file_path)

        # Count total employees
        total_employees = data.shape[0]

        # Initialize a dictionary to store results for each month
        monthly_results = {}

        for month in range(1, 13):  # Loop through each month from 1 to 12
            # Filter data based on the criteria for the specific month
            filtered_data = filter_by_date(data, year=year, month=month)

            filtered_count = filtered_data.shape[0]

            if 'Actual Termination date' in data.columns:
                data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
                terminated_employees = data[(data['Actual Termination date'].notna()) & (data['Actual Termination date'].dt.year == year)].shape[0]
            else:
                terminated_employees = 0

            if 'Assignment Category' in data.columns:
                categories_of_interest = ['Touring 6:6', 'Touring 8:4']
                category_counts = data[data['Assignment Category'].isin(categories_of_interest)].shape[0]
            else:
                category_counts = 0

            # Store the results for the current month
            monthly_results[month] = {
                'Total Employees': total_employees,
                'Filtered Count': filtered_count,
                'Terminated Employees': terminated_employees,
                'Category Counts': category_counts,
            }

        return monthly_results

    except Exception as e:
        print(f'An error occurred: {e}')
        return {}

# Example usage
file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
monthly_results = count_employees_by_joining_date(file_path, year=2024)

# Print the results for each month
for month, results in monthly_results.items():
    print(f'Month: {month}')
    print(f"  Total Employees: {results['Total Employees']}")
    print(f"  Filtered Count: {results['Filtered Count']}")
    print(f"  Terminated Employees: {results['Terminated Employees']}")
    print(f"  Category Counts: {results['Category Counts']}")
