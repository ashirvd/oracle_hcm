import pytest
from oracle_hcm_finance.Finance_KPIs.sga_to_revenue import sga_to_revenue


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
])
def test_sga_to_revenue(capfd, month, month_name):
    # Call the function to execute the print statements
    sga_to_revenue(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    # Check if the expected processing message is in the captured output
    assert f'SG&A to Revenue % for {month_name}:' in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
#pytest  test_sga_to_revenue.py --html=report_sga_to_revenue.html --self-contained-html
