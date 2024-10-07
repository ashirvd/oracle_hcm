import pandas as pd

file_path = '../datasources/PromotionbyGender.csv'

def without_filter_by_grade():
    try:
        csv_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')  # Try different encodings if necessary

        # Get the total number of rows
        total_rows = csv_data.shape[0]
        print(f'Total number of records in the CSV file: {total_rows}')

        # Count non-empty entries in the 'Grade Change Date' column
        non_empty_grade_change_date_count = csv_data['Grade Change Date'].notna().sum()

        # Filter rows where 'Grade Change Date' is not empty
        filtered_data = csv_data[csv_data['Grade Change Date'].notna()]

        # Get the total number of employees with a non-empty 'Grade Change Date'
        total_promoted = filtered_data.shape[0]

        # Count the number of males and females in the filtered data
        gender_counts = filtered_data['Gender'].value_counts()

        # Count the number of employees for each grade, broken down by gender
        grade_gender_counts = filtered_data.groupby(['Grade', 'Gender']).size().unstack(fill_value=0)

        # Print the results
        print(f'Total number of employees who got promoted: {total_promoted}')
        print(f'Number of Males got promotion {gender_counts.get("Male", 0)}')
        print(f'Number of Females got promotion: {gender_counts.get("Female", 0)}')
        print('\nNumber of employees for each grade:')

        for grade in grade_gender_counts.index:
            male_count = grade_gender_counts.loc[grade].get('Male', 0)
            female_count = grade_gender_counts.loc[grade].get('Female', 0)
            print(f'Grade {grade}: Male = {male_count}, Female = {female_count}')

    except UnicodeDecodeError:
        print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')

def filter_by_grade_change_date(df, year=None, month=None, quarter=None):
    """
    Filter the DataFrame based on year, month, and quarter for 'Grade Change Date'.
    Only records with valid 'Grade Change Date' will be considered.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing employee data.
    - year (int, optional): The year to filter by.
    - month (int, optional): The month to filter by (1 to 12).
    - quarter (int, optional): The quarter to filter by (1 to 4).

    Returns:
    - pd.DataFrame: The filtered DataFrame based on the specified criteria.
    """
    if 'Grade Change Date' in df.columns:
        # Convert 'Grade Change Date' to datetime format for filtering purposes
        df = df.copy()  # Make a copy to avoid modifying the original DataFrame
        df['Grade Change Date'] = pd.to_datetime(df['Grade Change Date'], format='%d-%b-%Y', errors='coerce')  # Adjust format as necessary

        # Remove rows where 'Grade Change Date' couldn't be parsed
        df = df.dropna(subset=['Grade Change Date'])

        if year is not None:
            # Filter by year
            df = df[df['Grade Change Date'].dt.year == year]

        if month is not None:
            # Filter by month
            df = df[df['Grade Change Date'].dt.month == month]

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
                df = df[df['Grade Change Date'].dt.month.isin(quarters[quarter])]

    else:
        print('Grade Change Date column is not in dataset')

    return df

try:
    csv_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')  # Adjust encoding as necessary

    # Get the total number of rows
    total_rows = csv_data.shape[0]
    print(f'Total number of records in the CSV file: {total_rows}')

    # Filter data by date
    filtered_data = filter_by_grade_change_date(csv_data, year=None, month=None, quarter=None)

    # Get the total number of employees with a non-empty 'Grade Change Date'
    total_promoted = filtered_data.shape[0]
    print(f'Total number of employees who got promoted: {total_promoted}')

    # Count the number of males and females in the filtered data
    gender_counts = filtered_data['Gender'].value_counts()
    print(f'Number of Males who got promotion: {gender_counts.get("Male", 0)}')
    print(f'Number of Females who got promotion: {gender_counts.get("Female", 0)}')

    # Count the number of employees for each grade, broken down by gender
    grade_gender_counts = filtered_data.groupby(['Grade', 'Gender']).size().unstack(fill_value=0)

    print('\nNumber of employees for each grade:')
    for grade in grade_gender_counts.index:
        male_count = grade_gender_counts.loc[grade].get('Male', 0)
        female_count = grade_gender_counts.loc[grade].get('Female', 0)
        print(f'Grade {grade}: Male = {male_count}, Female = {female_count}')

except UnicodeDecodeError:
    print('Failed to load file with ISO-8859-1 encoding. Trying a different encoding.')
