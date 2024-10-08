import pytest
from oracle_hcm_finance.Finance_KPIs.purchase_orders_kpis import purchase_orders

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

@pytest.mark.run(order=9)
def test_purchase_orders(capfd, month, month_name):
    # Call the function to process purchase orders for the given month
    purchase_orders(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    # Check if the output contains the processing statement for the month
    assert f'Month: {month_name}' in output

    # Check for the expected output structure (AOG, Urgent, Normal)
    assert 'AOG' in output
    assert 'Urgent' in output
    assert 'Normal' in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)

# Command to run:
# pytest test_purchase_orders_kpis.py --html=report_purchase_orders.html --self-contained-html
