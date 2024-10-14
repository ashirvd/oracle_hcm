import pytest

from oracle_hcm_finance.HCM_KPIs.joiners_by_age_gender_kpis import joiners_by_age_gender

# Define the expected output just once
expected_output = "Counts"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=20)
def test_joiners_by_age_gender_month(month, capsys):
    joiners_by_age_gender(month)
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)


