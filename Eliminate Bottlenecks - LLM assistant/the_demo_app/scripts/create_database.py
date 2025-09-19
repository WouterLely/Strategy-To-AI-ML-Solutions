#!/usr/bin/env python3
"""
Create a sample SQLite database with sales and HR data (Northwind-inspired)
"""
import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_database():
    # Ensure data/database directory exists
    os.makedirs("data/database", exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect("data/database/company.db")
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Populate with sample data
    populate_employees(cursor)
    populate_departments(cursor)
    populate_customers(cursor)
    populate_products(cursor)
    populate_orders(cursor)
    populate_order_details(cursor)
    
    # Commit and close
    conn.commit()
    conn.close()
    print("Database created successfully at data/database/company.db")

def create_tables(cursor):
    """Create all necessary tables"""
    
    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            title TEXT,
            department_id INTEGER,
            hire_date DATE,
            salary DECIMAL(10,2),
            email TEXT,
            phone TEXT,
            manager_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(department_id),
            FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
        )
    """)
    
    # Departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL,
            location TEXT,
            budget DECIMAL(12,2)
        )
    """)
    
    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            contact_name TEXT,
            contact_title TEXT,
            address TEXT,
            city TEXT,
            country TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price DECIMAL(8,2),
            units_in_stock INTEGER,
            discontinued BOOLEAN DEFAULT 0
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            employee_id INTEGER,
            order_date DATE,
            required_date DATE,
            shipped_date DATE,
            ship_city TEXT,
            ship_country TEXT,
            freight DECIMAL(8,2),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    """)
    
    # Order Details table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INTEGER,
            product_id INTEGER,
            unit_price DECIMAL(8,2),
            quantity INTEGER,
            discount DECIMAL(4,2) DEFAULT 0,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

def populate_departments(cursor):
    """Populate departments table"""
    departments = [
        (1, "Infrastructure Services", "New York", 2500000),
        (2, "Cloud & Application Services", "Austin", 3200000),
        (3, "Consulting Services", "Chicago", 1800000),
        (4, "Security & Resiliency", "Atlanta", 2100000),
        (5, "Network Services", "Dallas", 1900000),
        (6, "Digital Workplace Services", "Phoenix", 1600000),
        (7, "Data & AI Services", "Denver", 2800000),
        (8, "Human Resources", "New York", 800000),
        (9, "Finance & Operations", "Charlotte", 1200000)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO departments 
        (department_id, department_name, location, budget)
        VALUES (?, ?, ?, ?)
    """, departments)

def populate_employees(cursor):
    """Populate employees table"""
    employees = [
        (1, "Alexandra", "Chen", "VP Infrastructure Services", 1, "2019-03-15", 165000, "alexandra.chen@company.com", "555-0101", None),
        (2, "Marcus", "Thompson", "Infrastructure Architect", 1, "2020-06-20", 135000, "marcus.thompson@company.com", "555-0102", 1),
        (3, "Priya", "Patel", "Cloud Solutions Consultant", 2, "2021-01-10", 125000, "priya.patel@company.com", "555-0201", None),
        (4, "David", "Kim", "Application Modernization Lead", 2, "2020-09-15", 140000, "david.kim@company.com", "555-0202", 3),
        (5, "Sarah", "Williams", "IT Strategy Consultant", 3, "2018-11-01", 150000, "sarah.williams@company.com", "555-0301", None),
        (6, "James", "Rodriguez", "Digital Transformation Consultant", 3, "2021-04-14", 130000, "james.rodriguez@company.com", "555-0302", 5),
        (7, "Elena", "Kowalski", "Cybersecurity Specialist", 4, "2020-02-20", 145000, "elena.kowalski@company.com", "555-0401", None),
        (8, "Michael", "Johnson", "Security Architect", 4, "2021-07-30", 155000, "michael.johnson@company.com", "555-0402", 7),
        (9, "Aisha", "Hassan", "Network Engineer", 5, "2022-01-10", 110000, "aisha.hassan@company.com", "555-0501", None),
        (10, "Carlos", "Martinez", "Senior Network Consultant", 5, "2019-08-15", 125000, "carlos.martinez@company.com", "555-0502", 9),
        (11, "Rachel", "Turner", "Digital Workplace Consultant", 6, "2021-03-25", 115000, "rachel.turner@company.com", "555-0601", None),
        (12, "Thomas", "Anderson", "Data Scientist", 7, "2020-10-12", 135000, "thomas.anderson@company.com", "555-0701", None),
        (13, "Lisa", "Brown", "AI Solutions Architect", 7, "2021-05-18", 160000, "lisa.brown@company.com", "555-0702", 12),
        (14, "Jennifer", "Davis", "HR Director", 8, "2018-01-20", 120000, "jennifer.davis@company.com", "555-0801", None),
        (15, "Robert", "Wilson", "Finance Manager", 9, "2019-09-30", 105000, "robert.wilson@company.com", "555-0901", None)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO employees 
        (employee_id, first_name, last_name, title, department_id, hire_date, salary, email, phone, manager_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees)

def populate_customers(cursor):
    """Populate customers table"""
    customers = [
        (1, "Global Financial Services Corp", "Amanda Rodriguez", "CIO", "200 Liberty St", "New York", "USA", "212-555-0001", "amanda.rodriguez@gfs.com"),
        (2, "MegaHealth Systems", "Dr. Kevin Park", "Chief Technology Officer", "1500 Medical Center Dr", "Houston", "USA", "713-555-0002", "kevin.park@megahealth.com"),
        (3, "RetailMax International", "Sarah Chen", "VP of IT Operations", "3000 Commerce Blvd", "Atlanta", "USA", "404-555-0003", "sarah.chen@retailmax.com"),
        (4, "ManufacturingPro Industries", "James Mueller", "Head of Digital Transformation", "850 Industrial Way", "Detroit", "USA", "313-555-0004", "james.mueller@mfgpro.com"),
        (5, "TeleConnect Networks", "Maria Gonzalez", "Infrastructure Director", "450 Communications Ave", "Dallas", "USA", "214-555-0005", "maria.gonzalez@teleconnect.com"),
        (6, "EnergyFlow Corporation", "Robert Kim", "IT Strategy Manager", "1200 Energy Plaza", "Houston", "USA", "281-555-0006", "robert.kim@energyflow.com"),
        (7, "SecureBank Holdings", "Lisa Thompson", "Chief Information Security Officer", "100 Financial District", "Charlotte", "USA", "704-555-0007", "lisa.thompson@securebank.com"),
        (8, "CloudTech Innovations", "Michael Zhang", "VP Cloud Architecture", "500 Innovation Dr", "Seattle", "USA", "206-555-0008", "michael.zhang@cloudtech.com"),
        (9, "Government Services Agency", "Jennifer Adams", "IT Modernization Lead", "300 Federal Building", "Washington", "USA", "202-555-0009", "jennifer.adams@gsa.gov"),
        (10, "LogisticsPro Global", "Carlos Rivera", "Digital Operations Director", "750 Supply Chain Way", "Memphis", "USA", "901-555-0010", "carlos.rivera@logisticspro.com")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO customers 
        (customer_id, company_name, contact_name, contact_title, address, city, country, phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers)

def populate_products(cursor):
    """Populate products table"""
    products = [
        (1, "Infrastructure Modernization", "Infrastructure Services", 250000.00, 50, 0),
        (2, "Cloud Migration & Optimization", "Cloud Services", 180000.00, 75, 0),
        (3, "Application Modernization", "Application Services", 320000.00, 40, 0),
        (4, "Cybersecurity Assessment & Implementation", "Security Services", 150000.00, 60, 0),
        (5, "Digital Workplace Transformation", "Workplace Services", 120000.00, 80, 0),
        (6, "Data Analytics & AI Implementation", "Data & AI Services", 280000.00, 35, 0),
        (7, "Network Infrastructure Upgrade", "Network Services", 200000.00, 45, 0),
        (8, "IT Strategy & Consulting", "Consulting Services", 95000.00, 100, 0),
        (9, "Managed IT Operations", "Managed Services", 75000.00, 120, 0),
        (10, "Disaster Recovery & Business Continuity", "Resiliency Services", 160000.00, 55, 0),
        (11, "DevOps & Automation Implementation", "Application Services", 140000.00, 65, 0),
        (12, "Multi-Cloud Management", "Cloud Services", 110000.00, 70, 0),
        (13, "Zero Trust Security Architecture", "Security Services", 190000.00, 30, 0),
        (14, "Edge Computing Solutions", "Infrastructure Services", 220000.00, 25, 0),
        (15, "Mainframe Modernization", "Infrastructure Services", 350000.00, 20, 0)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO products 
        (product_id, product_name, category, unit_price, units_in_stock, discontinued)
        VALUES (?, ?, ?, ?, ?, ?)
    """, products)

def populate_orders(cursor):
    """Populate orders table with random data"""
    base_date = datetime(2023, 1, 1)
    orders = []
    
    for order_id in range(1, 51):  # 50 orders
        customer_id = random.randint(1, 10)
        employee_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8])  # Service delivery team members
        
        order_date = base_date + timedelta(days=random.randint(0, 365))
        required_date = order_date + timedelta(days=random.randint(7, 30))
        shipped_date = order_date + timedelta(days=random.randint(1, 14)) if random.random() > 0.1 else None
        
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        countries = ["USA", "Canada", "Mexico"]
        
        orders.append((
            order_id,
            customer_id,
            employee_id,
            order_date.strftime("%Y-%m-%d"),
            required_date.strftime("%Y-%m-%d"),
            shipped_date.strftime("%Y-%m-%d") if shipped_date else None,
            random.choice(cities),
            random.choice(countries),
            round(random.uniform(50, 500), 2)
        ))
    
    cursor.executemany("""
        INSERT OR REPLACE INTO orders 
        (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_city, ship_country, freight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders)

def populate_order_details(cursor):
    """Populate order details table"""
    order_details = []
    
    for order_id in range(1, 51):
        # Each order has 1-4 products
        num_products = random.randint(1, 4)
        products_in_order = random.sample(range(1, 16), num_products)
        
        for product_id in products_in_order:
            quantity = random.randint(1, 10)
            # Get product price (simplified - in real scenario you'd query the products table)
            base_prices = {
                1: 250000, 2: 180000, 3: 320000, 4: 150000, 5: 120000, 6: 280000, 7: 200000, 8: 95000, 
                9: 75000, 10: 160000, 11: 140000, 12: 110000, 13: 190000, 14: 220000, 15: 350000
            }
            unit_price = base_prices[product_id]
            discount = random.choice([0, 0.05, 0.10, 0.15]) if random.random() > 0.7 else 0
            
            order_details.append((order_id, product_id, unit_price, quantity, discount))
    
    cursor.executemany("""
        INSERT OR REPLACE INTO order_details 
        (order_id, product_id, unit_price, quantity, discount)
        VALUES (?, ?, ?, ?, ?)
    """, order_details)

if __name__ == "__main__":
    create_database()
