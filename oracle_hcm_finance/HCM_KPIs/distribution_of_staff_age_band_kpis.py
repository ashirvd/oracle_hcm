from datetime import datetime
import pandas as pd
import os

def distribution_staff_age_band(month):
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output-Updated (1).xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    year = 2024
    today = pd.Timestamp(datetime.now().date())

    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Ensure 'Date of Joining' exists and convert it to datetime
        if 'Date of Joining' in data.columns:
            data = data.copy()
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')
            data = data.dropna(subset=['Date of Joining'])  # Drop rows where 'Date of Joining' couldn't be parsed

            # Ensure 'Date of Birth' exists and calculate Age from DOB
            if 'Date of Birth' in data.columns:
                data['Date of Birth'] = pd.to_datetime(data['Date of Birth'], format='%d-%b-%Y', errors='coerce')
                # Calculate Age based on DOB and today's date
                data['Age'] = today.year - data['Date of Birth'].dt.year
                # Subtract 1 from age where the birthday has not occurred this year
                data['Age'] -= (today.month < data['Date of Birth'].dt.month) | \
                               ((today.month == data['Date of Birth'].dt.month) & (today.day < data['Date of Birth'].dt.day))
                data['Age'] = data['Age'].where(data['Age'] >= 0, 0)  # Ensure age is not negative

            else:
                print('Date of Birth column is not in the dataset. Age will not be calculated from DOB.')

            # Exclude 'Board Members' if necessary
            if 'Job title - English' in data.columns:
                data = data[data['Job title - English'] != 'Board Member']

            # If 'Actual Termination date' exists, filter based on that
            if 'Actual Termination date' in data.columns:
                data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y',
                                                                 errors='coerce')

                def calculate_headcount_for_month(month):
                    # Get the month name
                    month_name = pd.Timestamp(year=year, month=month, day=1).strftime('%B')
                    # Filter for employees who joined on or before the end of the month and are still active
                    end_of_month = pd.Timestamp(year, month, pd.Timestamp(year, month, 1).days_in_month)
                    if today < end_of_month:
                        print(f"Month {month_name} is not complete. Headcount cannot be calculated.")
                        return 0  # Exit if the month is not complete

                    filtered_data = data[(
                        data['Date of Joining'] <= end_of_month) &  # Employees joined on or before the month end
                        ((data['Actual Termination date'].isna()) | (data['Actual Termination date'] > end_of_month))
                        # Employees not terminated or terminated after the month
                    ].copy()  # Explicitly create a copy to avoid SettingWithCopyWarning

                    # Count the total active employees
                    headcount = filtered_data.shape[0]

                    # Define age categories
                    age_bins = [float('-inf'), 25, 35, 45, 60, float('inf')]
                    age_labels = ['<25', '25-34', '35-44', '45-59', '60 and above']

                    # Bin the ages and assign to a new column using .loc
                    filtered_data.loc[:, 'Age Group'] = pd.cut(filtered_data['Age'], bins=age_bins, labels=age_labels,
                                                               right=False)

                    # Count the number of employees in each age group
                    age_counts = filtered_data['Age Group'].value_counts().sort_index()

                    # Calculate percentages
                    age_percentages = (age_counts / headcount) * 100 if headcount > 0 else age_counts

                    # Display results
                    print(f"Headcount for {month_name}: {headcount}")
                    print("Age Distribution:")
                    for age_group, count in age_counts.items():
                        percentage = age_percentages[age_group]
                        print(f"{age_group}: Count = {count}, Percentage = {percentage:.2f}%")

                    return headcount

                # If 'all' is passed, calculate for every month
                if month == 'all':
                    results = {}
                    for month_number in range(1, 11):
                        month_name = pd.Timestamp(year=year, month=month_number, day=1).strftime('%B')
                        headcount = calculate_headcount_for_month(month_number)
                        results[month_name] = headcount
                    return results

                # Otherwise, calculate for a specific month
                else:
                    month_name = pd.Timestamp(year=year, month=month, day=1).strftime('%B')
                    headcount = calculate_headcount_for_month(month)
                    return headcount

            else:
                print('Actual Termination Date column is not in the dataset.')
                return 0

        else:
            print('Date of Joining column is not in the dataset.')
            return 0

    except Exception as e:
        print(f'An error occurred: {e}')
        return 0


distribution_staff_age_band(1)  # January
distribution_staff_age_band('all')  # All months
