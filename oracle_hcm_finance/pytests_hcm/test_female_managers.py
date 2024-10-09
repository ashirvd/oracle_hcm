import pytest
from oracle_hcm_finance.HCM_KPIs.female_managers_kpis import female_managers


@pytest.mark.parametrize("month, expected_output", [
    (1, "Female managers in January:"),
    (2, "Female managers in February:"),
    (3, "Female managers in March:"),
    (4, "Female managers in April:"),
    (5, "Female managers in May:"),
    (6, "Female managers in June:"),
    (7, "Female managers in July:"),
    (8, "Female managers in August:"),
    (9, "Female managers in September:"),
    (10, "Female managers in October:"),
    (11, "Female managers in November:"),
    (12, "Female managers in December:"),
], ids=[
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
])
@pytest.mark.run(order=2)
def test_female_managers(month, expected_output, capsys):
    female_managers(month)  # Call the female_managers function
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)

    # pytest test_female_managers.py --html=report_test_female_managers.html --self-contained-html
    # pip install pytest-ordering

    # run this command to run all pytests in 'pytests_hcm' folder
    # cd oracle_hcm_finance\pytests_hcm
    # pytest --html=hcm_all_reports.html
