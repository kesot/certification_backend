from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import json
import requests
import logging
import sys
sys.path.append("../")
from defines import LOGIC_PORT, SESSION_PORT, USERS_PORT, CERTIFICATES_PORT, LOG_FORMAT, LOG_LOGIC_FNAME

define("debug", default=True)

users_url = "http://localhost:" + str(USERS_PORT)
session_url = "http://localhost:" + str(SESSION_PORT)
certificates_url = "http://localhost" + str(CERTIFICATES_PORT)


class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            headers = {'Content-type': 'application/json'}

            answer = requests.post(users_url + "/add_user", data=json.dumps(data), headers=headers).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                self.write(answer)

        except Exception as e:
            logging.error("add_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"answer": 0, "error": str(e)}))


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            code = self.get_argument("code")

            answer = requests.get(session_url+"/check?code={0}".format(code)).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                login = answer["login"]
                entity_type = answer["type"]
                url = users_url + "/get_user?login={0}&type={1}".format(login, entity_type)

                answer = requests.get(url).json()
                if answer["answer"] == 0:
                    raise Exception(answer["error"])
                else:
                    self.write(answer)

        except Exception as e:
            logging.error("get_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"answer": 0, "error": str(e)}))


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]

            answer = requests.get(session_url+"/check?code={0}".format(code)).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                headers = {"Content-type": "application/json"}
                requests.delete(session_url + "/logout", data=json.dumps(data), headers=headers)

                data = {"login": answer["login"], "type": answer["type"]}
                answer = requests.delete(users_url + "/remove_user", data=json.dumps(data), headers=headers).json()
                if answer["answer"] == 0:
                    raise Exception(answer["error"])
                else:
                    self.write(answer)

        except Exception as e:
            logging.error("remove_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"answer": 0, "error": str(e)}))


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]

            answer = requests.get(session_url+"/check?code={0}".format(code)).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                data["login"] = answer["login"]
                data["type"] = answer["type"]
                headers = {"Content-type": "application/json"}

                answer = requests.put(users_url + "/update_user", data=json.dumps(data), headers=headers).json()
                if answer["answer"] == 0:
                    raise Exception(answer["error"])
                else:
                    self.write(answer)

        except Exception as e:
            logging.error("get_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"answer": 0, "error": str(e)}))


class LoginUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            entity_type = self.get_argument("type")

            url = session_url + "/login?login={0}&password={1}&type={2}".format(login, password, entity_type)
            answer = requests.get(url).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                self.write(answer)

        except Exception as e:
                logging.error("login request: {0}".format(str(e)))
                self.set_status(400)
                self.write(json.dumps({"answer": 0, "error": str(e)}))


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            headers = {"Content-type": "application/json"}

            answer = requests.delete(session_url+"/logout", data=json.dumps(data), headers=headers).json()
            if answer["answer"] == 0:
                raise Exception(answer["error"])
            else:
                self.write(answer)

        except Exception as e:
                logging.error("logout request: {0}".format(str(e)))
                self.set_status(400)
                self.write(json.dumps({"answer": 0, "error": str(e)}))


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