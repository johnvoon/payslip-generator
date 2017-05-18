"""
Employee Model
"""
from db import db


class Employee(db.Model):
    """
    Employee info
    """
    __tablename__ = 'employees'

    # Employee details
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    annual_salary = db.Column(db.Integer())
    super_rate = db.Column(db.Numeric())

    # Relationships
    payslips = db.relationship('Payslip',
                               backref=db.backref(
                                   'employee', lazy='joined'),
                               lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def to_json(self):
        """
        Convert an Employee instance to JSON format
        """
        return {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'annualSalary': self.annual_salary,
            'superRate': '{}%'.format(self.super_rate * 100),
            'payslips': [payslip.json() for payslip in self.payslips.all()]
        }

    def save_to_db(self):
        """
        Save Employee to database
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete Employee from database
        """
        db.session.delete(self)
        db.session.commit()
