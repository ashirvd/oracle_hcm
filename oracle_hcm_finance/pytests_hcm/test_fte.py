import pytest

# Import the original calculate_fte function
from oracle_hcm_finance.HCM_KPIs.FTE_summary_kpis import calculate_fte

# Define the expected output just once
expected_output = "Total FTE for "

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
@pytest.mark.run(order=8)
def test_fte__month(month, capsys):
    # Call the calculate_fte function directly without mocking
    calculate_fte(month)  # Call the calculate_fte function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)


