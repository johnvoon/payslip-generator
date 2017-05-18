import csv
import codecs
from io import StringIO
from flask import Response
from decimal import Decimal, ROUND_HALF_UP
from tax_brackets import tax_brackets


def convert_to_float(percentage):
    """
    Convert percentage to float
    """
    return float(percentage.strip('%')) / 100


def round_nearest_whole_dollar(amount):
    """
    Round a monetary amount to the nearest whole dollar,
    e.g.    round_nearest_whole_dollar(5000.30) == 5000
            round_nearest_whole_dollar(5000.50) == 5001
    """
    amount = Decimal(amount)
    return amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def monthly_gross_income(annual_salary):
    """
    Calculate monthly gross income given an annual salary amount
    """
    gross_income = annual_salary / 12
    return round_nearest_whole_dollar(gross_income)


def monthly_income_tax(annual_salary, tax_brackets):
    """
    Calculate monthly income tax payable given an annual salary amount
    and array of tax rates
    """
    income_tax = 0

    for index, bracket in enumerate(tax_brackets):
        if annual_salary >= bracket['threshold']:
            if index == 0:
                income_tax += bracket['threshold'] * bracket['rate']
            else:
                threshold_difference = bracket['threshold'] - \
                    tax_brackets[index - 1]['threshold']
                income_tax += threshold_difference * bracket['rate']
        else:
            if index == 0:
                additional_salary = annual_salary - bracket['threshold']
                income_tax += additional_salary * bracket['rate']
                return income_tax / 12
            else:
                additional_salary = annual_salary - \
                    tax_brackets[index - 1]['threshold']
                income_tax += additional_salary * bracket['rate']
                return round_nearest_whole_dollar(income_tax / 12)


def monthly_net_income(gross_income, income_tax):
    """
    Calculate monthly net income given the gross income
    and income tax
    """
    return gross_income - income_tax


def monthly_super_amount(gross_income, super_rate):
    """
    Calculate the super amount given the gross income
    and super rate
    """
    super_amount = gross_income * Decimal(super_rate)
    return round_nearest_whole_dollar(super_amount)


def parse_csv_from_file(file):
    """
    Open a CSV file, extract and return employee data
    in the form of a list of dictionaries
    """
    csvFileReader = None
    employee_data = []

    # if FileStorage object (which has a save() method)
    if hasattr(file, 'save'):
        csvFileReader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    # else if File object (which does not have a save() method)
    else:
        csvFileReader = csv.reader(file)

    for row in csvFileReader:
        employee_data.append({
            'first_name': row[0],
            'last_name': row[1],
            'annual_salary': int(row[2]),
            'super_rate': convert_to_float(row[3]),
            'payment_period': row[4]
        })

    return employee_data


def generate_payslip_data(employee_data):
    """
    Generate payslip data in the form of a list of dictionaries given parsed CSV employee data
    """
    payslip_data = []

    for employee in employee_data:
        gross_income = monthly_gross_income(employee['annual_salary'])
        income_tax = monthly_income_tax(
            employee['annual_salary'], tax_brackets)
        net_income = monthly_net_income(
            gross_income, income_tax)
        super_amount = monthly_super_amount(
            gross_income, employee['super_rate'])

        payslip_data.append({
            'full_name': employee['first_name'] + ' ' + employee['last_name'],
            'payment_period': employee['payment_period'],
            'gross_income': gross_income,
            'income_tax': income_tax,
            'net_income': net_income,
            'super_amount': super_amount
        })

    return payslip_data


def generate_csv_output(payslip_data):
    """
    Generate a StringIO object representing a CSV file
    from payslip data in the form of a list of dictionaries
    """
    payslip_output = StringIO(newline=None)
    csvFileWriter = csv.writer(payslip_output, delimiter=',')

    data = [['Full Name', 'Payment Period', 'Gross Income',
             'Income Tax', 'Net Income', 'Super']]

    for employee in payslip_data:
        data.append([
            employee['full_name'],
            employee['payment_period'],
            str(employee['gross_income']),
            str(employee['income_tax']),
            str(employee['net_income']),
            str(employee['super_amount'])
        ])

    csvFileWriter.writerows(data)

    return payslip_output
