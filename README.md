# Splitwise Clone

A Flask-based expense sharing and tracking application with JWT authentication.

## Features

### User Management
- User registration and authentication
- JWT-based secure API access
- Profile management

### Group Expenses
- Create and manage groups
- Add members to groups
- Track shared expenses
- Multiple expense splitting options:
  - Equal split
  - Exact amount split
  - Percentage-based split

### Personal Expense Tracking
- Create custom expense categories
- Track daily personal expenses
- Categorize expenses
- View expenses by date range
- Get expense summaries by category
- Track uncategorized expenses

## API Endpoints

### Authentication
- `POST /auth/register`: Register a new user
- `POST /auth/login`: Login and get JWT token

### Groups
- `POST /groups/create`: Create a new group
- `GET /groups/`: List user's groups
- `POST /groups/<group_id>/add_member`: Add member to group

### Group Expenses
- `POST /expenses/create`: Create a shared expense
- `GET /expenses/group/<group_id>`: Get group expenses

### Personal Expenses
- `POST /expenses/categories`: Create expense category
- `GET /expenses/categories`: List user's expense categories
- `POST /expenses/personal`: Add personal expense
- `GET /expenses/personal`: View personal expenses (with optional filters)
- `GET /expenses/personal/summary`: Get expense summary by category

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask db upgrade
```

4. Run the application:
```bash
python run.py
```

## Database Management

### Initial Setup
```bash
# Initialize migrations directory
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Making Database Changes
1. Update models in your code
2. Generate migration:
```bash
flask db migrate -m "Description of changes"
```
3. Review the generated migration in `migrations/versions/`
4. Apply the migration:
```bash
flask db upgrade
```

### Common Migration Commands
```bash
# View current migration version
flask db current

# View migration history
flask db history

# Rollback one migration
flask db downgrade

# Rollback to specific migration
flask db downgrade <migration_id>

# Create empty migration file
flask db revision -m "description"

# Show pending migrations
flask db show
```

### Database Maintenance
```bash
# Rebuild database from scratch
rm -f instance/splitwise.db
flask db upgrade

# Mark migration as complete without running
flask db stamp <migration_id>

# Generate SQL without executing
flask db upgrade --sql
```

### Best Practices
1. Always review generated migrations before applying
2. Backup database before major migrations
3. Test migrations on development environment first
4. Keep migrations small and focused
5. Use meaningful migration messages
6. Version control your migrations

## Environment Variables
- `SECRET_KEY`: Secret key for JWT encoding
- `DATABASE_URL`: Database connection URL (defaults to SQLite)
- `FLASK_ENV`: Development/Production environment

## API Usage Examples

### 1. Register a User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. Create Expense Category
```bash
curl -X POST http://localhost:5000/expenses/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Groceries",
    "description": "Food and household items"
  }'
```

### 4. Add Personal Expense
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

### 5. View Personal Expenses
```bash
curl -X GET http://localhost:5000/expenses/personal \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Get Expense Summary
```bash
curl -X GET "http://localhost:5000/expenses/personal/summary?start_date=2023-12-01&end_date=2023-12-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Dependencies
- Flask 2.2.5
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.0.4
- PyJWT 2.8.0
- SQLite (default database)
- Other dependencies listed in requirements.txt

## Security Features
- JWT-based authentication
- Password hashing with bcrypt
- Token expiration
- Protected API endpoints
- Input validation

## Database Schema
- Users
- Groups
- GroupMemberships
- Expenses
- ExpenseCategories
- ExpenseSplits

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
