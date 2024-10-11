import pytest
from oracle_hcm_finance.HCM_KPIs.staff_cost import staff_cost

@pytest.mark.parametrize("month", [1, 2, 3, 4, 5, 6, 7,8], ids=[
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August"
])
@pytest.mark.run(order=7)
def test_staff_cost_month(month, capsys):
    staff_cost(month)  # Call the actual_vs_budget function
    captured = capsys.readouterr()  # Capture the output
    assert "Processing file for month" in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
