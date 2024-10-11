import pandas as pd
from datetime import datetime

# Load the Excel file
file_path = '../data_hcm/Employee Data Without Payroll Details ΓÇô Active and Inactive_Output.xlsx'
df = pd.read_excel(file_path)

# Ensure columns are in the right format
df['Actual Termination date'] = pd.to_datetime(df['Actual Termination date'], errors='coerce')
df['Date of Joining'] = pd.to_datetime(df['Date of Joining'], errors='coerce')

# Filter out employees terminated before 1 January 2024
cutoff_date = pd.Timestamp('2024-01-01')
active_employees = df[df['Actual Termination date'] < cutoff_date]

# Function to categorize employees based on experience
def categorize_experience(joining_date):
    if pd.isna(joining_date):
        return None
    today = datetime.today()
    experience_years = (today - joining_date).days / 365.25
    if experience_years < 1:
        return '<1 year'
    elif 1 <= experience_years < 3:
        return '1-3 years'
    elif 3 <= experience_years < 5:
        return '3-5 years'
    else:
        return '>5 years'

# Apply categorization to the active employees
active_employees['Experience Category'] = active_employees['Date of Joining'].apply(categorize_experience)

# Calculate total employees in each category
category_counts = active_employees['Experience Category'].value_counts()

# Calculate percentages
total_employees = active_employees.shape[0]
category_percentages = (category_counts / total_employees) * 100

# Output the results
print("Total Employees by Experience Category:")
print(category_counts)
print("\nPercentage of Employees in each Category:")
print(category_percentages)
