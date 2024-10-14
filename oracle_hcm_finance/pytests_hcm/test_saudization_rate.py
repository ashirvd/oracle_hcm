import pytest

from oracle_hcm_finance.HCM_KPIs.saudization_rate_kpis import saudization_filter

# Define the expected output just once
expected_output = "Saudization Rate for"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=12)
def test_saudization_filter_month(month, capsys):
    saudization_filter(month)  # Call the saudization_filter function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
