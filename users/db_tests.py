import unittest
from db_processor import DBProcessor
from db_tables import Users, Clients
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
        self.assertTrue(self.db.add_entity(user))

        user = self.db.get_entity("ivan", 0)
        self.assertTrue(user)
        self.assertEqual(user.email, "ivanov@test.com")
        self.assertEqual(user.sname, "Иванов")
        self.assertEqual(str(user.birthday), "1990-11-11")
        self.assertEqual(user.password, self.password)

        self.assertTrue(self.db.remove_entity(user))

    def test_bad_add_user(self):
        user = "Not user object"
        self.assertFalse(self.db.add_entity(user))

    def test_bad_get_user(self):
        user = self.db.get_entity("iivanov", 0)
        self.assertFalse(user)

    def test_bad_remove_user(self):
        user = "Not user object"
        self.assertFalse(self.db.remove_entity(user))

    def test_client(self):
        data = {"login": "test_client", "password": self.password}
        client = Clients(data)
        self.assertTrue(self.db.add_entity(client))

        client = self.db.get_entity("test_client", 1)
        self.assertTrue(client)
        self.assertEqual(client.password, self.password)

        self.assertTrue(self.db.remove_entity(client))

    def test_bad_add_client(self):
        client = "Not client object"
        self.assertFalse(self.db.add_entity(client))

    def test_bad_get_client(self):
        client = self.db.get_entity("ttest_client", 1)
        self.assertFalse(client)

    def test_bad_remove_client(self):
        client = "Not client object"
        self.assertFalse(self.db.remove_entity(client))

if __name__ == "__main__":
    unittest.main()