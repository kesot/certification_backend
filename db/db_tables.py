from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()
server = "127.0.0.1"
port= "5432"
def_db_connection_string = 'postgresql+psycopg2://admin:admin@{0}:{1}/usersDB'.format(server, port)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    fname = Column(String, nullable=False)
    sname = Column(String, nullable=False)
    mname = Column(String, nullable=False)
    birthday = Column(Date)
    email = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


if __name__ == "__main__":
    engine = create_engine(def_db_connection_string)
    Base.metadata.create_all(engine)
