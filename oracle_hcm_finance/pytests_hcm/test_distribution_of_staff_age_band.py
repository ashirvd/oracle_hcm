import pytest

from oracle_hcm_finance.HCM_KPIs.distribution_of_staff_age_band_kpis import distribution_staff_age_band

# Define the expected output just once
expected_output = "Headcount"

@pytest.mark.parametrize("month", [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'all'
], ids=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "All Months"
])
@pytest.mark.run(order=22)
def test_distribution_staff_age_band_month(month, capsys):
    distribution_staff_age_band(month)
    captured = capsys.readouterr()  # Capture the output
    assert expected_output in captured.out  # Check if expected output is in captured stdout

    # Optionally, print all output for debugging purposes
    print("Captured Output:")
    print(captured.out)


