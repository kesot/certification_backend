import unittest
from db_processor import DBProcessor
from db_tables import Users
import hashlib


class TestDBFunctions(unittest.TestCase):
    def setUp(self):
        b_password = "test_password".encode("utf-8")
        self.password = hashlib.sha256(b_password).hexdigest()
        self.db = DBProcessor()

    def test_user(self):
        data = {"fname": "Иван", "sname": "Иванов", "mname": "Иванович",
                "birthday": "1990-11-11", "email": "ivanov@test.com",
                "login": "ivan", "password": self.password}
        user = Users(data)
        self.assertTrue(self.db.add_user(user))

        user = self.db.get_user("ivan")
        self.assertTrue(user)
        self.assertEqual(user.email, "ivanov@test.com")
        self.assertEqual(user.sname, "Иванов")
        self.assertEqual(str(user.birthday), "1990-11-11")
        self.assertEqual(user.password, self.password)

        self.assertTrue(self.db.remove_user(user))

    def test_bad_add_user(self):
        user = "Not user object"
        self.assertFalse(self.db.add_user(user))

    def test_bad_get_user(self):
        user = self.db.get_user("iivanov")
        self.assertFalse(user)

    def test_bad_remove_user(self):
        user = "Not user object"
        self.assertFalse(self.db.remove_user(user))

if __name__ == "__main__":
    unittest.main()