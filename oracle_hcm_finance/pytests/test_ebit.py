import pytest
from oracle_hcm_finance.Finance_KPIs.YTD_EBIT_kpis import ebit

@pytest.mark.parametrize("month, expected_output", [
    (1, "Using data for the month: January"),
    (2, "Using data for the month: February"),
    (3, "Using data for the month: March"),
    (4, "Using data for the month: April"),
    (5, "Using data for the month: May"),
    (6, "Using data for the month: June"),
    (7, "Using data for the month: July"),
    (8, "Using data for the month: August"),
    (9, "Using data for the month: September"),
])
def test_ebit(month, expected_output, capsys):
    ebit(month)  # Call the ebit function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout
    # Check if the expected output is in the captured output


    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
