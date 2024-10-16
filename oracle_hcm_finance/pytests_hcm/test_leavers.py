import pytest

from oracle_hcm_finance.HCM_KPIs.leavers import leavers

# Define the expected output pattern
expected_output_pattern = "Total number of leavers in"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=5)
def test_leavers_month(month, capsys):
    leavers(month)  # Call the leavers function
    captured = capsys.readouterr()  # Capture the output

    # Check if expected output is in captured stdout
    assert expected_output_pattern in captured.out

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)


