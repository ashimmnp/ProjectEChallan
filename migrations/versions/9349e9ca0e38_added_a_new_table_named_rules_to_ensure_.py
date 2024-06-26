"""Added a new table named rules to ensure a proper data and rule description in it and be selected by officer later
Revision ID: 9349e9ca0e38
Revises: aabe6ec313d9
Create Date: 2024-04-02 16:33:41.266970
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9349e9ca0e38'
down_revision = 'aabe6ec313d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rulesAndRegulations',
    sa.Column('rulesId', sa.String(length=255), nullable=False),
    sa.Column('rulecategory', sa.String(length=255), nullable=True),
    sa.Column('ruleDesc', sa.String(length=225), nullable=True),
    sa.PrimaryKeyConstraint('rulesId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rulesAndRegulations')
    # ### end Alembic commands ###