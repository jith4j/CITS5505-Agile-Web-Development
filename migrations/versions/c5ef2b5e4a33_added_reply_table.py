"""Added Reply table

Revision ID: c5ef2b5e4a33
Revises: a6c20669e892
Create Date: 2024-05-18 15:33:46.373292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5ef2b5e4a33'
down_revision = 'a6c20669e892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reply', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('reply', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reply_answer_id'), ['answer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_reply_question_id'), ['question_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_reply_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_reply_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reply', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reply_user_id'))
        batch_op.drop_index(batch_op.f('ix_reply_timestamp'))
        batch_op.drop_index(batch_op.f('ix_reply_question_id'))
        batch_op.drop_index(batch_op.f('ix_reply_answer_id'))

    op.drop_table('reply')
    # ### end Alembic commands ###
