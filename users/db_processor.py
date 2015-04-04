from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from db_tables import CONNECTION_ADDRESS, Users, Base
from defines import LOG_FORMAT, LOG_USERS_FNAME
import logging


class DBProcessor:
    def __init__(self):
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_USERS_FNAME)
        engine = create_engine(CONNECTION_ADDRESS)
        Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def add_user(self, user):
        try:
            self.session.add(user)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database add_user: {0}".format(str(e)))
            self.session.rollback()
        return False

    def remove_user(self, user):
        try:
            self.session.delete(user)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database remove_user: {0}".format(str(e)))
            self.session.rollback()
        return False

    def get_user(self, login):
        try:
            user = self.session.query(Users).filter(Users.login == login).one()
            return user
        except exc.SQLAlchemyError as e:
            logging.error("database remove_user: {0}".format(str(e)))
            self.session.rollback()
        return None

    def update_user(self, data):
        try:
            user = self.session.query(Users).filter(Users.login == data["login"]).one()
            user.update_dict(data)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database remove_user: {0}".format(str(e)))
            self.session.rollback()
        return False