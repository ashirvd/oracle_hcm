import pytest
from oracle_hcm_finance.Finance_KPIs.sga_percentage import sga_percentage


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
], ids=["January", "February", "March", "April", "May", "June", "July", "August", "September"])

@pytest.mark.run(order=7)
def test_sga_percentage(capfd, month, month_name):
    # Call the function to calculate SG&A % for the month
    sga_percentage(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    # Check if the expected output contains SG&A % for the month
    assert f'SG&A % for {month_name}:' in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
