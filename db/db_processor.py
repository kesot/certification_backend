from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from db_tables import CONNECTION_ADDRESS, Users, Base


def add_user(user):
    try:
        session.add(user)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        session.rollback()
        pass
        # write to log.error here
    return False


def remove_user(user):
    try:
        session.delete(user)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        session.rollback()
        pass
        # write to log.error here
    return False


def get_user(login):
    try:
        user = session.query(Users).filter(Users.login == login).one()
        return user
    except exc.SQLAlchemyError as e:
        session.rollback()
        pass
        # write to log.error here
    return None


def update_user(data):
    try:
        user = session.query(Users).filter(Users.login == data["login"]).one()
        user.update_dict(data)
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        session.rollback()
        pass
        # write to log.error here
    return False

    
# create global session instance
engine = create_engine(CONNECTION_ADDRESS)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()