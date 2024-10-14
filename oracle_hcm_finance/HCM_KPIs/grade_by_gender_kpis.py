import pandas as pd
import os

# Function to map grades using a custom grade_mapper function
def grade_mapper(grade):
    if grade == '1':
        return '1'
    elif grade in ['2', 'T1']:
        return '2'
    elif grade in ['3', 'T2']:
        return '3'
    elif grade in ['4', 'T3']:
        return '4'
    elif grade in ['5', 'T4', 'C1', 'S1']:
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

def map_grade(month):
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'
    year = 2024

    if not os.path.exists(file_path):
        print(f'The specified file "{file_path}" was not found. Skipping...')
        return

    try:
        data = pd.read_excel(file_path)

        if 'Date of Joining' in data.columns:
            data['Date of Joining'] = pd.to_datetime(data['Date of Joining'], format='%d-%b-%Y', errors='coerce')
        if 'Actual Termination date' in data.columns:
            data['Actual Termination date'] = pd.to_datetime(data['Actual Termination date'], format='%d-%b-%Y', errors='coerce')

        today = pd.Timestamp.now()

        def get_active_employees(data, month):
            months = range(1, 13) if month == 'all' else [month]
            active_data = pd.DataFrame()

            for m in months:
                month_cutoff_date = pd.Timestamp(f'{year}-{m:02d}-01')
                end_of_month = month_cutoff_date + pd.offsets.MonthEnd(1)

                filtered_data = data[
                    ((data['Actual Termination date'].isna()) | (data['Actual Termination date'] > end_of_month)) &
                    (data['Date of Joining'] <= end_of_month) &
                    (data['Job title - English'] != 'Board Member')
                ]
                active_data = pd.concat([active_data, filtered_data])

            return active_data

        filtered_data = get_active_employees(data, month)

        if 'Gender' in filtered_data.columns and 'Grade' in filtered_data.columns:

            filtered_data['Mapped_Grade'] = filtered_data['Grade'].apply(grade_mapper)
            filtered_data = filtered_data[filtered_data['Gender'].isin(['Male', 'Female'])]

            grade_gender_counts = filtered_data.groupby(['Mapped_Grade', 'Gender']).size().unstack(fill_value=0)
            grade_gender_counts['Total'] = grade_gender_counts.sum(axis=1)
            sorted_counts = grade_gender_counts.sort_values(by='Total', ascending=False)

            if month == 'all':
                for m in range(1, 13):
                    month_data = get_active_employees(data, m)
                    if not month_data.empty:
                        month_data['Mapped_Grade'] = month_data['Grade'].apply(grade_mapper)
                        month_data = month_data[month_data['Gender'].isin(['Male', 'Female'])]

                        month_grade_gender_counts = month_data.groupby(['Mapped_Grade', 'Gender']).size().unstack(fill_value=0)
                        month_grade_gender_counts['Total'] = month_grade_gender_counts.sum(axis=1)
                        sorted_month_counts = month_grade_gender_counts.sort_values(by='Total', ascending=False)

                        print(f'Count of employees by Grade and Gender for {pd.Timestamp(year=year, month=m, day=1).strftime("%B, %Y")}:')
                        print(sorted_month_counts)
            else:
                print(f'Count of employees by Grade and Gender for {pd.Timestamp(year=year, month=month, day=1).strftime("%B, %Y")}:')
                print(sorted_counts)
        else:
            print('Missing columns Gender or Grade in the dataset.')

    except UnicodeDecodeError:
        print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')

# map_grade(1)
map_grade('all')
