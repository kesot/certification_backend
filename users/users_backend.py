from db_processor import DBProcessor
from db_tables import Users
from tornado.options import define, options, parse_command_line
from defines import USERS_PORT, LOG_FORMAT, LOG_USERS_FNAME
import tornado.ioloop
import tornado.web
import logging
import json

define("debug", default=True)


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        user = Users(data)
        if db.add_user(user):
            self.write(json.dumps({"answer": 1}))
        else:
            logging.error("add_user request: {0}".format(str(data)))
            self.write(json.dumps({"answer": 0, "error": "Can't add new user"}))


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument("login")
        user = db.get_user(login)
        if not user:
            message = "Can't find such user {0}".format(login)
            logging.error("get_user request: {0}".format(message))
            self.write(json.dumps({"answer": 0, "error": message}))
        else:
            user_json = user.to_json()
            user_json["answer"] = 1
            self.write(json.dumps(user_json, ensure_ascii=False))


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        login = data["login"]
        user = db.get_user(login)
        if not user:
            message = "Can't find such user {0}".format(login)
            logging.error("remove_user request: {0}".format(message))
            self.write(json.dumps({"answer": 0, "error": message}))
        else:
            if db.remove_user(user):
                self.write({"answer": 1})
            else:
                message = "Can't remove such user {0}".format(login)
                logging.error("remove_user request: {0}".format(message))
                self.write({"answer": 0, "error": message})


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        if not db.update_user(data):
            logging.error("update_user request: {0}".format(str(data)))
            self.write(json.dumps({"answer": 0, "error": "Can't update such user"}))
        else:
            self.write(json.dumps({"answer": 1}))


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