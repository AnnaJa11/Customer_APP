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
    # Retrieving customer data from the base
    report_data = get_report_data()
    print(report_data)  # Dodaj to
    return render_template('report.html', report_data=report_data)

# Funkcja do generowania danych raportu
def generate_report_data():
    # Tworzymy instancję aplikacji obsługi klienta
    app = CustomerServiceApp("database.db")
    # Generujemy raport i zwracamy go
    return app.generate_report()

# Widok do dodawania nowego klienta
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

        # Dodanie klienta do bazy danych
        add_customer(**customer_info)

        # Po dodaniu klienta przekieruj użytkownika do strony raportu
        return redirect(url_for('show_report'))
    else:
        # Jeśli dostęp jest za pomocą metody GET, po prostu wyświetl formularz
        return render_template('add_customer.html')

# Funkcja do pobierania danych klienta z bazy danych
def get_report_data():
    session = Session()
    customers = session.query(Customer).all()
    session.close()
    return customers

if __name__ == '__main__':
    app.run(debug=True)