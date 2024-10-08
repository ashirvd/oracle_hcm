import pytest

from oracle_hcm_finance.HCM_KPIs.female_managers_kpis import female_managers

# Define the expected output just once
expected_output = "Female managers in "

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
@pytest.mark.run(order=2)
def test_female_managers_month(month, capsys):
    # Call the female_managers function directly without mocking
    female_managers(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

