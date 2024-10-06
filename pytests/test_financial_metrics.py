import pytest
from oracle_hcm_finance.Finance_KPIs.financial_metrics import financial_metrics

@pytest.mark.parametrize("month, expected_output", [
    (1, "Processing financial metrics for: January"),
    (2, "Processing financial metrics for: February"),
    (3, "Processing financial metrics for: March"),
    (4, "Processing financial metrics for: April"),
    (5, "Processing financial metrics for: May"),
    (6, "Processing financial metrics for: June"),
    (7, "Processing financial metrics for: July"),
    (8, "Processing financial metrics for: August"),
    (9, "Processing financial metrics for: September"),
])
def test_financial_metrics(capfd, month, expected_output):
    financial_metrics(month)  # Call the function to execute the print statements
    captured = capfd.readouterr()  # Capture the output
    output = captured.out  # Get the standard output

    # Check if the expected output is in the captured output
    assert expected_output in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
