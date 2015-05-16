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
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            entity_type = int(self.get_argument("type"))

            answer = requests.get(users_url+"/get_user?login={0}&type={1}".format(login, entity_type))
            answer_data = answer.json()
            if answer.status_code != 200:
                raise Exception(answer_data["error"])

            if password != answer_data["password"]:
                raise Exception("Incorrect login or password")
            else:
                code = "".join(str(uuid4()).split("-"))
                connections_cache[code] = (login, entity_type, time.time() + EXPIRATION_TIME)
                self.set_status(200)
                self.write(json.dumps({"code": code}))

        except Exception as e:
            logging.error("login request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class CheckUserAccessHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            code = self.get_argument("code")

            if code in connections_cache:
                connection_info = connections_cache[code]
                if time.time() < connection_info[2]:
                    login = connection_info[0]
                    entity_type = connection_info[1]
                    connections_cache[code] = (login, entity_type, time.time() + EXPIRATION_TIME)
                    self.set_status(200)
                    self.write(json.dumps({"login": login, "type": entity_type}))
                else:
                    del connections_cache[code]
                    raise Exception("removed code {0} from cache".format(code))
            else:
                raise Exception("No such code {0}".format(code))

        except Exception as e:
            logging.error("check request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]

            if code in connections_cache:
                del connections_cache[code]
                self.set_status(200)
            else:
                raise Exception("No such code {0}".format(code))

        except Exception as e:
            logging.error("logout request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


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