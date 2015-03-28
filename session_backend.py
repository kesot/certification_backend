import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from defines import SESSION_PORT, USERS_PORT, MEMCACHED_IP
import json
import requests
from uuid import uuid4
import pylibmc

define("debug", default=True)

users_url = "http://localhost:" + str(USERS_PORT)


class LoginUserHandler(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        answer = requests.get(users_url+"/get_user?login={0}".format(login)).json()
        if answer["answer"] == 0:
            self.write(answer)
            return
        if password != answer["password"]:
            self.write(json.dumps({"answer": 0, "error": "Incorrect login or password"}))
        else:
            code = "".join(str(uuid4()).split("-"))
            connections_cache[code] = login
            self.write(json.dumps({"answer": 1, "code": code}))


class CheckUserAccessHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code")
        if code in connections_cache:
            self.write(json.dumps({"answer": 1, "login": connections_cache[code]}))
        else:
            self.write(json.dumps({"answer": 0}))


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        code = data["code"]
        if code in connections_cache:
            del connections_cache[code]
            self.write(json.dumps({"answer": 1}))
        else:
            self.write(json.dumps({"answer": 0, "error": "No such code"}))


if __name__ == "__main__":
    app = tornado.web.Application([(r"/login", LoginUserHandler),
                                   (r"/check", CheckUserAccessHandler),
                                   (r"/logout", LogoutUserHandler)],
                                  debug=options.debug)
    connections_cache = pylibmc.Client([MEMCACHED_IP],
                                       binary=True,
                                       behaviors={"tcp_nodelay": True})
    parse_command_line()
    app.listen(SESSION_PORT)
    tornado.ioloop.IOLoop.instance().start()