from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import json
import requests
import logging
import sys
sys.path.append("../")
from defines import LOGIC_PORT, SESSION_PORT, USERS_PORT, LOG_FORMAT, LOG_LOGIC_FNAME
from helper import check_status_code

define("debug", default=True)

users_url = "http://localhost:" + str(USERS_PORT)
session_url = "http://localhost:" + str(SESSION_PORT)
certificates_url = "http://certificatesbackend.azurewebsites.net/"


########################################
############ Users Handlers ############
########################################
class AddUserHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            headers = {'Content-type': 'application/json'}

            if int(data["type"]) == 1:
                company = data["company"]
                answer = requests.get(certificates_url + "/api/Companies/ByName?companyName={0}".format(company))
                if not check_status_code(answer.status_code):
                    company_data = {"Name": company}
                    answer = requests.post(certificates_url + "/api/Companies", data=json.dumps(company_data), headers=headers)
                    if not check_status_code(answer.status_code):
                        raise Exception("Can't add new company with name {0}".format(company))

                data["firm_id"] = answer.json()["Id"]

            answer = requests.post(users_url + "/add_user", data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception(answer.json()["error"])

            self.set_status(200)

        except Exception as e:
            logging.error("add_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            code = self.get_argument("code")

            answer = requests.get(session_url+"/check?code={0}".format(code))
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            login = answer_data["login"]
            entity_type = answer_data["type"]
            url = users_url + "/get_user?login={0}&type={1}".format(login, entity_type)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            self.set_status(200)
            self.write(answer_data)

        except Exception as e:
            logging.error("get_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class RemoveUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]

            answer = requests.get(session_url+"/check?code={0}".format(code))
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            headers = {"Content-type": "application/json"}
            requests.delete(session_url + "/logout", data=json.dumps(data), headers=headers)

            data = {"login": answer_data["login"], "type": answer_data["type"]}
            answer = requests.delete(users_url + "/remove_user", data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception(answer.json()["error"])

            self.set_status(200)

        except Exception as e:
            logging.error("remove_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class UpdateUserHandler(tornado.web.RequestHandler):
    def put(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]

            answer = requests.get(session_url+"/check?code={0}".format(code))
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            data["login"] = answer_data["login"]
            data["type"] = answer_data["type"]
            headers = {"Content-type": "application/json"}

            answer = requests.put(users_url + "/update_user", data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception(answer.json()["error"])

            self.set_status(200)

        except Exception as e:
            logging.error("get_user request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class LoginUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            entity_type = self.get_argument("type")

            url = session_url + "/login?login={0}&password={1}&type={2}".format(login, password, entity_type)
            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            self.set_status(200)
            self.write(answer_data)

        except Exception as e:
                logging.error("login request: {0}".format(str(e)))
                self.set_status(400)
                self.write(json.dumps({"error": str(e)}))


class LogoutUserHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            headers = {"Content-type": "application/json"}

            answer = requests.delete(session_url+"/logout", data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception(answer.json()["error"])

            self.set_status(200)

        except Exception as e:
                logging.error("logout request: {0}".format(str(e)))
                self.set_status(400)
                self.write(json.dumps({"error": str(e)}))


############################################
############ Companies Handlers ############
############################################
class CompaniesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = certificates_url + "/api/Companies"

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get companies list")

            self.set_status(200)
            self.write(json.dumps(answer.json(), ensure_ascii=False))

        except Exception as e:
            logging.error("companies request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


##################################################
############ CertificateSets Handlers ############
##################################################
class CertificateSetsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            page_index = self.get_argument("pageIndex")
            page_size = self.get_argument("pageSize")
            url = certificates_url + "/api/CertificateSets?pageIndex={0}&pageSize={1}".format(page_index, page_size)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get certificateSets list")

            ignore_keys = ["MaskString", "AdministrativeName", "CompanyId", "AllCertificatesGenerated"]
            answer_data = [{key: certificate[key] for key in certificate if key not in ignore_keys}
                           for certificate in answer.json()]

            self.set_status(200)
            self.write(json.dumps(answer_data, ensure_ascii=False))

        except Exception as e:
            logging.error("certificateSets request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class CertificateSetsByCompanyHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            company_id = self.get_argument("companyId")
            url = certificates_url + "/api/CertificateSets/ByCompany?companyId={0}".format(company_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get certificateSets from company with id {0}".format(company_id))

            ignore_keys = ["MaskString", "AdministrativeName", "CompanyId", "AllCertificatesGenerated"]
            answer_data = [{key: certificate[key] for key in certificate if key not in ignore_keys}
                           for certificate in answer.json()]

            self.set_status(200)
            self.write(json.dumps(answer_data, ensure_ascii=False))

        except Exception as e:
            logging.error("certificateSetsByCompany request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class CertificateSetsByIdHandler(tornado.web.RequestHandler):
    def get(self, _id=None):
        try:
            url = certificates_url + "/api/CertificateSets/{0}".format(_id)
            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get info about certificateSet with id {0}".format(_id))

            ignore_keys = ["MaskString", "AdministrativeName", "CompanyId", "AllCertificatesGenerated"]
            answer_json = answer.json()
            answer_data = {key: answer_json[key] for key in answer_json if key not in ignore_keys}

            self.set_status(200)
            self.write(json.dumps(answer_data, ensure_ascii=False))

        except Exception as e:
            logging.error("certificateSetsById request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


#########################################
############ Orders Handlers ############
#########################################
class OrdersByUserHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            code = self.get_argument("code")
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            url = certificates_url + "/api/Orders/ByUser/{0}".format(user_id)
            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get orders list for user with id {0}".format(user_id))

            self.set_status(200)
            self.write(json.dumps(answer.json(), ensure_ascii=False))

        except Exception as e:
            logging.error("ordersByUser request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class OrdersByIdHandler(tornado.web.RequestHandler):
    def get(self, _id=None):
        try:
            code = self.get_argument("code")
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            url = certificates_url + "/api/Orders/{0}".format(_id)
            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get order with id {0}".format(_id))

            answer_data = answer.json()
            if user_id != answer_data["UserExternalId"]:
                raise Exception("Access denied for user with id {0} to order with id {1}".format(user_id, _id))

            self.set_status(200)
            self.write(json.dumps(answer_data, ensure_ascii=False))

        except Exception as e:
            logging.error("ordersById request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class AddCertificatesToCartHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            set_id = data["id"]
            url = certificates_url + "/api/CertificateSets/{0}/first-available-certificate".format(set_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get available certificate from certificateSet with id {0}".format(set_id))

            certificate_id = answer.json()["Id"]
            url = certificates_url + "/api/Orders/last-unpaid/{0}".format(user_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                url = certificates_url + "/api/Orders/create-for-user/{0}".format(user_id)
                answer = requests.post(url)
                if not check_status_code(answer.status_code):
                    raise Exception("Can't create cart for user with id {0}".format(user_id))

            order_id = answer.json()["Id"]
            headers = {'Content-type': 'application/json'}
            url = certificates_url + "/api/Orders/{0}/add-certificates".format(order_id)
            data = [certificate_id]

            answer = requests.post(url, data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception("Can't add certificates to cart with id {0}".format(order_id))

            self.set_status(200)

        except Exception as e:
            logging.error("addCertificateToCart request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class GetCartHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            code = self.get_argument("code")
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            url = certificates_url + "/api/Orders/last-unpaid/{0}".format(user_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get cart for user with id {0}".format(user_id))

            self.set_status(200)
            self.write(json.dumps(answer.json(), ensure_ascii=False))

        except Exception as e:
            logging.error("getCart request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class RemoveCertificatesFromCartHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            code = data["code"]
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            url = certificates_url + "/api/Orders/last-unpaid/{0}".format(user_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get cart for user with id {0}".format(user_id))

            order_id = answer.json()["Id"]
            headers = {'Content-type': 'application/json'}
            url = certificates_url + "/api/Orders/{0}/remove-certificates".format(order_id)
            data = data["certificates"]

            answer = requests.delete(url, data=json.dumps(data), headers=headers)
            if not check_status_code(answer.status_code):
                raise Exception("Can't remove certificates from cart with id {0}".format(order_id))

            self.set_status(200)

        except Exception as e:
            logging.error("removeCertificateFromCart request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


class ConfirmPaymentHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            code = self.get_argument("code")
            url = session_url+"/check?code={0}".format(code)

            answer = requests.get(url)
            answer_data = answer.json()
            if not check_status_code(answer.status_code):
                raise Exception(answer_data["error"])

            if answer_data["type"] != 0:
                raise Exception("Method not available for this user (bad entity_type)")

            user_id = answer_data["id"]
            url = certificates_url + "/api/Orders/last-unpaid/{0}".format(user_id)

            answer = requests.get(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't get cart for user with id {0}".format(user_id))

            order_id = answer.json()["Id"]
            url = certificates_url + "/api/Orders/{0]/confirm-payment".format(order_id)

            answer = requests.post(url)
            if not check_status_code(answer.status_code):
                raise Exception("Can't confirm payment for cart with id {0}".format(order_id))

            self.set_status(200)

        except Exception as e:
            logging.error("confirmPayment request: {0}".format(str(e)))
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_LOGIC_FNAME)
    logging.info("Logic service started")
    app = tornado.web.Application([(r"/add_user", AddUserHandler),
                                   (r"/get_user", GetUserHandler),
                                   (r"/remove_user", RemoveUserHandler),
                                   (r"/update_user", UpdateUserHandler),
                                   (r"/login", LoginUserHandler),
                                   (r"/logout", LogoutUserHandler),
                                   (r"/companies", CompaniesHandler),
                                   (r"/certificateSets", CertificateSetsHandler),
                                   (r"/certificateSets/company", CertificateSetsByCompanyHandler),
                                   (r"/certificateSets/([0-9]+)", CertificateSetsByIdHandler),
                                   (r"/orders/user", OrdersByUserHandler),
                                   (r"/orders/([0-9]+)", OrdersByIdHandler),
                                   (r"/orders/add_to_cart", AddCertificatesToCartHandler),
                                   (r"/orders/get_cart", GetCartHandler),
                                   (r"/orders/remove_from_cart", RemoveCertificatesFromCartHandler),
                                   (r"/orders/confirm_payment", ConfirmPaymentHandler)],
                                  debug=options.debug)
    parse_command_line()
    app.listen(LOGIC_PORT)
    tornado.ioloop.IOLoop.instance().start()