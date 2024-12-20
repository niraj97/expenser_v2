"""add category support

Revision ID: 8a8834e02ad3
Revises: 935b5d85121c
Create Date: 2024-11-19 01:13:44.297131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a8834e02ad3'
down_revision = '935b5d85121c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_category_user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.create_foreign_key('fk_expense_category_id', 'expense_category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_constraint('fk_expense_category_id', type_='foreignkey')
        batch_op.alter_column('date',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.drop_column('category_id')

    op.drop_table('expense_category')
    # ### end Alembic commands ###
