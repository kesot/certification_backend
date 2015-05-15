import unittest
import requests
import json
import sys
sys.path.append("../")
from defines import SESSION_PORT

session_url = "http://localhost:" + str(SESSION_PORT)


class TestSessionBackendMethods(unittest.TestCase):
    def setUp(self):
        self.login = "ivan"
        self.login_method_url = session_url + "/login"
        self.check_method_url = session_url + "/check"
        self.logout_method_url = session_url + "/logout"

    def test_bad_login_method(self):
        url = self.login_method_url
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 0)
        url += "?login=bad"
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 0)
        url += "&password=bad"
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 0)
        url += "&type=0"
        result = requests.get(url).json()
        self.assertEqual(result["answer"], 0)

    def test_check_bad_method(self):
        url = self.check_method_url
        result = requests.get(url)
        self.assertEqual(result.json()["answer"], 0)
        url += "?code=bad"
        result = requests.get(url)
        self.assertEqual(result.json()["answer"], 0)

    def test_logout_bad_method(self):
        data = {}
        headers = {'Content-type': 'application/json'}
        result = requests.delete(self.logout_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)
        data["code"] = "bad"
        result = requests.delete(self.logout_method_url, data=json.dumps(data), headers=headers)
        self.assertEqual(result.json()["answer"], 0)


if __name__ == "__main__":
    unittest.main(warnings="ignore")