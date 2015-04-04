from tornado.options import define, options, parse_command_line
from uuid import uuid4
import tornado.ioloop
import tornado.web
import json
import requests
import pylibmc
import time
import logging
import sys
sys.path.append("../")
from defines import SESSION_PORT, USERS_PORT, MEMCACHED_IP, EXPIRATION_TIME, LOG_FORMAT, LOG_SESSION_FNAME

define("debug", default=True)

users_url = "http://localhost:" + str(USERS_PORT)


class LoginUserHandler(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        answer = requests.get(users_url+"/get_user?login={0}".format(login)).json()
        if answer["answer"] == 0:
            logging.error("login request: {0}".format(answer["error"]))
            self.write(answer)
            return
        if password != answer["password"]:
            logging.error("login request: Incorrect login or password")
            self.write(json.dumps({"answer": 0, "error": "Incorrect login or password"}))
        else:
            code = "".join(str(uuid4()).split("-"))
            connections_cache[code] = (login, time.time() + EXPIRATION_TIME)
            self.write(json.dumps({"answer": 1, "code": code}))


class CheckUserAccessHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code")
        if code in connections_cache:
            if time.time() < connections_cache[code][1]:
                login = connections_cache[code][0]
                connections_cache[code] = (login, time.time() + EXPIRATION_TIME)
                self.write(json.dumps({"answer": 1, "login": login}))
            else:
                logging.error("check request: removed code {0} from cache".format(code))
                del connections_cache[code]
                self.write(json.dumps({"answer": 0}))
        else:
            message = "No such code {0}".format(code)
            logging.error("check request: {0}".format(message))
            self.write(json.dumps({"answer": 0, "error": message}))


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        code = data["code"]
        if code in connections_cache:
            del connections_cache[code]
            self.write(json.dumps({"answer": 1}))
        else:
            message = "No such code {0}".format(code)
            logging.error("logout request: {0}".format(message))
            self.write(json.dumps({"answer": 0, "error": message}))


if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_SESSION_FNAME)
    logging.info("Session service started")

    connections_cache = pylibmc.Client([MEMCACHED_IP],
                                       binary=True,
                                       behaviors={"tcp_nodelay": True})

    app = tornado.web.Application([(r"/login", LoginUserHandler),
                                   (r"/check", CheckUserAccessHandler),
                                   (r"/logout", LogoutUserHandler)],
                                  debug=options.debug)
    parse_command_line()
    app.listen(SESSION_PORT)
    tornado.ioloop.IOLoop.instance().start()