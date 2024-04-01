import sqlite3
from datetime import datetime, timedelta

class Customer:
    def __init__(self, name, phone, email, callback_date, comments, interested=None):
        self.id = None  # Dodajemy atrybut id
        self.name = name
        self.phone = phone
        self.email = email
        self.interested = interested
        self.interactions = []
        self.callback_date = callback_date
        self.comments = comments

    def add_interaction(self, interaction):
        self.interactions.append(interaction)

    def set_callback_date(self, callback_date):
        self.callback_date = callback_date
        print(f"Callback scheduled with {self.name} on {callback_date}")

    def send_notification(self, message):
        print(f"Notification sent to {self.name}: {message}")

class Interaction:
    def __init__(self, date, notes):
        self.date = date
        self.notes = notes

class CustomerServiceApp:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    phone TEXT,
                                    email TEXT,
                                    interested TEXT,
                                    callback_date TEXT
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS interactions (
                                    id INTEGER PRIMARY KEY,
                                    customer_id INTEGER,
                                    date TEXT,
                                    notes TEXT,
                                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                                )''')
        self.connection.commit()

    def add_customer(self, customer):
        self.cursor.execute('''INSERT INTO customers (name, phone, email, interested, callback_date)
                               VALUES (?, ?, ?, ?, ?)''',
                               (customer.name, customer.phone, customer.email, customer.interested, customer.callback_date))
        self.connection.commit()
        
        # Retrieve the id of the most recently added customer
        customer_id = self.cursor.lastrowid
        
        # Assign the customer ID to the Customer object
        customer.id = customer_id
        
        return customer_id

    def record_interaction(self, customer_id, date, notes):  # Changing the parameter to customer_id
        self.cursor.execute('''INSERT INTO interactions (customer_id, date, notes)
                               VALUES (?, ?, ?)''',
                               (customer_id, date, notes))
        self.connection.commit()

    def update_interest(self, customer_id, interested):  # Changing the parameter to customer_id
        self.cursor.execute('''UPDATE customers SET interested = ? WHERE id = ?''',
                               (interested, customer_id))
        self.connection.commit()

    def schedule_callback(self, customer_id, callback_date):  # Changing the parameter to customer_id
        self.cursor.execute('''UPDATE customers SET callback_date = ? WHERE id = ?''',
                               (callback_date, customer_id))
        self.connection.commit()

    def send_reminder(self, customer):
        if customer.callback_date:
            now = datetime.now()
            if customer.callback_date <= now:
                message = "Reminder: Callback scheduled today!"
                customer.send_notification(message)

    def generate_report(self):
        self.cursor.execute('''SELECT * FROM customers''')
        customers = self.cursor.fetchall()
        print("----- Customer Service Report -----")
        for customer in customers:
            print(f"Customer: {customer[1]}")
            print(f"Phone: {customer[2]}")
            print(f"Email: {customer[3]}")
            print(f"Interest: {customer[4]}")
            if customer[5]:
                print(f"Callback scheduled for: {customer[5]}")

            self.cursor.execute('''SELECT * FROM interactions WHERE customer_id = ?''', (customer[0],))
            interactions = self.cursor.fetchall()
            print("Interactions:")
            for interaction in interactions:
                print(f"- Date: {interaction[2]}, Notes: {interaction[3]}")
        print("----------------------------------")

# Create an instance of the customer management application
app = CustomerServiceApp("database.db")


# Generate report
app.generate_report()




# # Add customers
# customer1 = Customer("John Doe", "123-456-789", "john@example.com", "12-12-2024", "something bla bla")
# customer2 = Customer("Jane Smith", "987-654-321", "jane@example.com", "12-12-2024", "something bla bla")

# # Add customers to the database and save their IDs
# customer1_id = app.add_customer(customer1)
# customer2_id = app.add_customer(customer2)

# # We log interactions with customers using their IDs
# app.record_interaction(customer1_id, "2024-03-12", "Klient zainteresowany usługami transportowymi")
# app.record_interaction(customer2_id, "2024-03-13", "Klient niezainteresowany usługami transportowymi")

# # Marking customer interests
# app.update_interest(customer1_id, "Tak")
# app.update_interest(customer2_id, "Nie")

# # Scheduling follow-up calls with customers
# callback_date1 = datetime(2024, 3, 15, 10, 0)  # Example date and time
# callback_date2 = datetime(2024, 3, 16, 11, 30)  # Example date and time
# app.schedule_callback(customer1_id, callback_date1)
# app.schedule_callback(customer2_id, callback_date2)

# # Send notifications/reminders
# app.send_reminder(customer1)
# app.send_reminder(customer2)