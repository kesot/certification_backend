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
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

        data["type"] = 3
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_remove_bad_method(self):
        data = {}
        headers = {"Content-type": "application/json"}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["login"] = "test"
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 0
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 1
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_user_add_remove_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password, "type": 0}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data = {"login": "ivan", "type": 1}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 0
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_client_add_remove_method(self):
        data = {"login": "ozon", "password": self.password, "type": 0}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 1
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data = {"login": "ozon", "type": 0}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 1
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_get_bad_method(self):
        result = requests.get(self.get_method_url)
        self.assertEqual(result.json()["answer"], 0)
        result = requests.get(self.get_method_url + "?login=test")
        self.assertEqual(result.json()["answer"], 0)
        result = requests.get(self.get_method_url + "?login=test&type=0")
        self.assertEqual(result.json()["answer"], 0)
        result = requests.get(self.get_method_url + "?login=test&type=1")
        self.assertEqual(result.json()["answer"], 0)

    def test_user_add_get_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password, "type": 0}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data["answer"] = 1
        result = requests.get(self.get_method_url+"?login=ivan&type=1").json()
        self.assertEqual(result["answer"], 0)
        result = requests.get(self.get_method_url+"?login=ivan&type=0").json()
        result["type"] = 0
        self.assertDictEqual(data, result)
        data = {"login": "ivan", "type": 0}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_client_add_get_method(self):
        data = {"login": "ozon", "password": self.password, "type": 1}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data["answer"] = 1
        result = requests.get(self.get_method_url+"?login=ozon&type=0").json()
        self.assertEqual(result["answer"], 0)
        result = requests.get(self.get_method_url+"?login=ozon&type=1").json()
        result["type"] = 1
        self.assertDictEqual(data, result)
        data = {"login": "ozon", "type": 1}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_update_bad_method(self):
        data = {}
        headers = {"Content-type": "application/json"}
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["login"] = "test"
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 0
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["type"] = 1
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)

    def test_user_update_method(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password, "type": 0}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data = {"fname": "Андрей", "sname": "Андреев", "mname": "Андреевич", "login": "ivan", "type": 0}
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        result = requests.get(self.get_method_url + "?login=ivan&type=0").json()
        self.assertEqual(result["answer"], 1)
        self.assertEqual(result["fname"], "Андрей")
        self.assertEqual(result["sname"], "Андреев")
        data = {"login": "ivan", "type": 0}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)

    def test_client_update_method(self):
        data = {"login": "ozon", "password": self.password, "type": 1}
        headers = {"Content-type": "application/json"}
        result = requests.post(self.add_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        data = {"password": "new_password", "login": "ozon", "type": 1}
        result = requests.put(self.update_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)
        result = requests.get(self.get_method_url + "?login=ozon&type=1").json()
        self.assertEqual(result["answer"], 1)
        self.assertEqual(result["password"], "new_password")
        data = {"login": "ozon", "type": 1}
        result = requests.delete(self.remove_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 1)


if __name__ == "__main__":
    unittest.main(warnings='ignore')