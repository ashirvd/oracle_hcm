import pytest

from oracle_hcm_finance.HCM_KPIs.head_count_summary_kpis import head_count

# Define the expected output pattern
expected_output_pattern = "Headcount for"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "All Months"
])
@pytest.mark.run(order=1)
def test_head_count_month(month, capsys):
    # Call the head_count function directly
    head_count(month)  # Call the head_count function
    captured = capsys.readouterr()  # Capture the output

    # Check if expected output is in captured stdout
    assert expected_output_pattern in captured.out

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)


