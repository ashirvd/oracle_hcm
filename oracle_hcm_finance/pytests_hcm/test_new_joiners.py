import pytest

# Import the original new_joiners function
from oracle_hcm_finance.HCM_KPIs.new_joiners_pipeline_kpis import new_joiners

# Define the expected output just once
expected_output = "Total number of new joiners"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
@pytest.mark.run(order=4)
def test_new_joiners(month, capsys):
    # Call the new_joiners function directly without mocking
    new_joiners(month)  # Call the new_joiners function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

