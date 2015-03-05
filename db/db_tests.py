import unittest
import db_processor
from db_tables import Users
import hashlib


class TestDBFunctions(unittest.TestCase):
    def setUp(self):
        b_password = "test_passwor".encode("utf-8")
        self.password = hashlib.sha256(b_password).hexdigest()

    def test_add_user(self):
        user = Users(fname="Иван", sname="Иванов", mname="Иванович", 
                birthday="1990-11-11", email="ivanov@test.com", 
                login="ivan", password=self.password)
        self.assertTrue(db_processor.add_user(user))

    def test_get_user(self):
        user = db_processor.get_user("ivan")
        self.assertTrue(user)
        self.assertEqual(user.email, "ivanov@test.com")
        self.assertEqual(user.sname, "Иванов")
        self.assertEqual(str(user.birthday), "1990-11-11")
        self.assertEqual(user.password, self.password)

    def test_remove_user(self):
        user = db_processor.get_user("ivan")
        self.assertTrue(user)
        self.assertTrue(db_processor.remove_user(user))

    def test_bad_add_user(self):
        user = "Not user object"
        self.assertFalse(db_processor.add_user(user))

    def test_bad_get_user(self):
        user = db_processor.get_user("iivanov")
        self.assertFalse(user)

    def test_bad_remove_user(self):
        user = "Not user object"
        self.assertFalse(db_processor.remove_user(user))
        
if __name__ == "__main__":
    unittest.main()
