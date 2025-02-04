import pytest

from oracle_hcm_finance.HCM_KPIs.promotion_by_grade_genderkpis import promotion_by_grade_gender

# Define the expected output just once
expected_output = "Total number of employees who got promoted in"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=18)
def test_promotion_by_grade_gender_month(month, capsys):
    promotion_by_grade_gender(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
