import pytest
from oracle_hcm_finance.Finance_KPIs.managed_spend_kpis import managed_spend
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

@pytest.mark.run(order=8)
def test_managed_spend(capfd, month, month_name):
    # Call the function to process receivables for the given month
    managed_spend(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    # Check if the output contains the expected month
    assert f'Month: {month_name}' in output

    # Check for the presence of each PO type in the output
    assert 'Direct Purchase ' in output
    assert 'Sole Source ' in output
    assert 'Single Source ' in output
    assert 'Competitive ' in output
    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)
