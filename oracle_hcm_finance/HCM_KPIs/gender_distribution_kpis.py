import pandas as pd
import os

def gender_distribution(month):
    """
    Calculates the count and percentage of male and female employees for a specified month or all months.

    Parameters:
    - month (int or str): The month (1 for January, 2 for February, etc.) or 'all' for all months.
    """
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'
    year = 2024

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    # List of month names for formatting the output
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Function to map individual grades
    def grade_mapper(grade):
        # (same grade mapping logic)
        ...

    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Ensure date columns are in datetime format
        data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')
        data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')

        # Define a function to calculate and print gender distribution for a specific month
        def calculate_gender_distribution(month):
            # Define start and end date for the given month
            start_date = pd.Timestamp(f'{year}-{month:02d}-01')
            end_date = start_date + pd.offsets.MonthEnd(1)

            # Filter data based on the specified conditions
            filtered_data = data[
                (data['Job title - English'] != 'Board Member') &
                (data['Actual Termination date'].isna() | (data['Actual Termination date'] > end_date)) &
                (data['Date of Joining'] <= end_date)
            ]

            if 'Gender' in filtered_data.columns:
                # Filter the data to include only Male and Female genders
                filtered_data = filtered_data[filtered_data['Gender'].isin(['Male', 'Female'])]

                # Group by Gender and count occurrences
                gender_counts = filtered_data['Gender'].value_counts()

                # Calculate total employees
                total_employees = gender_counts.sum()

                # Calculate percentage for each gender
                gender_percentages = (gender_counts / total_employees) * 100 if total_employees > 0 else {}

                # Get the month name for output formatting
                month_name = month_names[month - 1]

                # Print the gender distribution for the specified month and year
                print(f'Gender distribution for {month_name} {year}:')
                for gender, count in gender_counts.items():
                    percentage = gender_percentages[gender] if gender in gender_percentages else 0
                    print(f'{gender}: {count} ({percentage:.2f}%)')
            else:
                print('Missing column Gender in the dataset.')

        # If month is 'all', calculate for all months
        if month == 'all':
            for m in range(1, 13):
                calculate_gender_distribution(m)
        else:
            # Call the gender distribution calculation for the specified month
            calculate_gender_distribution(month)

    except Exception as e:
        print(f'Error: {str(e)}')

# Example usage
gender_distribution(2)  # For February
gender_distribution('all')  # For all months
