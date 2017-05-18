# Payslip Generator
A payslip generator that takes a .csv file as input and outputs a downloadable .csv file. 

# Instructions
- Go to [link]
- Upload a .csv file and click "Generate Payslip Data"
- Download the .csv file

## Assumptions
- CSV input will be in the form: first name (string), last name (string), annual salary (positive integer), super rate (%), payment start and end date (year not specified) (string, e.g. 01 March - 31 March).
- The period between the payment start and end date (both dates inclusive) inputted by the user will be exactly one month.
- Payslip will be generated on a monthly basis only for this program, not fortnightly, pro rata, etc.
- Employee first names and last names are unique, i.e. there are no two employees with the same first and last names.
- Data is not stored to server

## Tech
- Flask web framework
- Flask-RESTful API
- React, Redux front-end
- Heroku (free tier) for hosting the API
- Surge for hosting static assets.

# Todo (in addition to problem specifications)
- Allow saving of employee and payslip data to database
- Allow payslip data to be retrieved in JSON format
- Generate payslip in PDF format

