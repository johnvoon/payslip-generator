import csv

import requests
from flask import request, make_response
from flask_restful import Resource, reqparse
from models.payslip import Payslip
from utils import *


class Payslip(Resource):
    def post(self):
        """
        Get and parse CSV file uploaded by user and
        generate downloadable CSV file containing payslip data.
        """
        uploaded_file = request.files.get('file', None)
        if uploaded_file:
            if uploaded_file.filename.endswith('.csv'):
                try:
                    # Parse uploaded file and generate CSV output
                    employee_data = parse_csv_from_file(uploaded_file)
                    payslip_data = generate_payslip_data(employee_data)
                    generated_csv_file = generate_csv_output(payslip_data)

                    # generate response with correct headers
                    response = make_response(generated_csv_file.getvalue())
                    response.headers['Content-Disposition'] = 'attachment; filename=payslip.csv'
                    response.headers['Content-Type'] = 'text/csv'

                    return response

                except requests.exceptions.RequestException as err:
                    return {'message': 'Error: {}'.format(err)}, 500

            return {'message': 'The file you uploaded is not a .csv file. Please upload a .csv file'}, 400

        return {'message': 'No file was detected. Please upload a .csv file'}, 400
