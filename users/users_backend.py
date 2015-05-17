from db_processor import DBProcessor
from db_tables import Users, Clients
from tornado.options import define, options, parse_command_line
from defines import USERS_PORT, LOG_FORMAT, LOG_USERS_FNAME
import tornado.ioloop
import tornado.web
import logging
import json

define("debug", default=True)


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            if not "type" in data:
                raise Exception("Argument 'type' required")

            entity_type = int(data["type"])
            if entity_type == 0:
                entity = Users(data)
            elif entity_type == 1:
                entity = Clients(data)
            else:
                raise Exception("Unknown value for 'type' argument")

            if db.add_entity(entity):
                self.set_status(200)
            else:
                raise Exception("Can't add new user")

        except Exception as e:
            logging.error("add_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            login = self.get_argument("login")
            entity_type = int(self.get_argument("type"))

            entity = db.get_entity(login, entity_type)
            if not entity:
                raise Exception("Can't find such user {0}".format(login))

            self.set_status(200)
            self.write(json.dumps(entity.to_json(), ensure_ascii=False))

        except Exception as e:
            logging.error("get_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            if not "login" in data:
                raise Exception("Argument 'login' required")
            if not "type" in data:
                raise Exception("Argument 'type' required")

            login = data["login"]
            entity_type = int(data["type"])

            entity = db.get_entity(login, entity_type)
            if not entity:
                raise Exception("Can't find user with login {0}".format(login))

            if db.remove_entity(entity):
                self.set_status(200)
            else:
                raise Exception("Can't remove user with login {0}".format(login))

        except Exception as e:
            logging.error("remove_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            if not "login" in data:
                raise Exception("Argument 'login' required")
            if not "type" in data:
                raise Exception("Argument 'type' required")

            entity_type = int(data["type"])

            if not db.update_entity(data, entity_type):
                raise Exception("Can't update user with login {0}".format(data["login"]))

            self.set_status(200)

        except Exception as e:
            logging.error("update_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_USERS_FNAME)
    logging.info("Users service started")
    db = DBProcessor()
    app = tornado.web.Application([(r"/add_user", AddUserHandler),
                                   (r"/get_user", GetUserHandler),
                                   (r"/remove_user", RemoveUserHandler),
                                   (r"/update_user", UpdateUserHandler)],
                                  debug=options.debug)
    parse_command_line()
    app.listen(USERS_PORT)
    tornado.ioloop.IOLoop.instance().start()