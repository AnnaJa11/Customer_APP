from flask import Flask, render_template, request, redirect, url_for
from database_setup import add_customer, Customer, Session
from app import CustomerServiceApp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Homepage view
@app.route('/')
def index():
    return render_template('index.html', title='Customer Service App', navigation=[...], year=2024)

# Report view
@app.route('/report')
def show_report():
    # Retrieving customer data from the database
    report_data = get_report_data()
    print(report_data)  # Add this
    return render_template('report.html', report_data=report_data)

# Function to generate report data
def generate_report_data():
    # Create an instance of the customer service application
    app = CustomerServiceApp("database.db")
    # Generate the report and return it
    return app.generate_report()

# View for adding a new customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_new_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        interested = request.form['interested']
        callback_date = request.form['callback_date']
        comments = request.form['comments']

        customer_info = {
            'name': name,
            'phone': phone,
            'email': email,
            'interested': interested,
            'callback_date': callback_date,
            'comments': comments
        }

        # Add the customer to the database
        add_customer(**customer_info)

        # After adding the customer, redirect the user to the report page
        return redirect(url_for('show_report'))
    else:
        # If the access is via the GET method, simply display the form
        return render_template('add_customer.html')

# Function to retrieve customer data from the database
def get_report_data():
    session = Session()
    customers = session.query(Customer).all()
    session.close()
    return customers

if __name__ == '__main__':
    app.run(debug=True)