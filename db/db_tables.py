from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sys
sys.path.append("../")
from defines import DB_PORT, DB_IP


Base = declarative_base()
CONNECTION_ADDRESS = 'postgresql+psycopg2://admin:admin@{0}:{1}/usersDB'.format(DB_IP, DB_PORT)


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

    def __init__(self, data):
        self.update_dict(data)

    def update_dict(self, data):
        for key in data:
            setattr(self, key, data[key])

    def to_json(self):
        return {"fname": self.fname, "sname": self.sname, "mname": self.mname,
                "birthday": str(self.birthday), "email": self.email,
                "login": self.login, "password": self.password}


if __name__ == "__main__":
    engine = create_engine(CONNECTION_ADDRESS)
    Base.metadata.create_all(engine)
