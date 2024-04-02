from flask import Flask, render_template, request, redirect, url_for
from database_setup import add_customer, edit_customer, Customer, Session, get_report_data

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
    return render_template('report.html', report_data=report_data)

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

# View for editing an existing customer
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer_form(customer_id):
    session = Session()
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        interested = request.form['interested']
        callback_date = request.form['callback_date']
        comments = request.form['comments']
        
        edit_customer(customer_id, name, phone, email, interested, callback_date, comments)
        session.close()
        return redirect(url_for('show_report'))  # Redirect to customer report page
    session.close()
    return render_template('edit_customer.html', customer=customer)

if __name__ == '__main__':
    app.run(debug=True)