"""
Test cases for Account Model
"""
import unittest
from service import create_app, db
from service.models import Account, DataValidationError

class TestAccountModel(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        pass

    def setUp(self):
        """This runs before each individual test"""
        db.drop_all()  # clean up the old tables
        db.create_all()  # create new tables
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """This runs after each individual test"""
        db.session.remove()
        self.app_context.pop()

    ######################################################################
    # T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """It should create an account and assert its presence"""
        account = Account(
            name="John Doe",
            email="john@example.com",
            address="123 Main St",
            phone_number="555-1234"
        )
        account.create()
        self.assertIsNotNone(account.id)
        self.assertEqual(account.name, "John Doe")
        self.assertEqual(account.email, "john@example.com")

    def test_read_an_account(self):
        """It should read an account by its ID"""
        account = Account(
            name="Alice Smith",
            email="alice@example.com",
            address="456 Elm St",
            phone_number="555-5678"
        )
        account.create()
        self.assertIsNotNone(account.id)
        
        # Retrieve the account from the database
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, "Alice Smith")
        self.assertEqual(found_account.email, "alice@example.com")

    def test_update_an_account(self):
        """It should update account information in the database"""
        account = Account(
            name="Bob Jones",
            email="bob@example.com",
            address="789 Pine St",
            phone_number="555-9012"
        )
        account.create()
        self.assertIsNotNone(account.id)
        
        # Modify the account details
        account.address = "Updated Address 999"
        account.name = "Robert Jones"
        account.update()
        
        # Verify the updates persist
        updated_account = Account.find(account.id)
        self.assertEqual(updated_account.name, "Robert Jones")
        self.assertEqual(updated_account.address, "Updated Address 999")

    def test_delete_an_account(self):
        """It should delete an account and ensure it is removed"""
        account = Account(
            name="Charlie Brown",
            email="charlie@example.com",
            address="12 Peanut St"
        )
        account.create()
        self.assertIsNotNone(account.id)
        
        # Assert the account is in the database
        self.assertEqual(len(Account.all()), 1)
        
        # Delete the account
        account.delete()
        
        # Verify the database is empty
        self.assertEqual(len(Account.all()), 0)
        self.assertIsNone(Account.find(account.id))

    def test_list_all_accounts(self):
        """It should retrieve all active accounts"""
        self.assertEqual(len(Account.all()), 0)
        
        # Create multiple accounts
        account1 = Account(name="User One", email="one@example.com")
        account2 = Account(name="User Two", email="two@example.com")
        account1.create()
        account2.create()
        
        # Verify list length
        self.assertEqual(len(Account.all()), 2)

    def test_serialize_an_account(self):
        """It should serialize an account into a dictionary representation"""
        account = Account(
            name="Danny",
            email="danny@example.com",
            address="789 Main Rd",
            phone_number="111-2222"
        )
        serial_data = account.serialize()
        self.assertEqual(serial_data["name"], "Danny")
        self.assertEqual(serial_data["email"], "danny@example.com")
        self.assertEqual(serial_data["address"], "789 Main Rd")
        self.assertEqual(serial_data["phone_number"], "111-2222")

    def test_deserialize_an_account(self):
        """It should deserialize valid data dictionary into an account model"""
        data = {
            "name": "Emma",
            "email": "emma@example.com",
            "address": "456 Oak Ln",
            "phone_number": "333-4444"
        }
        account = Account()
        account.deserialize(data)
        self.assertEqual(account.name, "Emma")
        self.assertEqual(account.email, "emma@example.com")
        self.assertEqual(account.address, "456 Oak Ln")
        self.assertEqual(account.phone_number, "333-4444")

    def test_deserialize_with_missing_keys(self):
        """It should raise DataValidationError when data keys are missing"""
        bad_data = {
            "address": "Missing name and email"
        }
        account = Account()
        with self.assertRaises(DataValidationError):
            account.deserialize(bad_data)

    def test_deserialize_with_invalid_type(self):
        """It should raise DataValidationError when data type is invalid"""
        account = Account()
        with self.assertRaises(DataValidationError):
            account.deserialize("this is a string, not a dict")
