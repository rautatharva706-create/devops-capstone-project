"""
Test cases for REST API Routes
"""
import unittest
from service import create_app, db
from service.models import Account

class TestAccountRoutes(unittest.TestCase):
    """Test Cases for REST API Routes"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.client = cls.app.test_client()

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
    # U T I L I T Y   F U N C T I O N S
    ######################################################################

    def _create_accounts(self, count):
        """Helper method to seed accounts in the database"""
        accounts = []
        for i in range(count):
            account = Account(
                name=f"Test User {i}",
                email=f"user{i}@example.com",
                address=f"Street {i}",
                phone_number=f"555-{i:04d}"
            )
            account.create()
            accounts.append(account)
        return accounts

    ######################################################################
    # T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should return the root landing page details"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Customer Accounts Microservice")
        self.assertIn("endpoints", data)

    def test_health(self):
        """It should return healthy status code 200"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")

    def test_create_account(self):
        """It should create a new account successfully"""
        new_account = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "address": "456 Oak Ave",
            "phone_number": "555-9876"
        }
        response = self.client.post(
            "/accounts",
            json=new_account,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], "Jane Doe")
        self.assertEqual(data["email"], "jane@example.com")

    def test_create_account_bad_request(self):
        """It should return 400 Bad Request when missing fields"""
        bad_account = {
            "address": "Missing name and email"
        }
        response = self.client.post(
            "/accounts",
            json=bad_account,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_account_unsupported_media_type(self):
        """It should return 415 Unsupported Media Type on bad content type"""
        new_account = {"name": "Jane", "email": "jane@example.com"}
        response = self.client.post(
            "/accounts",
            json=new_account,
            content_type="text/plain"
        )
        self.assertEqual(response.status_code, 415)

    def test_read_account(self):
        """It should retrieve a specific account"""
        accounts = self._create_accounts(1)
        account_id = accounts[0].id
        
        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], account_id)
        self.assertEqual(data["name"], "Test User 0")

    def test_read_account_not_found(self):
        """It should return 404 if account is not found"""
        response = self.client.get("/accounts/9999")
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        """It should update an existing account"""
        accounts = self._create_accounts(1)
        account_id = accounts[0].id
        
        updated_data = {
            "name": "Jane Modified",
            "email": "user0@example.com",
            "address": "New Address 101",
            "phone_number": "555-0000"
        }
        response = self.client.put(
            f"/accounts/{account_id}",
            json=updated_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Jane Modified")
        self.assertEqual(data["address"], "New Address 101")

    def test_update_account_not_found(self):
        """It should return 404 if trying to update non-existing account"""
        updated_data = {"name": "Test", "email": "test@example.com"}
        response = self.client.put(
            "/accounts/9999",
            json=updated_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_account(self):
        """It should delete an account and return 204 No Content"""
        accounts = self._create_accounts(1)
        account_id = accounts[0].id
        
        # Verify it exists first
        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)
        
        # Delete it
        response = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 204)
        
        # Verify it is gone
        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 404)

    def test_list_all_accounts(self):
        """It should list all accounts"""
        self._create_accounts(3)
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_method_not_allowed(self):
        """It should return 405 Method Not Allowed for disallowed HTTP actions"""
        response = self.client.delete("/accounts")
        self.assertEqual(response.status_code, 405)

    def test_security_headers(self):
        """It should verify that Talisman HTTP Security Headers are set"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        # Verify standard Talisman secure HTTP headers are present
        headers = response.headers
        self.assertIn("X-Frame-Options", headers)
        self.assertEqual(headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertIn("X-Content-Type-Options", headers)
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("X-XSS-Protection", headers)
        
    def test_cors_policy(self):
        """It should verify that CORS headers are active on the response"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        # Verify Access-Control-Allow-Origin header is present
        headers = response.headers
        self.assertIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")
