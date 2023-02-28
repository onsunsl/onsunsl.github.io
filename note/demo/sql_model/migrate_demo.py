from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import os

# 参考 https://blog.csdn.net/saltysoda/article/details/117334183

from migrate.versioning import api

SQLITE_FILE_NAME = "database.db"
db = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(db)
Base = declarative_base(engine)


class Poo(Base):
    __tablename__ = 'poo'

    poo = Column(String(128), primary_key=True, unique=True)
    capa = Column(String(128), nullable=True)
    mou = Column(String(128), nullable=True)
    ded = Column(String(128), nullable=True)
    de = Column(String(128), nullable=True)
    de2 = Column(String(128), nullable=True)


if __name__ == '__main__':
    Base.metadata.create_all()
    repo = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_repository')
    if not os.path.exists(repo):
        api.create(repo, 'database repository')
        api.version_control(db, repo)

    migration = repo + '/versions/%03d_migration.py' % (
            api.db_version(db, repo) + 1)
    old_model = api.create_model(db, repo)
    import types

    new = types.ModuleType('old_model')
    exec(old_model, new.__dict__)
    script = api.make_update_script_for_model(db, repo, new.meta,
                                              Base.metadata)
    print(script)
    open(migration, 'wt').write(script)
    api.upgrade(db, repo)

