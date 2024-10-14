import pandas as pd

def promotion_by_grade_gender(month):
    """
    This function reads the employee data, filters it by the specified month or all months
    for the year 2024, and calculates the number of promotions by grade and gender.

    Parameters:
    - month (int or str): The month (1 to 12) to filter the promotions for the year 2024,
                          or 'all' to get results for all months.

    Returns:
    - None: Prints the promotion statistics by grade and gender.
    """
    file_path = '../data_hcm/KPI Dashboard - Employee Data Without Payroll Details – Active and Inactive_Output1 (1) (1).xlsx'

    def map_grade(grade):
        """
        Maps the original grade to the standardized grade format.

        Parameters:
        - grade (str): The original grade value.

        Returns:
        - str: The standardized grade.
        """
        if grade == '1':
            return '1'
        elif grade in ('2', 'T1'):
            return '2'
        elif grade in ('3', 'T2'):
            return '3'
        elif grade in ('4', 'T3'):
            return '4'
        elif grade in ('5', 'T4', 'C1'):
            return '5'
        elif grade in ('6', 'T5'):
            return '6'
        elif grade in ('7', 'T6', 'C2'):
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

    def get_date_range(month):
        """Calculate the start and end dates for a given month in 2024."""
        start_date = pd.Timestamp(year=2024, month=month, day=1)
        # If it's December, the end date should be January of the next year
        end_date = pd.Timestamp(year=2024, month=(month % 12 + 1), day=1)
        return start_date, end_date

    def filter_by_grade_change_date(df, start_date, end_date):
        """
        Filter the DataFrame based on the grade change date.
        Only records with valid 'Grade Change Date' will be considered.
        """
        if 'Grade Change Date' in df.columns:
            # Convert 'Grade Change Date' to datetime format for filtering purposes
            df = df.copy()  # Make a copy to avoid modifying the original DataFrame
            df['Grade Change Date'] = pd.to_datetime(df['Grade Change Date'], format='%d-%b-%Y',
                                                     errors='coerce')  # Adjust format as necessary

            # Remove rows where 'Grade Change Date' couldn't be parsed
            df = df.dropna(subset=['Grade Change Date'])

            # Filter by date range
            df = df[(df['Grade Change Date'] >= start_date) & (df['Grade Change Date'] < end_date)]

        else:
            print('Grade Change Date column is not in dataset')

        return df

    try:
        # Read the Excel file
        excel_data = pd.read_excel(file_path, engine='openpyxl')  # Use openpyxl engine for .xlsx files

        # Map the grades to standardized values
        excel_data['Mapped Grade'] = excel_data['Grade'].apply(map_grade)

        if month == 'all':
            for month in range(1, 13):  # Loop through each month from January to December
                start_date, end_date = get_date_range(month)
                filtered_data = filter_by_grade_change_date(excel_data, start_date, end_date)

                # Get the total number of employees with a non-empty 'Grade Change Date'
                total_promoted = filtered_data.shape[0]
                print(
                    f'Total number of employees who got promoted in {start_date.strftime("%B")} 2024: {total_promoted}')

                # Count the number of males and females in the filtered data
                gender_counts = filtered_data['Gender'].value_counts()
                print(
                    f'Number of Males who got promotion in {start_date.strftime("%B")} 2024: {gender_counts.get("Male", 0)}')
                print(
                    f'Number of Females who got promotion in {start_date.strftime("%B")} 2024: {gender_counts.get("Female", 0)}')

                # Count the number of employees for each grade, broken down by gender
                grade_gender_counts = filtered_data.groupby(['Mapped Grade', 'Gender']).size().unstack(fill_value=0)

                print(f'\nNumber of employees for each grade in {start_date.strftime("%B")} 2024:')
                for grade in grade_gender_counts.index:
                    male_count = grade_gender_counts.loc[grade].get('Male', 0)
                    female_count = grade_gender_counts.loc[grade].get('Female', 0)
                    print(f'Grade {grade}: Male = {male_count}, Female = {female_count}')
                print('\n' + '-' * 50)  # Separator for clarity between months

        else:
            # If month is not 'all', process normally for the specific month
            start_date, end_date = get_date_range(month)
            filtered_data = filter_by_grade_change_date(excel_data, start_date, end_date)

            # Get the total number of employees with a non-empty 'Grade Change Date'
            total_promoted = filtered_data.shape[0]
            print(
                f'Total number of employees who got promoted in {start_date.strftime("%B")} 2024: {total_promoted}')

            # Count the number of males and females in the filtered data
            gender_counts = filtered_data['Gender'].value_counts()
            print(
                f'Number of Males who got promotion in {start_date.strftime("%B")} 2024: {gender_counts.get("Male", 0)}')
            print(
                f'Number of Females who got promotion in {start_date.strftime("%B")} 2024: {gender_counts.get("Female", 0)}')

            # Count the number of employees for each grade, broken down by gender
            grade_gender_counts = filtered_data.groupby(['Mapped Grade', 'Gender']).size().unstack(fill_value=0)

            print(f'\nNumber of employees for each grade in {start_date.strftime("%B")} 2024:')
            for grade in grade_gender_counts.index:
                male_count = grade_gender_counts.loc[grade].get('Male', 0)
                female_count = grade_gender_counts.loc[grade].get('Female', 0)
                print(f'Grade {grade}: Male = {male_count}, Female = {female_count}')

    except FileNotFoundError:
        print(f'Error: The file {file_path} was not found.')
    except Exception as e:
        print(f'An error occurred: {e}')


# Example usage for all months
promotion_by_grade_gender('all')
promotion_by_grade_gender(3)
