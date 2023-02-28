from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
poo = Table('poo', post_meta,
    Column('poo', String(length=128), primary_key=True, nullable=False),
    Column('capa', String(length=128)),
    Column('mou', String(length=128)),
    Column('ded', String(length=128)),
    Column('de', String(length=128)),
    Column('de2', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['poo'].columns['de2'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['poo'].columns['de2'].drop()
