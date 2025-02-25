"""empty message

Revision ID: 0485366af6fa
Revises: 2c8a5740d795
Create Date: 2024-10-23 17:52:27.523379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '0485366af6fa'
down_revision: Union[str, None] = '2c8a5740d795'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_closed', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('emotion', sa.Enum('공포', '기쁨', '놀람', '분노', '슬픔', '중립', '혐오', name='emotion'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_chat_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_chat_user_id'), ['user_id'], unique=False)

    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_user', sa.Boolean(), nullable=False),
    sa.Column('emotion', sa.Enum('공포', '기쁨', '놀람', '분노', '슬픔', '중립', '혐오', name='emotion'), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chat_user_id'))
        batch_op.drop_index(batch_op.f('ix_chat_date'))

    op.drop_table('chat')
    # ### end Alembic commands ###
