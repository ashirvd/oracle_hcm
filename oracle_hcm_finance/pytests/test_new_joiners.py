import pytest
from unittest.mock import patch

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
@pytest.mark.run(order=1)
def test_new_joiners(month, capsys):
    with patch('oracle_hcm_finance.HCM_KPIs.n_new_joiners_pipeline_kpis.new_joiners') as mock_new_joiners:
        mock_new_joiners.return_value = None  # Adjust this if necessary

        # Call the new_joiners function
        new_joiners(month)  # Call the new_joiners function
        captured = capsys.readouterr()  # Capture the output
        assert expected_output in captured.out  # Check if expected output is in captured stdout

        # Optionally, print all output for debugging purposes
        print("Captured Output:")
        print(captured.out)

# To run the tests, you would typically use a command like:
# pytest test_new_joiners.py --html=report_new_joiners.html --self-contained-html
