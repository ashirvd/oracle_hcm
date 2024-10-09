import pytest
from oracle_hcm_finance.Finance_KPIs.variance_to_budget import variance_to_budget


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

@pytest.mark.run(order=4)
def test_variance_to_budget(capfd, month, month_name):
    # Call the function to execute the print statements
    variance_to_budget(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    assert "Processing sheet:" in output
    assert "Financial variances (in millions):" in output
    assert "Revenue: Variance =" in output
    assert "Gross Profit: Variance =" in output
    assert "EBIT: Variance =" in output
    assert "Net Income: Variance =" in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
