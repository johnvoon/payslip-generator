import pytest
import filecmp
from utils import *
from tax_brackets import tax_brackets


def test_convert_to_float():
    """
    Should convert a percentage string to float
    """
    assert convert_to_float('50%')
    assert convert_to_float('100%')


def test_round_nearest_whole_dollar_down():
    """
    Should round money amount if < 50 cents
    """
    assert round_nearest_whole_dollar(5004.15) == 5004
    assert round_nearest_whole_dollar(5004.4999) == 5004


def test_round_nearest_whole_dollar_up():
    """
    Should round money amount up if >= 50 cents
    """
    assert round_nearest_whole_dollar(5004.5) == 5005
    assert round_nearest_whole_dollar(5004.99) == 5005


def test_monthly_gross_income():
    """
    Should return correct monthly gross income given annual salary
    """
    assert monthly_gross_income(60050) == 5004
    assert monthly_gross_income(120000) == 10000


def test_monthly_income_tax():
    """
    Should return correct monthly income tax given annual salary and tax brackets
    """
    assert monthly_income_tax(18000, tax_brackets) == 0
    assert monthly_income_tax(60050, tax_brackets) == 922
    assert monthly_income_tax(120000, tax_brackets) == 2696


def test_monthly_income_tax_base_amounts():
    """
    Should return correct monthly income tax base amounts
    """
    assert monthly_income_tax(18200, tax_brackets) == 0
    assert monthly_income_tax(37000, tax_brackets) == 298
    assert monthly_income_tax(80000, tax_brackets) == 1462
    assert monthly_income_tax(180000, tax_brackets) == 4546


def test_monthly_net_income_60050():
    """
    Should return correct monthly net income if annual salary is $60,050
    """
    gross_income = monthly_gross_income(60050)
    income_tax = monthly_income_tax(60050, tax_brackets)
    assert monthly_net_income(gross_income, income_tax) == 4082


def test_monthly_net_income_120000():
    """
    Should return correct monthly net income if annual salary is $120,000
    """
    gross_income = monthly_gross_income(120000)
    income_tax = monthly_income_tax(120000, tax_brackets)
    assert monthly_net_income(gross_income, income_tax) == 7304


def test_monthly_super_amount():
    """
    Should return correct monthly super amount
    """
    gross_income = monthly_gross_income(60050)
    super_rate = 0.09
    assert monthly_super_amount(gross_income, super_rate) == 450


def test_parse_csv_from_file():
    """
    Should parse CSV file and return extracted employee data
    """
    mock_csv_file = open('mock_employee_data.csv', 'r')
    mock_employee_data = [
        {
            'first_name': 'David',
            'last_name': 'Rudd',
            'annual_salary': 60050,
            'super_rate': 0.09,
            'payment_period': '01 March - 31 March'
        },
        {
            'first_name': 'Ryan',
            'last_name': 'Chen',
            'annual_salary': 120000,
            'super_rate': 0.1,
            'payment_period': '01 March - 31 March'
        }
    ]

    assert parse_csv_from_file(mock_csv_file) == mock_employee_data
    mock_csv_file.close()


def test_generate_payslip_data():
    """
    Should generate payslip data from employee data extracted from CSV file
    """
    mock_csv_file = open('mock_employee_data.csv', 'r')
    employee_data = parse_csv_from_file(mock_csv_file)
    mock_payslip_data = [
        {
            'full_name': 'David Rudd',
            'payment_period': '01 March - 31 March',
            'gross_income': Decimal(5004),
            'income_tax': Decimal(922),
            'net_income': Decimal(4082),
            'super_amount': Decimal(450)
        },
        {
            'full_name': 'Ryan Chen',
            'payment_period': '01 March - 31 March',
            'gross_income': Decimal(10000),
            'income_tax': Decimal(2696),
            'net_income': Decimal(7304),
            'super_amount': Decimal(1000)
        }
    ]

    assert generate_payslip_data(employee_data) == mock_payslip_data
    mock_csv_file.close()


def test_generate_csv_output():
    """
    Should generate CSV output file from payslip data
    """
    mock_payslip_data = [
        {
            'full_name': 'David Rudd',
            'payment_period': '01 March - 31 March',
            'gross_income': Decimal(5004),
            'income_tax': Decimal(922),
            'net_income': Decimal(4082),
            'super_amount': Decimal(450)
        },
        {
            'full_name': 'Ryan Chen',
            'payment_period': '01 March - 31 March',
            'gross_income': Decimal(10000),
            'income_tax': Decimal(2696),
            'net_income': Decimal(7304),
            'super_amount': Decimal(1000)
        }
    ]
    payslip_output = generate_csv_output(mock_payslip_data)
    mock_payslip = open('mock_payslip.csv')

    assert payslip_output.getvalue() == mock_payslip.read()
    payslip_output.close()
    mock_payslip.close()
