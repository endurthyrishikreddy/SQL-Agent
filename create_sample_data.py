#!/usr/bin/env python3
"""
Simple sample data generator for SQL Agent testing
Creates Excel files without complex dependencies
"""

import csv
import random
from datetime import datetime, timedelta

def create_sales_data():
    """Create sample sales data"""
    print("Creating sales data...")
    
    # Sample data
    regions = ['North', 'South', 'East', 'West', 'Central']
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones']
    
    # Generate 100 records
    data = []
    for i in range(1, 101):
        order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(50, 2000), 2)
        total_amount = round(quantity * unit_price, 2)
        
        record = {
            'order_id': i,
            'date': order_date.strftime('%Y-%m-%d'),
            'region': random.choice(regions),
            'product': random.choice(products),
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'customer_id': random.randint(1000, 9999),
            'salesperson': f'Salesperson_{random.randint(1, 20)}'
        }
        data.append(record)
    
    # Write to CSV (Excel can open CSV files)
    with open('sample_sales_data.csv', 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print("✅ Created sample_sales_data.csv")

def create_employee_data():
    """Create sample employee data"""
    print("Creating employee data...")
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    positions = ['Manager', 'Senior', 'Junior', 'Lead', 'Associate']
    
    data = []
    for i in range(1, 51):  # 50 employees
        hire_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 365*8))
        salary = round(random.uniform(30000, 150000), 2)
        
        record = {
            'employee_id': i,
            'first_name': f'First_{i}',
            'last_name': f'Last_{i}',
            'email': f'employee_{i}@company.com',
            'department': random.choice(departments),
            'position': random.choice(positions),
            'salary': salary,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'age': random.randint(22, 65),
            'experience_years': random.randint(0, 20)
        }
        data.append(record)
    
    with open('sample_employee_data.csv', 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print("✅ Created sample_employee_data.csv")

def create_customer_data():
    """Create sample customer data"""
    print("Creating customer data...")
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
    customer_types = ['Individual', 'Business', 'Enterprise']
    
    data = []
    for i in range(1, 31):  # 30 customers
        reg_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365*3))
        total_spent = round(random.uniform(100, 10000), 2)
        
        record = {
            'customer_id': i,
            'customer_name': f'Customer_{i}',
            'email': f'customer_{i}@email.com',
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'city': random.choice(cities),
            'customer_type': random.choice(customer_types),
            'total_orders': random.randint(1, 50),
            'total_spent': total_spent,
            'registration_date': reg_date.strftime('%Y-%m-%d')
        }
        data.append(record)
    
    with open('sample_customer_data.csv', 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print("✅ Created sample_customer_data.csv")

def main():
    """Main function to create all sample data"""
    print("🤖 SQL Agent - Sample Data Generator")
    print("=" * 40)
    
    try:
        create_sales_data()
        create_employee_data()
        create_customer_data()
        
        print("\n🎉 All sample data files created successfully!")
        print("\n📁 Generated files:")
        print("   - sample_sales_data.csv")
        print("   - sample_employee_data.csv") 
        print("   - sample_customer_data.csv")
        print("\n💡 You can now upload these CSV files to the SQL Agent application.")
        print("   Note: CSV files can be opened in Excel and saved as .xlsx if needed.")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == "__main__":
    main() 