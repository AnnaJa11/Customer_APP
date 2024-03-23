from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creating a database engine
engine = create_engine('sqlite:///database.db', echo=True)

Base = declarative_base()

# Client's model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)  # Add column phone
    email = Column(String)
    info = Column(Text)

# Creating a table in the database
Base.metadata.create_all(engine)

# Creating a session
Session = sessionmaker(bind=engine)

# A function to add customer data to the database
def add_customer(customer_info):
    session = Session()
    new_customer = Customer(**customer_info)
    session.add(new_customer)
    session.commit()
    session.close()

# A function retrieving customer data from the database
def get_report_data():
    session = Session()
    customers = session.query(Customer).all()
    session.close()
    return customers