import pytest
from oracle_hcm_finance.HCM_KPIs.promotions_count_kpis import promotion_count

# Define the expected output pattern
expected_output_pattern = "Number of promotions in month"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=6)
def test_promotion_month(month, capsys):
    promotion_count(month)
    captured = capsys.readouterr()  # Capture the output

    # Check if expected output is in captured stdout
    assert expected_output_pattern in captured.out

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

