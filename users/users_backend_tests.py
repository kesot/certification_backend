import unittest
import requests
import hashlib
import json
import sys
sys.path.append("../")
from defines import USERS_PORT

users_url = "http://localhost:" + str(USERS_PORT)


class TestUsersBackendMethods(unittest.TestCase):
    def setUp(self):
        b_password = "test_password".encode("utf-8")
        self.password = hashlib.sha256(b_password).hexdigest()
        self.add_method_url = users_url + "/add_user"
        self.get_method_url = users_url + "/get_user"
        self.remove_method_url = users_url + "/remove_user"
        self.update_method_url = users_url + "/update_user"

    def test_add_bad_method(self):
        """
        the password-field is missing
        """
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan"}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_remove_bad_method(self):
        """
        the login 'test_user' not exist
        """
        data = {"login": "test_user"}
        headers = {"Content-type": "application/json"}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_get_bad_method(self):
        """
        the login 'test_user' not exist
        """
        result = requests.get(self.get_method_url+"?login=test_user")
        self.assertEqual(result.json()["answer"], 0)

    def test_update_bad_method(self):
        """
        the login 'test_user' not exist
        """
        data = {"login": "test_user"}
        headers = {"Content-type": "application/json"}
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_add_remove_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data = {"login": "ivan"}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_get_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data["answer"] = 1
        result = requests.get(self.get_method_url+"?login=ivan").json()
        self.assertDictEqual(data, result)
        data = {"login": "ivan"}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_update_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data = {"fname": "Андрей", "sname": "Андреев", "mname": "Андреевич",
                "birthday": "1991-12-12", "email": "andreev@test.com",
                "login": "ivan", "password": self.password}
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data = {"login": "ivan"}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)


if __name__ == "__main__":
    unittest.main(warnings='ignore')