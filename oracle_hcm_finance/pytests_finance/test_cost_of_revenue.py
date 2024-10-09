import pytest
from unittest.mock import patch
from oracle_hcm_finance.Finance_KPIs.cost_of_revenue import cost_of_revenue

@pytest.mark.parametrize("month, month_name", [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September")
], ids=[
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September"
])
@pytest.mark.run(order=5)
def test_cost_of_revenue(capfd, month, month_name):
    cost_of_revenue(month)  # Call the function to execute the print statements
    captured = capfd.readouterr()  # Capture the output
    output = captured.out  # Get the standard output

    # Check if the expected processing message is in the captured output
    assert f'Processing financial metrics for: {month_name}' in output
    assert f'Cost of Revenue % for {month_name}:' in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
#pytest test_cost_of_revenue.py --html=report_cost_of_revenue.html --self-contained-html
