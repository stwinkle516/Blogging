from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import String, Integer, DATETIME, create_engine, select
from datetime import datetime

# Create a session
engine = create_engine('mysql+mysqlconnector://root:Mylifestyle@localhost/blogger')

def db_session():
    conn=Session(engine)
    return conn

















'''
class Base(DeclarativeBase):
    pass
class Users(Base):

    __tablename__ = "users"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Firstname: Mapped[str] = mapped_column(String(45))
    Lastname : Mapped[str] = mapped_column(String(45))
    email : Mapped[str] = mapped_column(String(45))
    contact : Mapped[str] = mapped_column(String(45))
    Pass : Mapped[str] = mapped_column(String(128))
    Created_at : Mapped[str] = mapped_column(DATETIME)
    Updated_at : Mapped[str] = mapped_column(DATETIME)
    Username : Mapped[str] = mapped_column(String(45))




conn = Session(engine)

# new_user = Users()
# new_user.ID = 3
# new_user.Firstname = "lali"
# new_user.Lastname = "Singh"
# new_user.email = "lali@gmail.com"
# new_user.contact = "1234567890"
# new_user.Pass = "password@123"
# new_user.created_at = datetime.now()
# new_user.updated_at = datetime.now()
# new_user.Username = "lalisingh"

# Add the new_user to the session
# conn.add(new_user)
# # Commit the changes to the database
# conn.commit()

# Query and print the results
res = conn.scalars(select(Users)).all()

for i in res:
    print(i.ID, i.Firstname, i.Pass)


# Close the connection
conn.close()'''