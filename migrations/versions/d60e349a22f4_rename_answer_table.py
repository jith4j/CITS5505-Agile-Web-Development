"""Rename Answer Table

Revision ID: d60e349a22f4
Revises: d3901026e71b
Create Date: 2024-05-11 17:52:11.070856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd60e349a22f4'
down_revision = 'd3901026e71b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_question_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_question_user_id'), ['user_id'], unique=False)

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_index('ix_answer_timestamp')
        batch_op.drop_index('ix_answer_user_id')

    op.drop_table('answer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.create_index('ix_answer_user_id', ['user_id'], unique=False)
        batch_op.create_index('ix_answer_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_question_user_id'))
        batch_op.drop_index(batch_op.f('ix_question_timestamp'))

    op.drop_table('question')
    # ### end Alembic commands ###
