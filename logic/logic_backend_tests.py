import unittest
import requests
import json
import sys
sys.path.append("../")
from defines import LOGIC_PORT

logic_url = "http://localhost:" + str(LOGIC_PORT)


class TestLogicBackendMethods(unittest.TestCase):
    def setUp(self):
        self.add_user_method_url = logic_url + "/add_user"
        self.get_user_method_url = logic_url + "/get_user"
        self.remove_user_method_url = logic_url + "/remove_user"
        self.update_user_method_url = logic_url + "/update_user"
        self.login_user_method_url = logic_url + "/login"
        self.logout_user_method_url = logic_url + "/logout"

    def test_add_user_method_bad(self):
        data = {"login": "test"}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_user_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_get_user_method_bad(self):
        result = requests.get(self.get_user_method_url + "?code=test")
        self.assertEqual(result.json()["answer"], 0)

    def test_remove_user_method_bad(self):
        data = {"code": "test"}
        headers = {"Content-type": "application/json"}
        result = requests.delete(self.remove_user_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_update_user_method_bad(self):
        data = {"code": "test"}
        headers = {"Content-type": "application/json"}
        result = requests.put(self.update_user_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_login_user_method_bad(self):
        url = self.login_user_method_url + "?login=test&password=test"
        result = requests.get(url)
        self.assertEqual(result.json()["answer"], 0)

    def test_logout_user_method_bad(self):
        data = {"code": "test"}
        headers = {"Content-type": "application/json"}
        result = requests.delete(self.logout_user_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_main(self):
        login = "ivan"
        password = "password"
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": login, "password": password}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_user_method_url, data=json.dumps(data), headers=headers).json()
        self.assertEqual(result["answer"], 1)
        url = self.login_user_method_url + "?login={0}&password={1}".format(login, password)
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 1)
        code = result["code"]
        data = {"code": code}
        headers = {"Content-type": "application/json"}
        result = requests.delete(self.logout_user_method_url, data=json.dumps(data), headers=headers).json()
        self.assertEqual(result["answer"], 1)
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 1)
        code = result["code"]
        data = {"fname": "ИВАН", "email": "test@ivanov.com", "code": code}
        result = requests.put(self.update_user_method_url, data=json.dumps(data), headers=headers).json()
        self.assertEqual(result["answer"], 1)
        result = requests.get(self.get_user_method_url+"?code={0}".format(code)).json()
        old_data = result
        self.assertEqual(result["fname"], "ИВАН")
        self.assertEqual(result["email"], "test@ivanov.com")
        data = {"bad_key": "test", "code": code}
        result = requests.put(self.update_user_method_url, data=json.dumps(data), headers=headers).json()
        self.assertEqual(result["answer"], 1)
        result = requests.get(self.get_user_method_url+"?code={0}".format(code)).json()
        self.assertDictEqual(old_data, result)
        result = requests.delete(self.remove_user_method_url, data=json.dumps(data), headers=headers).json()
        self.assertEqual(result["answer"], 1)
        result = requests.get(self.get_user_method_url+"?code={0}".format(code)).json()
        self.assertEqual(result["answer"], 0)


if __name__ == "__main__":
    unittest.main(warnings="ignore")