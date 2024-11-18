from flask import Blueprint, request, jsonify
from ..models.group import Group, GroupMembership
from ..models.user import User
from .. import db
from ..utils.jwt_utils import token_required

groups = Blueprint('groups', __name__)

@groups.route('/create', methods=['POST'])
@token_required
def create_group(current_user):
    """Create a new group"""
    data = request.get_json()
    
    # Validate input
    if not data.get('name'):
        return jsonify({"error": "Group name is required"}), 400
    
    # Create group
    new_group = Group(
        name=data.get('name'),
        description=data.get('description', '')
    )
    db.session.add(new_group)
    
    # Add current user as admin
    membership = GroupMembership(
        user=current_user,
        group=new_group,
        role='admin'
    )
    db.session.add(membership)
    
    # Add other members if specified
    members = data.get('members', [])
    for member_email in members:
        user = User.query.filter_by(email=member_email).first()
        if user and user != current_user:
            member_membership = GroupMembership(
                user=user,
                group=new_group,
                role='member'
            )
            db.session.add(member_membership)
    
    db.session.commit()
    
    return jsonify({
        "message": "Group created successfully",
        "group_id": new_group.id
    }), 201

@groups.route('/', methods=['GET'])
@token_required
def get_user_groups(current_user):
    """Retrieve groups for the current user"""
    user_groups = []
    
    for membership in current_user.group_memberships:
        group = membership.group
        group_data = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_at": group.created_at,
            "role": membership.role,
            "members": []
        }
        
        # Get group members
        for member_ship in group.memberships:
            group_data['members'].append({
                "id": member_ship.user.id,
                "username": member_ship.user.username,
                "role": member_ship.role
            })
        
        user_groups.append(group_data)
    
    return jsonify(user_groups), 200

@groups.route('/<int:group_id>/add_member', methods=['POST'])
@token_required
def add_group_member(current_user, group_id):
    """Add a member to a group"""
    group = Group.query.get_or_404(group_id)
    
    # Check if current user is an admin
    current_membership = GroupMembership.query.filter_by(
        user=current_user, 
        group=group, 
        role='admin'
    ).first()
    
    if not current_membership:
        return jsonify({"error": "Only group admins can add members"}), 403
    
    data = request.get_json()
    member_email = data.get('email')
    
    if not member_email:
        return jsonify({"error": "Email is required"}), 400
    
    user = User.query.filter_by(email=member_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Check if user is already a member
    existing_membership = GroupMembership.query.filter_by(
        user=user, 
        group=group
    ).first()
    
    if existing_membership:
        return jsonify({"error": "User is already a member of this group"}), 400
    
    # Add new membership
    new_membership = GroupMembership(
        user=user,
        group=group,
        role='member'
    )
    db.session.add(new_membership)
    db.session.commit()
    
    return jsonify({
        "message": "Member added successfully",
        "user_id": user.id
    }), 201
