import pytest

# Import the original management_vs_staff function
from oracle_hcm_finance.HCM_KPIs.management_vs_staff_kpis import management_vs_staff

# Define the expected output just once
expected_output = "Management vs Staff ratio of"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
@pytest.mark.run(order=9)
def test_management_vs_staff_month(month, capsys):
    # Call the management_vs_staff function directly without mocking
    management_vs_staff(month)  # Call the management_vs_staff function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

