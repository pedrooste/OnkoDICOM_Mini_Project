"""Example demonstrating sqlite setup and use"""
import sqlite3
from customer import Customer

# connection and cursor setup
conn = sqlite3.connect('customer.db')
c = conn.cursor()


# table setup
# c.execute("CREATE TABLE customer (first text,last text,pay integer)")


def insert_customer(cust):
    """Inserts customer based on object"""
    with conn:
        c.execute("INSERT INTO customer VALUES (:first, :last, :pay)",
                  {'first': cust.first, 'last': cust.last, 'pay': cust.pay})


def get_customer_by_fname(fname):
    """Gets customer by their first name"""
    c.execute("SELECT * FROM customer WHERE first = :first", {'first': fname})
    print(c.fetchall())


# Clearing table
with conn:
    c.execute("DELETE * FROM customer")

# Python Customers

insert_customer(Customer('Pedro', 'Oste', 420))
insert_customer(Customer('Sades', 'Oste', 512))
insert_customer(Customer('Caitlyn', 'Oste', 411))
insert_customer(Customer('Jake', 'Oste', 78))

get_customer_by_fname('Caitlyn')

# We no longer need to commit as we use the with conn
# conn.commit()

# Closing the connection
conn.close()
