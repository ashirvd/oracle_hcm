import pytest
from oracle_hcm_finance.HCM_KPIs.actual_vs_budget import actual_vs_budget
expected_output = "Month"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=9)
def test_actual_vs_budget_month(month, capsys):
        actual_vs_budget(month)
        captured = capsys.readouterr()  # Capture the output
        assert expected_output in captured.out  # Check if expected output is in captured stdout

        # Optionally, print all output for debugging purposes
        print("Captured Output:")
        print(captured.out)