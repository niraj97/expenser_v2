from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.expense import Expense, ExpenseSplit, SplitType, ExpenseCategory
from ..models.group import Group, GroupMembership
from .. import db
from ..utils.jwt_utils import token_required

expenses = Blueprint('expenses', __name__)

@expenses.route('/create', methods=['POST'])
@token_required
def create_expense(current_user):
    """Create a new expense"""
    data = request.get_json()
    
    # Validate input
    if not data.get('description') or not data.get('amount'):
        return jsonify({"error": "Description and amount are required"}), 400
    
    # Optional group association
    group = None
    if data.get('group_id'):
        group = Group.query.get(data.get('group_id'))
        if not group:
            return jsonify({"error": "Group not found"}), 404
            
        # Check if user is a member of the group
        is_member = GroupMembership.query.filter_by(
            user=current_user,
            group=group
        ).first()
        if not is_member:
            return jsonify({"error": "You are not a member of this group"}), 403
    
    # Create expense
    new_expense = Expense(
        description=data.get('description'),
        amount=data.get('amount'),
        paid_by=current_user,
        group=group
    )
    db.session.add(new_expense)
    
    # Handle expense splits
    split_type = data.get('split_type', 'equal')
    split_details = data.get('splits', [])
    
    if split_type == 'equal':
        # Equal split among all specified users
        total_users = len(split_details)
        split_amount = new_expense.amount / total_users
        
        for user_data in split_details:
            split = ExpenseSplit(
                expense=new_expense,
                user_id=user_data['user_id'],
                split_type=SplitType.EQUAL,
                amount_or_percentage=split_amount
            )
            db.session.add(split)
    
    elif split_type == 'exact':
        # Exact amount split
        for user_data in split_details:
            split = ExpenseSplit(
                expense=new_expense,
                user_id=user_data['user_id'],
                split_type=SplitType.EXACT,
                amount_or_percentage=user_data['amount']
            )
            db.session.add(split)
    
    elif split_type == 'percentage':
        # Percentage-based split
        for user_data in split_details:
            split = ExpenseSplit(
                expense=new_expense,
                user_id=user_data['user_id'],
                split_type=SplitType.PERCENTAGE,
                amount_or_percentage=user_data['percentage']
            )
            db.session.add(split)
    
    db.session.commit()
    
    return jsonify({
        "message": "Expense created successfully",
        "expense_id": new_expense.id
    }), 201

@expenses.route('/group/<int:group_id>', methods=['GET'])
@token_required
def get_group_expenses(current_user, group_id):
    """Retrieve expenses for a specific group"""
    group = Group.query.get_or_404(group_id)
    
    # Check if user is a member of the group
    is_member = GroupMembership.query.filter_by(
        user=current_user,
        group=group
    ).first()
    if not is_member:
        return jsonify({"error": "Not authorized to view group expenses"}), 403
    
    expenses = group.expenses.order_by(Expense.date.desc()).all()
    
    expense_list = []
    for expense in expenses:
        expense_data = {
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "date": expense.date,
            "paid_by": expense.paid_by.username,
            "splits": []
        }
        
        for split in expense.splits:
            expense_data['splits'].append({
                "user": split.user.username,
                "split_type": split.split_type.value,
                "amount": split.amount_or_percentage
            })
        
        expense_list.append(expense_data)
    
    return jsonify(expense_list), 200

@expenses.route('/categories', methods=['POST'])
@token_required
def create_category(current_user):
    """Create a new expense category"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({"error": "Category name is required"}), 400
    
    category = ExpenseCategory(
        name=data.get('name'),
        description=data.get('description', ''),
        user=current_user
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        "message": "Category created successfully",
        "category": {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }
    }), 201

@expenses.route('/categories', methods=['GET'])
@token_required
def get_categories(current_user):
    """Get all expense categories for the current user"""
    categories = current_user.categories.all()
    
    return jsonify([{
        "id": cat.id,
        "name": cat.name,
        "description": cat.description
    } for cat in categories]), 200

@expenses.route('/personal', methods=['POST'])
@token_required
def create_personal_expense(current_user):
    """Create a new personal expense"""
    data = request.get_json()
    
    # Validate input
    if not data.get('description') or not data.get('amount'):
        return jsonify({"error": "Description and amount are required"}), 400
    
    # Validate category if provided
    category = None
    if data.get('category_id'):
        category = ExpenseCategory.query.get(data.get('category_id'))
        if not category or category.user_id != current_user.id:
            return jsonify({"error": "Invalid category"}), 400
    
    # Create expense
    expense = Expense(
        description=data.get('description'),
        amount=data.get('amount'),
        date=datetime.fromisoformat(data.get('date', datetime.utcnow().isoformat())),
        paid_by=current_user,
        category=category
    )
    
    db.session.add(expense)
    
    # Create a single split for the personal expense
    split = ExpenseSplit(
        expense=expense,
        user=current_user,
        split_type=SplitType.EXACT,
        amount_or_percentage=expense.amount
    )
    db.session.add(split)
    
    db.session.commit()
    
    return jsonify({
        "message": "Personal expense created successfully",
        "expense": {
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "date": expense.date.isoformat(),
            "category": category.name if category else None
        }
    }), 201

@expenses.route('/personal', methods=['GET'])
@token_required
def get_personal_expenses(current_user):
    """Get personal expenses with optional filters"""
    # Get query parameters
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query
    query = Expense.query.filter(
        Expense.paid_by == current_user,
        Expense.group_id.is_(None)  # Personal expenses have no group
    )
    
    # Apply filters
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    if start_date:
        query = query.filter(Expense.date >= datetime.fromisoformat(start_date))
    
    if end_date:
        query = query.filter(Expense.date <= datetime.fromisoformat(end_date))
    
    # Get results ordered by date
    expenses = query.order_by(Expense.date.desc()).all()
    
    return jsonify([{
        "id": exp.id,
        "description": exp.description,
        "amount": exp.amount,
        "date": exp.date.isoformat(),
        "category": exp.category.name if exp.category else None
    } for exp in expenses]), 200

@expenses.route('/personal/summary', methods=['GET'])
@token_required
def get_expense_summary(current_user):
    """Get summary of personal expenses by category"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query for personal expenses
    query = db.session.query(
        ExpenseCategory.name,
        db.func.sum(Expense.amount).label('total')
    ).join(
        Expense,
        ExpenseCategory.id == Expense.category_id
    ).filter(
        Expense.paid_by == current_user,
        Expense.group_id.is_(None)
    )
    
    # Apply date filters
    if start_date:
        query = query.filter(Expense.date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Expense.date <= datetime.fromisoformat(end_date))
    
    # Group by category and get results
    summary = query.group_by(ExpenseCategory.name).all()
    
    # Also get total uncategorized expenses
    uncategorized = db.session.query(
        db.func.sum(Expense.amount)
    ).filter(
        Expense.paid_by == current_user,
        Expense.group_id.is_(None),
        Expense.category_id.is_(None)
    )
    
    if start_date:
        uncategorized = uncategorized.filter(Expense.date >= datetime.fromisoformat(start_date))
    if end_date:
        uncategorized = uncategorized.filter(Expense.date <= datetime.fromisoformat(end_date))
    
    uncategorized_total = uncategorized.scalar() or 0
    
    # Combine results
    result = {
        "by_category": [{
            "category": name,
            "total": float(total)
        } for name, total in summary],
        "uncategorized": float(uncategorized_total),
        "total": float(sum(total for _, total in summary) + uncategorized_total)
    }
    
    return jsonify(result), 200
