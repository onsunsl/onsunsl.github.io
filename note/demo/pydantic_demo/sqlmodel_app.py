from typing import Optional

from pydantic import Json
from sqlmodel import JSON, Column, Field, Session, SQLModel, create_engine, select


class MyTable(SQLModel, table=True):
    """My table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    extras: Json = Field(default_factory=dict, sa_column=Column(JSON))


SQLITE_FILE_NAME = "database.db"
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    """Create db and tables."""
    SQLModel.metadata.create_all(engine)


def my_table_ops():
    """My table ops."""
    with Session(engine) as session:
        row1 = MyTable(name="ZHOU-01")
        # session.add(row1)

        row2 = MyTable(name="ZHOU-02", extras='{"name":"zhou-02"}')
        # session.add(row2)

        row3 = MyTable(name="ZHOU-03")
        row3.extras["name"] = "zhou-03"
        # session.add(row3)

        row4 = MyTable(name="ZHOU-04")
        row4.extras = dict(name="zhou-04", age=18)
        # session.add(row4)

        row5 = MyTable(name="ZHOU-05", extras=dict(name="zhou-05"))  # not working
        # session.add(row5)

        session.add_all([row1, row2, row3, row4, row5])
        session.commit()

    # with Session(engine) as session:
    #     row = session.exec(select(MyTable).where(MyTable.name == "ZHOU-02")).one()
    #     print("Result: ", row)
    #
    #     row.extras = dict(is_teacher=True, age=90)
    #     session.add(row)
    #     session.commit()
    #     print("Result2: ", row)
    #
    #     session.refresh(row)
    #     print("Result3: ", row)


def main():
    """Main."""
    create_db_and_tables()
    my_table_ops()


if __name__ == "__main__":
    main()
