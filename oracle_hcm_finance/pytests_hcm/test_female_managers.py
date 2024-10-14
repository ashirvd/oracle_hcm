import pytest

from oracle_hcm_finance.HCM_KPIs.female_managers_kpis import female_managers

expected_output = "Female"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=3)
def test_female_managers_month(month, capsys):
    female_managers(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

