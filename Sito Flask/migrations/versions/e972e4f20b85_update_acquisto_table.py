"""update acquisto table

Revision ID: e972e4f20b85
Revises: 
Create Date: 2024-09-21 12:39:05.234669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e972e4f20b85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Acquisto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qta', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Acquisto', schema=None) as batch_op:
        batch_op.drop_column('qta')

    # ### end Alembic commands ###
