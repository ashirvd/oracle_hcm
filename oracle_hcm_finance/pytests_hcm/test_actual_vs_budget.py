import pytest
from oracle_hcm_finance.HCM_KPIs.actual_vs_budget import actual_vs_budget  # Adjust import as necessary

@pytest.mark.parametrize("month", [1, 2, 3, 4, 5, 6, 7], ids=[
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July"
])
@pytest.mark.run(order=6)
def test_actual_vs_budget_month(month, capsys):
    actual_vs_budget(month)  # Call the actual_vs_budget function
    captured = capsys.readouterr()  # Capture the output
    assert "Percentage for the" in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
