import pandas as pd
import os


# Function to map grades and filter data for a specific month or all months
def map_grade(month):
    """
    Maps employee grades and counts occurrences by grade and gender for a specified month or all months.

    Parameters:
    - month (int or str): The month (1 for January, 2 for February, etc.) or 'all' for all months.
    """
    file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return  # Exit the function if the file is not found

    # Function to map individual grades
    def grade_mapper(grade):
        if grade == '1':
            return '1'
        elif grade in ['2', 'T1']:
            return '2'
        elif grade in ['3', 'T2']:
            return '3'
        elif grade in ['4', 'T3']:
            return '4'
        elif grade in ['5', 'T4', 'C1']:
            return '5'
        elif grade in ['6', 'T5']:
            return '6'
        elif grade in ['7', 'T6', 'C2']:
            return '7'
        elif grade == '8':
            return '8'
        elif grade == '9':
            return '9'
        elif grade == '10':
            return '10'
        elif grade == '11':
            return '11'
        elif grade == '12':
            return '12'
        elif grade == '13':
            return '13'
        elif grade == 'CEO':
            return 'CEO'
        else:
            return 'Trainees'

    try:
        # Load the Excel file
        data = pd.read_excel(file_path)

        # Ensure date columns are in datetime format
        if 'Date of Joining' in data.columns:
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')

        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y',
                                                             errors='coerce')

        # If the month is 'all', iterate over all months
        if month == 'all':
            for m in range(1, 13):
                month_cutoff_date = pd.Timestamp(f'2024-{m:02d}-01')
                # Filter data based on the new criteria for the specified month
                filtered_data = data[
                    ((data['Actual Termination date'].isna()) | (
                                data['Actual Termination date'] >= month_cutoff_date)) &
                    (data['Date of Joining'] < month_cutoff_date) &
                    (data['Job title - English'] != 'Board Member')
                    ]


                # Check if the Gender and Grade columns exist
                if 'Gender' in filtered_data.columns and 'Grade' in filtered_data.columns:
                    # Map the Grade column using the defined mapping function with assign
                    filtered_data = filtered_data.assign(Grade=filtered_data['Grade'].apply(grade_mapper))

                    # Filter the data to include only Male and Female genders
                    filtered_data = filtered_data[filtered_data['Gender'].isin(['Male', 'Female'])]

                    # Group by Grade and Gender, then count occurrences
                    grade_gender_counts = filtered_data.groupby(['Grade', 'Gender']).size().unstack(fill_value=0)

                    # Calculate total count per grade and add it as a column
                    grade_gender_counts['Total'] = grade_gender_counts.sum(axis=1)

                    # Sort the DataFrame by the Total column in descending order
                    sorted_counts = grade_gender_counts.sort_values(by='Total', ascending=False)

                    # Print counts of Male and Female by Grade with the Total column
                    print(f'Count of employees by Grade and Gender for {month_cutoff_date.strftime("%B, %Y")}:')
                    print(sorted_counts)
                else:
                    print('Missing columns Gender or Grade in the dataset.')

        else:
            # Define the cutoff date for the specified month
            month_cutoff_date = pd.Timestamp(f'2024-{month:02d}-01')
            filtered_data = data[
                ((data['Actual Termination date'].isna()) | (data['Actual Termination date'] >= month_cutoff_date)) &
                (data['Date of Joining'] < month_cutoff_date) &
                (data['Job title - English'] != 'Board Member')
                ]


            # Check if the Gender and Grade columns exist
            if 'Gender' in filtered_data.columns and 'Grade' in filtered_data.columns:
                # Map the Grade column using the defined mapping function with assign
                filtered_data = filtered_data.assign(Grade=filtered_data['Grade'].apply(grade_mapper))

                # Filter the data to include only Male and Female genders
                filtered_data = filtered_data[filtered_data['Gender'].isin(['Male', 'Female'])]

                # Group by Grade and Gender, then count occurrences
                grade_gender_counts = filtered_data.groupby(['Grade', 'Gender']).size().unstack(fill_value=0)

                # Calculate total count per grade and add it as a column
                grade_gender_counts['Total'] = grade_gender_counts.sum(axis=1)

                # Sort the DataFrame by the Total column in descending order
                sorted_counts = grade_gender_counts.sort_values(by='Total', ascending=False)

                # Print counts of Male and Female by Grade with the Total column
                print(f'Count of employees by Grade and Gender for {month_cutoff_date.strftime("%B, %Y")}:')
                print(sorted_counts)
            else:
                print('Missing columns Gender or Grade in the dataset.')

    except UnicodeDecodeError:
        print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')



map_grade(4)  # For April
map_grade('all')  # For all months
