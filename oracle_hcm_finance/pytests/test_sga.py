import pytest
from oracle_hcm_finance.Finance_KPIs.YTD_SGA_kpis import SGA

@pytest.mark.parametrize("month, expected_output", [
    (1, "Processing sheet for January"),
    (2, "Processing sheet for February"),
    (3, "Processing sheet for March"),
    (4, "Processing sheet for April"),
    (5, "Processing sheet for May"),
    (6, "Processing sheet for June"),
    (7, "Processing sheet for July"),
    (8, "Processing sheet for August"),
    (9, "Processing sheet for September"),
])
def test_sga(month, expected_output, capsys):
    SGA(month)  # Call the SGA function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
