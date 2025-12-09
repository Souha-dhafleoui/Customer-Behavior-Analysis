import sqlite3
import pandas as pd

# File paths to the CSV files
fact_table_file = 'C:/Users/mariem ben slama/BIproject/data/final data/fact_table.csv'
customer_dim_file = 'C:/Users/mariem ben slama/BIproject/data/final data/customer_dim.csv'
product_dim_file = 'C:/Users/mariem ben slama/BIproject/data/final data/product_dim.csv'
date_dim_file = 'C:/Users/mariem ben slama/BIproject/data/final data/date_dim.csv'

#Create customer_behavior Database
customer_behavior= 'C:/Users/mariem ben slama/BIproject/data/final data/customer_behavior.db'
connection = sqlite3.connect(customer_behavior)
cursor = connection.cursor()

# Define the schemas with foreign key constraints
# Create the customer dimension table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customer_dim (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL,
    subscription_status TEXT NOT NULL,
    generation TEXT NOT NULL,
    previous_purchases INTEGER NOT NULL,
    frequency_of_purchases TEXT NOT NULL
);
''')

# Create the product dimension table
cursor.execute('''
CREATE TABLE IF NOT EXISTS product_dim (
    product_id INTEGER PRIMARY KEY,
    item_purchased TEXT NOT NULL,
    category TEXT NOT NULL,
    size TEXT NOT NULL,
    color TEXT NOT NULL
);
''')

# Create the date dimension table
cursor.execute('''
CREATE TABLE IF NOT EXISTS date_dim (
    date_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    season TEXT NOT NULL
);
''')

# Create the fact table with composite primary key and foreign key constraints
cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_table (
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    purchase_amount_usd INTEGER NOT NULL,
    discount_applied TEXT NOT NULL,
    review_rating REAL NOT NULL,
    PRIMARY KEY (customer_id, product_id, date_id), -- Composite Primary Key
    FOREIGN KEY (customer_id) REFERENCES customer_dim (customer_id),
    FOREIGN KEY (product_id) REFERENCES product_dim (product_id),
    FOREIGN KEY (date_id) REFERENCES date_dim (date_id)
);
''')
# Load data from CSV files into the tables
# Load the fact table
fact_table = pd.read_csv(fact_table_file)
fact_table.to_sql('fact_table', connection, if_exists='append', index=False)

# Load the customer dimension table
customer_dim = pd.read_csv(customer_dim_file)
customer_dim.to_sql('customer_dim', connection, if_exists='append', index=False)

# Load the product dimension table
product_dim = pd.read_csv(product_dim_file)
product_dim.to_sql('product_dim', connection, if_exists='append', index=False)

# Load the date dimension table
date_dim = pd.read_csv(date_dim_file)
date_dim.to_sql('date_dim', connection, if_exists='append', index=False)

#Verify the data was loaded (optional)
for table_name in ['fact_table', 'customer_dim', 'product_dim', 'date_dim']:
    print(f"Data from {table_name}:")
    result = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", connection)
    print(result)

# Commit the changes and close the connection
connection.commit()
connection.close()

print(f"Database {customer_behavior} created and tables loaded successfully!")