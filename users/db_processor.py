from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from db_tables import CONNECTION_ADDRESS, Users, Clients, Base
from defines import LOG_FORMAT, LOG_USERS_FNAME
import logging


class DBProcessor:
    def __init__(self):
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_USERS_FNAME)
        engine = create_engine(CONNECTION_ADDRESS)
        Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def add_entity(self, entity):
        try:
            self.session.add(entity)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database add_entity: {0}".format(str(e)))
            self.session.rollback()
        return False

    def remove_entity(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database remove_entity: {0}".format(str(e)))
            self.session.rollback()
        return False

    def get_entity(self, login, entity_type):
        try:
            if entity_type == 0:
                entity = self.session.query(Users).filter(Users.login == login).one()
            elif entity_type == 1:
                entity = self.session.query(Clients).filter(Clients.login == login).one()
            else:
                raise exc.SQLAlchemyError("unknown entity type")
            return entity
        except exc.SQLAlchemyError as e:
            logging.error("database get_entity: {0}".format(str(e)))
            self.session.rollback()
        return None

    def update_entity(self, data, entity_type):
        try:
            if entity_type == 0:
                entity = self.session.query(Users).filter(Users.login == data["login"]).one()
                entity.update_dict(data)
            elif entity_type == 1:
                entity = self.session.query(Clients).filter(Clients.login == data["login"]).one()
                entity.update_dict(data)
            else:
                raise exc.SQLAlchemyError("unknown entity type")
            self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error("database update_entity: {0}".format(str(e)))
            self.session.rollback()
        return False