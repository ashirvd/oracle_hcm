import pytest
import os
import pandas as pd
from oracle_hcm_finance.HCM_KPIs.gender_distribution_kpis import gender_distribution

# Define the expected output just once
expected_output = "Gender distribution for "

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=13)
def test_gender_distribution(month, capsys):
    # Call the gender_distribution function
    gender_distribution(month)  # Call the gender_distribution function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

