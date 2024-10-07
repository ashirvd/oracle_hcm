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
], ids=[
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September"
])

@pytest.mark.run(order=1)
def test_ebit(month, expected_output, capsys):
    ebit(month)  # Call the ebit function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout
    # Check if the expected output is in the captured output


    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)
#pytest test_ebit.py --html=report_ebit.html --self-contained-html
#pip install pytest-ordering

#run this command to run all pytests in 'pytests' folder
#pytest --html=all_reports.html
