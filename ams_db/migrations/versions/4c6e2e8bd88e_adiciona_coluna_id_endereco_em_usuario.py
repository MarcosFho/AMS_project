"""adiciona coluna id_endereco em usuario

Revision ID: 4c6e2e8bd88e
Revises: 464f721501c4
Create Date: 2025-05-31 14:11:42.340571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4c6e2e8bd88e'
down_revision: Union[str, None] = '464f721501c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column('usuario', sa.Column('id_endereco', sa.Integer(), nullable=True))
    op.create_foreign_key(
        None,
        'usuario',
        'endereco',
        ['id_endereco'],
        ['id'],
        ondelete='SET NULL'
    )



def downgrade() -> None:
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_column('usuario', 'id_endereco')
