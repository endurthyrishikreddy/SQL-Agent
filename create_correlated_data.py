#!/usr/bin/env python3
"""
Create correlated sample data for testing multi-table queries
"""

import csv
import random
from datetime import datetime, timedelta

def create_correlated_data():
    """Create sample data with relationships between tables"""
    print("Creating correlated sample data...")
    
    # Set seed for reproducibility
    random.seed(42)
    
    # Generate 50 customers
    customers = []
    for i in range(1, 51):
        customer = {
            'customer_id': i,
            'customer_name': f'Customer_{i}',
            'email': f'customer_{i}@email.com',
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'customer_type': random.choice(['Individual', 'Business', 'Enterprise']),
            'registration_date': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365*3))).strftime('%Y-%m-%d')
        }
        customers.append(customer)
    
    # Generate 30 employees
    employees = []
    for i in range(1, 31):
        employee = {
            'employee_id': i,
            'first_name': f'Employee_{i}',
            'last_name': f'Smith_{i}',
            'email': f'employee_{i}@company.com',
            'department': random.choice(['Sales', 'Engineering', 'Marketing', 'HR', 'Finance']),
            'salary': round(random.uniform(30000, 150000), 2),
            'hire_date': (datetime(2015, 1, 1) + timedelta(days=random.randint(0, 365*8))).strftime('%Y-%m-%d')
        }
        employees.append(employee)
    
    # Generate 200 sales records with relationships
    sales = []
    for i in range(1, 201):
        # Randomly select customer and employee
        customer = random.choice(customers)
        employee = random.choice(employees)
        
        sale = {
            'sale_id': i,
            'customer_id': customer['customer_id'],
            'employee_id': employee['employee_id'],
            'product': random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard']),
            'quantity': random.randint(1, 5),
            'unit_price': round(random.uniform(100, 2000), 2),
            'sale_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'region': random.choice(['North', 'South', 'East', 'West'])
        }
        sale['total_amount'] = round(sale['quantity'] * sale['unit_price'], 2)
        sales.append(sale)
    
    # Generate 100 orders with customer relationships
    orders = []
    for i in range(1, 101):
        customer = random.choice(customers)
        order = {
            'order_id': i,
            'customer_id': customer['customer_id'],
            'order_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'status': random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled']),
            'total_amount': round(random.uniform(50, 5000), 2),
            'shipping_city': customer['city']
        }
        orders.append(order)
    
    # Write to CSV files
    with open('customers.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    
    with open('employees.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(employees)
    
    with open('sales.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sales[0].keys())
        writer.writeheader()
        writer.writerows(sales)
    
    with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    
    print("✅ Created correlated data files:")
    print("   - customers.csv (50 customers)")
    print("   - employees.csv (30 employees)")
    print("   - sales.csv (200 sales with customer_id and employee_id)")
    print("   - orders.csv (100 orders with customer_id)")
    
    print("\n🔗 Relationships:")
    print("   - sales.customer_id → customers.customer_id")
    print("   - sales.employee_id → employees.employee_id")
    print("   - orders.customer_id → customers.customer_id")
    
    print("\n💡 Example correlated questions you can ask:")
    print("   - 'Show me sales with customer and employee names'")
    print("   - 'Find customers who have both sales and orders'")
    print("   - 'Compare sales performance by employee department'")
    print("   - 'Show me total revenue by customer city'")
    print("   - 'Find employees who made sales to enterprise customers'")

if __name__ == "__main__":
    create_correlated_data() 