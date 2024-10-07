import pytest
from oracle_hcm_finance.Finance_KPIs.receivables_ageing_kpis import receivables_ageing  # Adjust the import according to your module structure

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

#@pytest.mark.run(order=8)  # Adjust the order if necessary
def test_receivables_ageing(capfd, month, month_name):
    # Call the function to process receivables for the given month
    receivables_ageing(month)

    # Capture the output from the function
    captured = capfd.readouterr()
    output = captured.out

    # Check if the expected output contains the processing statement for the month
    assert f'Processing file of month: {month_name}' in output

    # Check for the expected output structure (current and overdue amounts)
    assert 'Current Amount:' in output
    assert 'Overdue Amount:' in output

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(output)

# Command to run:
# pytest test_receivables_ageing_kpis.py --html=report_receivables_ageing.html --self-contained-html
