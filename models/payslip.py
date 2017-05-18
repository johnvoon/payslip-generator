"""
Payslip Model
"""
from db import db


class Payslip(db.Model):
    """
    Payslip info
    """
    __tablename__ = 'payslips'

    # Payslip details
    id = db.Column(db.Integer, primary_key=True)
    payment_period_start = db.Column(db.Date())
    payment_period_end = db.Column(db.Date())
    gross_income = db.Column(db.Numeric())
    income_tax = db.Column(db.Numeric())
    net_income = db.Column(db.Numeric())
    super_amount = db.Column(db.Numeric())

    # Foreign keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def to_json(self):
        """
        Convert Employee instance to JSON format
        """
        return {
            'firstName': self.user.first_name,
            'lastName': self.user.last_name,
            'payment_period_start': self.payment_period_start,
            'payment_period_end': self.payment_period_end,
            'gross_income': self.gross_income,
            'income_tax': self.income_tax,
            'net_income': self.net_income,
            'super_amount': self.super_amount
        }

    def to_csv(self):
        """
        Convert Employee instance to CSV format
        """
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
