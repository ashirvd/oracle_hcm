import pytest

from oracle_hcm_finance.HCM_KPIs.grade_by_gender_kpis import map_grade

# Define the expected output just once
expected_output = "Count of employees by Grade and Gender for"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=14)
def test_grade_by_gender_month(month, capsys):
    map_grade(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output for Month:")
    print(captured.out)

