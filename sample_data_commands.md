# Sample Data Population Commands for Splitwise Clone

## User Registration and Authentication

### Register First User (testuser)
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Register Second User (friend)
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "friend",
    "email": "friend@example.com",
    "password": "password123"
  }'
```

## Create Expense Categories

### Create Groceries Category
```bash
curl -X POST http://localhost:5000/expenses/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Groceries",
    "description": "Food and household items"
  }'
```

### Create Entertainment Category
```bash
curl -X POST http://localhost:5000/expenses/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Entertainment",
    "description": "Movies, games, and fun activities"
  }'
```

### Create Utilities Category
```bash
curl -X POST http://localhost:5000/expenses/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Utilities",
    "description": "Electricity, water, and internet bills"
  }'
```

## Add Personal Expenses

### Add Personal Grocery Expense
```bash
curl -X POST http://localhost:5000/expenses/personal \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "description": "Weekly groceries",
    "amount": 75.50,
    "category_id": 1,
    "date": "2023-12-01T10:00:00"
  }'
```

### Add Entertainment Expense
```bash
curl -X POST http://localhost:5000/expenses/personal \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "description": "Movie night",
    "amount": 25.00,
    "category_id": 2,
    "date": "2023-12-02T19:00:00"
  }'
```

### Add Utilities Expense
```bash
curl -X POST http://localhost:5000/expenses/personal \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "description": "Internet bill",
    "amount": 89.99,
    "category_id": 3,
    "date": "2023-12-03T09:00:00"
  }'
```

## Create Group and Add Members

### Create Roommates Group
```bash
curl -X POST http://localhost:5000/groups/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Roommates",
    "description": "Shared apartment expenses",
    "members": ["friend@example.com"]
  }'
```

## Add Group Expenses

### Add Electricity Bill
```bash
curl -X POST http://localhost:5000/expenses/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "group_id": 1,
    "description": "Electricity bill",
    "amount": 120.00,
    "split_type": "equal",
    "splits": [
      {"user_id": 1},
      {"user_id": 2}
    ],
    "date": "2023-12-03T10:00:00"
  }'
```

### Add Group Groceries
```bash
curl -X POST http://localhost:5000/expenses/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "group_id": 1,
    "description": "Groceries for apartment",
    "amount": 85.50,
    "split_type": "equal",
    "splits": [
      {"user_id": 1},
      {"user_id": 2}
    ],
    "date": "2023-12-04T15:30:00"
  }'
```

## View Data

### View Personal Expenses
```bash
curl -X GET http://localhost:5000/expenses/personal \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### View Group Expenses
```bash
curl -X GET http://localhost:5000/expenses/group/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### View Expense Summary
```bash
curl -X GET "http://localhost:5000/expenses/personal/summary?start_date=2023-12-01&end_date=2023-12-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Note: Replace `YOUR_JWT_TOKEN` with the actual JWT token received after login. The token is provided in the response when you register or login.
