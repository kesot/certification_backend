import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from defines import USERS_PORT
import json
import sys
sys.path.append("db/")
import db_processor

define("debug", default=True)


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        user = db_processor.Users(data)
        if db_processor.add_user(user):
            self.write(json.dumps({"answer": 1}))
        else:
            self.write(json.dumps({"answer": 0, "error": "Can't add new user"}))


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument("login")
        user = db_processor.get_user(login)
        if not user:
            self.write(json.dumps({"answer": 0, "error": "Can't find such user"}))
        else:
            user_json = user.to_json()
            user_json["answer"] = 1
            self.write(json.dumps(user_json, ensure_ascii=False))


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        user = db_processor.get_user(data["login"])
        if not user:
            self.write(json.dumps({"answer": 0, "error": "Can't find such user"}))
        else:
            if db_processor.remove_user(user):
                self.write({"answer": 1})
            else:
                self.write({"answer": 0, "error": "Can't remove user"})


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        if not db_processor.update_user(data):
            self.write(json.dumps({"answer": 0, "error": "Can't update such user"}))
        else:
            self.write(json.dumps({"answer": 1}))


app = tornado.web.Application([(r"/add_user", AddUserHandler),
                               (r"/get_user", GetUserHandler),
                               (r"/remove_user", RemoveUserHandler),
                               (r"/update_user", UpdateUserHandler)],
                              debug=options.debug)


if __name__ == "__main__":
    parse_command_line()
    app.listen(USERS_PORT)
    tornado.ioloop.IOLoop.instance().start()