import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_sales_data():
    """Create sample sales data for testing"""
    
    # Generate sample data
    np.random.seed(42)
    n_records = 1000
    
    # Regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Products
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones']
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 365)) for _ in range(n_records)]
    
    # Create DataFrame
    data = {
        'order_id': range(1, n_records + 1),
        'date': dates,
        'region': np.random.choice(regions, n_records),
        'product': np.random.choice(products, n_records),
        'quantity': np.random.randint(1, 10, n_records),
        'unit_price': np.random.uniform(50, 2000, n_records).round(2),
        'customer_id': np.random.randint(1000, 9999, n_records),
        'salesperson': [f'Salesperson_{i}' for i in np.random.randint(1, 21, n_records)]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate total amount
    df['total_amount'] = (df['quantity'] * df['unit_price']).round(2)
    
    return df

def create_sample_employee_data():
    """Create sample employee data for testing"""
    
    np.random.seed(42)
    n_records = 500
    
    # Departments
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    
    # Positions
    positions = ['Manager', 'Senior', 'Junior', 'Lead', 'Associate']
    
    # Generate dates
    start_date = datetime(2015, 1, 1)
    hire_dates = [start_date + timedelta(days=random.randint(0, 365*8)) for _ in range(n_records)]
    
    # Create DataFrame
    data = {
        'employee_id': range(1, n_records + 1),
        'first_name': [f'First_{i}' for i in range(n_records)],
        'last_name': [f'Last_{i}' for i in range(n_records)],
        'email': [f'employee_{i}@company.com' for i in range(n_records)],
        'department': np.random.choice(departments, n_records),
        'position': np.random.choice(positions, n_records),
        'salary': np.random.uniform(30000, 150000, n_records).round(2),
        'hire_date': hire_dates,
        'age': np.random.randint(22, 65, n_records),
        'experience_years': np.random.randint(0, 20, n_records)
    }
    
    df = pd.DataFrame(data)
    
    return df

def create_sample_customer_data():
    """Create sample customer data for testing"""
    
    np.random.seed(42)
    n_records = 300
    
    # Cities
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego']
    
    # Customer types
    customer_types = ['Individual', 'Business', 'Enterprise']
    
    # Create DataFrame
    data = {
        'customer_id': range(1, n_records + 1),
        'customer_name': [f'Customer_{i}' for i in range(n_records)],
        'email': [f'customer_{i}@email.com' for i in range(n_records)],
        'phone': [f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}' for _ in range(n_records)],
        'city': np.random.choice(cities, n_records),
        'customer_type': np.random.choice(customer_types, n_records),
        'total_orders': np.random.randint(1, 50, n_records),
        'total_spent': np.random.uniform(100, 10000, n_records).round(2),
        'registration_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365*3)) for _ in range(n_records)]
    }
    
    df = pd.DataFrame(data)
    
    return df

if __name__ == "__main__":
    # Create sample datasets
    print("Creating sample datasets...")
    
    # Sales data
    sales_df = create_sample_sales_data()
    sales_df.to_excel('sample_sales_data.xlsx', index=False)
    print("✅ Created sample_sales_data.xlsx")
    
    # Employee data
    employee_df = create_sample_employee_data()
    employee_df.to_excel('sample_employee_data.xlsx', index=False)
    print("✅ Created sample_employee_data.xlsx")
    
    # Customer data
    customer_df = create_sample_customer_data()
    customer_df.to_excel('sample_customer_data.xlsx', index=False)
    print("✅ Created sample_customer_data.xlsx")
    
    print("\nSample data files created successfully!")
    print("You can now use these files to test the SQL Agent application.") 