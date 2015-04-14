from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import json
import requests
import logging
import sys
sys.path.append("../")
from defines import LOGIC_PORT, SESSION_PORT, USERS_PORT, LOG_FORMAT, LOG_LOGIC_FNAME

define("debug", default=True)

users_url = "http://localhost:" + str(USERS_PORT)
session_url = "http://localhost:" + str(SESSION_PORT)


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        headers = {'Content-type': 'application/json'}
        answer = requests.post(users_url + "/add_user", data=json.dumps(data), headers=headers).json()
        if answer["answer"] == 0:
            logging.error("add_user request: {0}".format(answer["error"]))
        self.write(answer)


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code")
        answer = requests.get(session_url+"/check?code={0}".format(code)).json()
        if answer["answer"] == 0:
            logging.error("get_user request: {0}".format(answer["error"]))
            self.write(answer)
        else:
            login = answer["login"]
            url = users_url + "/get_user?login={0}".format(login)
            self.write(requests.get(url).json())


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        answer = requests.get(session_url+"/check?code={0}".format(data["code"])).json()
        if answer["answer"] == 0:
            logging.error("remove_user request: {0}".format(answer["error"]))
            self.write(answer)
        else:
            headers = {"Content-type": "application/json"}
            requests.delete(session_url + "/logout", data=json.dumps(data), headers=headers)
            data = {"login": answer["login"]}
            answer = requests.delete(users_url + "/remove_user", data=json.dumps(data), headers=headers)
            self.write(answer.json())


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        answer = requests.get(session_url+"/check?code={0}".format(data["code"])).json()
        if answer["answer"] == 0:
            logging.error("get_user request: {0}".format(answer["error"]))
            self.write(answer)
        else:
            data["login"] = answer["login"]
            headers = {"Content-type": "application/json"}
            answer = requests.put(users_url + "/update_user", data=json.dumps(data), headers=headers).json()
            self.write(answer)


class LoginUserHandler(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        url = session_url + "/login?login={0}&password={1}".format(login, password)
        answer = requests.get(url).json()
        if answer["answer"] == 0:
            logging.error("login request: {0}".format(answer["error"]))
        self.write(answer)


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        headers = {"Content-type": "application/json"}
        answer = requests.delete(session_url+"/logout", data=json.dumps(data), headers=headers).json()
        if answer["answer"] == 0:
            logging.error("logout request: {0}".format(answer["error"]))
        self.write(answer)


if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_LOGIC_FNAME)
    logging.info("Logic service started")
    app = tornado.web.Application([(r"/add_user", AddUserHandler),
                                   (r"/get_user", GetUserHandler),
                                   (r"/remove_user", RemoveUserHandler),
                                   (r"/update_user", UpdateUserHandler),
                                   (r"/login", LoginUserHandler),
                                   (r"/logout", LogoutUserHandler)],
                                  debug=options.debug)
    parse_command_line()
    app.listen(LOGIC_PORT)
    tornado.ioloop.IOLoop.instance().start()