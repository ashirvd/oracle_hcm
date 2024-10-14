import pandas as pd
import os
def female_managers(month_number):
    # Define the file path directly in the function
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found
    year = 2024
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October'}

    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Ensure 'Date of Joining' exists and convert it to datetime
        if 'Date of Joining' in data.columns:
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')
            data = data.dropna(subset=['Date of Joining'])  # Remove rows where 'Date of Joining' is NaT
        else:
            print("Date of Joining column is not in the dataset.")
            return

        # Ensure 'Actual Termination date' exists and convert to datetime
        if 'Actual Termination date' in data.columns:
            data['Actual_Termination_date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')
        else:
            print("Actual Termination date column is not in the dataset.")
            return

        # Filter by valid grades
        valid_grades = ['C2', 'T5', '6', '7', '8', '9', '10', '11', '12', 'CEO']
        if 'Grade' in data.columns:
            data = data[data['Grade'].astype(str).isin(valid_grades)]
        else:
            print("Grade column is not in the dataset.")
            return

        # Filter by gender (female)
        if 'Gender' in data.columns:
            data = data[data['Gender'].str.lower() == 'female']
        else:
            print("Gender column is not in the dataset.")
            return

        if month_number == 'all':
            for month in range(1, 11):
                # Filter data by the current month
                filtered_data = data[(data['Date of Joining'].dt.year < year) |
                                     ((data['Date of Joining'].dt.year == year) & (data['Date of Joining'].dt.month <= month))]

                # Further filter by termination date
                filtered_data = filtered_data[
                    (filtered_data['Actual_Termination_date'].isna()) |  # Employees still active
                    ((filtered_data['Actual_Termination_date'].dt.year == year) & (filtered_data['Actual_Termination_date'].dt.month > month)) |  # Terminated after the current month
                    (filtered_data['Actual_Termination_date'].dt.year > year)  # Terminated after the current year
                ]

                # Print the count of female managers for each month
                print(f"Female managers in {month_names[month]}: {filtered_data.shape[0]}")
        else:
            # Process for a specific month
            filtered_data = data[(data['Date of Joining'].dt.year < year) |
                                 ((data['Date of Joining'].dt.year == year) & (data['Date of Joining'].dt.month <= month_number))]

            filtered_data = filtered_data[
                (filtered_data['Actual_Termination_date'].isna()) |
                ((filtered_data['Actual_Termination_date'].dt.year == year) & (filtered_data['Actual_Termination_date'].dt.month > month_number)) |
                (filtered_data['Actual_Termination_date'].dt.year > year)
            ]

            # Print the count for the specified month
            print(f"Female managers in {month_names[month_number]}: {filtered_data.shape[0]}")

    except Exception as e:
        print(f'An error occurred: {e}')


female_managers(1)  # For January
female_managers('all')  # For all months
