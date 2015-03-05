from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from db_tables import def_db_connection_string, Users, Base


def add_user(user):
    try:
        session.add(user)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        pass
        # write to log.error here
    return False


def remove_user(user):
    try:
        session.delete(user)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        pass
        # write to log.error here
    return False


def get_user(login):
    try:
        user = session.query(Users).filter(Users.login == login).one()
        return user
    except exc.SQLAlchemyError as e:
        pass
    # write to log.error here
    return None

    
# create global session instance
engine = create_engine(def_db_connection_string)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
