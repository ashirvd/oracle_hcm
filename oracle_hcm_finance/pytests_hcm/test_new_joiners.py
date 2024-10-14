import pytest

from oracle_hcm_finance.HCM_KPIs.new_joiners_pipeline_kpis import new_joiners_pipeline

# Define the expected output just once
expected_output = "Total new joiners"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=14)
def test_new_joiners_month(month, capsys):
    new_joiners_pipeline(month)  # Call the function with a specific month
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
