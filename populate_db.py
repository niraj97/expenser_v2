#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://localhost:5000"

def print_response(response, message):
    """Print formatted response"""
    print(f"\n{message}")
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))

class DatabasePopulator:
    def __init__(self):
        self.tokens = {}  # Store tokens for each user
        self.user_ids = {}  # Store user IDs
        self.category_ids = {}  # Store category IDs
        self.group_ids = {}  # Store group IDs

    def register_user(self, username, email, password):
        """Register a new user"""
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
        print_response(response, f"Registering user: {username}")
        if response.status_code == 201:
            data = response.json()
            self.tokens[email] = data["token"]
            self.user_ids[email] = data["user_id"]
        return response.status_code == 201

    def create_category(self, name, description, user_email):
        """Create an expense category"""
        response = requests.post(
            f"{BASE_URL}/expenses/categories",
            headers={"Authorization": f"Bearer {self.tokens[user_email]}"},
            json={
                "name": name,
                "description": description
            }
        )
        print_response(response, f"Creating category: {name}")
        if response.status_code == 201:
            data = response.json()
            self.category_ids[name] = data["category"]["id"]
        return response.status_code == 201

    def create_group(self, name, description, creator_email, member_emails):
        """Create a group"""
        response = requests.post(
            f"{BASE_URL}/groups/create",
            headers={"Authorization": f"Bearer {self.tokens[creator_email]}"},
            json={
                "name": name,
                "description": description,
                "members": member_emails
            }
        )
        print_response(response, f"Creating group: {name}")
        if response.status_code == 201:
            data = response.json()
            self.group_ids[name] = data["group_id"]
        return response.status_code == 201

    def add_personal_expense(self, description, amount, category_name, date, user_email):
        """Add a personal expense"""
        response = requests.post(
            f"{BASE_URL}/expenses/personal",
            headers={"Authorization": f"Bearer {self.tokens[user_email]}"},
            json={
                "description": description,
                "amount": amount,
                "category_id": self.category_ids[category_name],
                "date": date.isoformat()
            }
        )
        print_response(response, f"Adding personal expense: {description}")
        return response.status_code == 201

    def add_group_expense(self, group_name, description, amount, paid_by_email, split_users, date):
        """Add a group expense"""
        response = requests.post(
            f"{BASE_URL}/expenses/create",
            headers={"Authorization": f"Bearer {self.tokens[paid_by_email]}"},
            json={
                "group_id": self.group_ids[group_name],
                "description": description,
                "amount": amount,
                "split_type": "equal",
                "splits": [{"user_id": self.user_ids[email]} for email in split_users],
                "date": date.isoformat()
            }
        )
        print_response(response, f"Adding group expense: {description}")
        return response.status_code == 201

def main():
    populator = DatabasePopulator()

    # Register users
    users = [
        ("alice", "alice@example.com", "password123"),
        ("bob", "bob@example.com", "password123"),
        ("charlie", "charlie@example.com", "password123")
    ]
    
    print("\n=== Registering Users ===")
    for username, email, password in users:
        populator.register_user(username, email, password)
        time.sleep(1)  # Add small delay between requests

    # Create categories
    categories = [
        ("Groceries", "Food and household items"),
        ("Entertainment", "Movies, games, and fun activities"),
        ("Utilities", "Electricity, water, and internet bills"),
        ("Rent", "Monthly rent and housing expenses"),
        ("Transportation", "Public transport and fuel expenses")
    ]
    
    print("\n=== Creating Categories ===")
    for name, description in categories:
        populator.create_category(name, description, "alice@example.com")
        time.sleep(1)

    # Create groups
    groups = [
        ("Roommates", "Shared apartment expenses", "alice@example.com", 
         ["bob@example.com", "charlie@example.com"]),
        ("Trip Group", "Weekend trip expenses", "bob@example.com", 
         ["alice@example.com", "charlie@example.com"])
    ]
    
    print("\n=== Creating Groups ===")
    for name, description, creator, members in groups:
        populator.create_group(name, description, creator, members)
        time.sleep(1)

    # Add personal expenses for Alice
    personal_expenses = [
        ("Weekly groceries", 75.50, "Groceries", datetime.now() - timedelta(days=5)),
        ("Movie night", 25.00, "Entertainment", datetime.now() - timedelta(days=3)),
        ("Internet bill", 89.99, "Utilities", datetime.now() - timedelta(days=2)),
        ("Bus pass", 45.00, "Transportation", datetime.now() - timedelta(days=1))
    ]
    
    print("\n=== Adding Personal Expenses ===")
    for description, amount, category, date in personal_expenses:
        populator.add_personal_expense(description, amount, category, date, "alice@example.com")
        time.sleep(1)

    # Add group expenses
    group_expenses = [
        ("Roommates", "Monthly rent", 1500.00, "alice@example.com", 
         ["alice@example.com", "bob@example.com", "charlie@example.com"], 
         datetime.now() - timedelta(days=4)),
        ("Roommates", "Electricity bill", 120.00, "bob@example.com",
         ["alice@example.com", "bob@example.com", "charlie@example.com"],
         datetime.now() - timedelta(days=3)),
        ("Trip Group", "Hotel booking", 450.00, "charlie@example.com",
         ["alice@example.com", "bob@example.com", "charlie@example.com"],
         datetime.now() - timedelta(days=2))
    ]
    
    print("\n=== Adding Group Expenses ===")
    for group, description, amount, paid_by, split_users, date in group_expenses:
        populator.add_group_expense(group, description, amount, paid_by, split_users, date)
        time.sleep(1)

    print("\nDatabase population completed!")

if __name__ == "__main__":
    main()
