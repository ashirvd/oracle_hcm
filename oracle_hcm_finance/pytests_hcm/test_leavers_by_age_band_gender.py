import pytest

from oracle_hcm_finance.HCM_KPIs.leavers_by_ageband_gender_kpis import leavers_by_age_gender

# Define the expected output just once
expected_output = "Total number of leavers in"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=21)
def test_leavers_by_age_gender_month(month, capsys):
    leavers_by_age_gender(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
