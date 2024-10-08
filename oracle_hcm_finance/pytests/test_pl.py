import pytest
from oracle_hcm_finance.Finance_KPIs.pl import pl

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
@pytest.mark.run(order=3)
def test_pl(capfd, month, expected_output):
    pl(month)  # Call the function to execute the print statements
    captured = capfd.readouterr()  # Capture the output
    output = captured.out  # Get the standard output

    # Check if the expected output is in the captured output
    assert expected_output in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
#pytest test_pl.py --html=report_pl.html --self-contained-html
