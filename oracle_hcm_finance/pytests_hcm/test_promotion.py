import pytest
import os

# Import the original promotion_count function
from oracle_hcm_finance.HCM_KPIs.promotions_count_kpis import promotion_count

# Define the expected output pattern
expected_output_pattern = "Number of promotions in month"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=5)
def test_promotion_month(month, capsys):
    # Call the promotion_count function for the specified month
    promotion_count(month)
    captured = capsys.readouterr()  # Capture the output

    # Check if expected output is in captured stdout
    assert expected_output_pattern in captured.out

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

