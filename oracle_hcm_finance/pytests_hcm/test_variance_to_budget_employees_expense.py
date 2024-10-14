import pytest
from oracle_hcm_finance.HCM_KPIs.variance_to_budget_employees_expenses import variance_to_budget
expected_output = "Month"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=10)
def test_variance_to_budget_employees_expenses_month(month, capsys):
    variance_to_budget(month)
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
