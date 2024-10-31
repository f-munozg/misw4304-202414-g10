import unittest
import os
from unittest.mock import patch, MagicMock
from flask import json
from flask_jwt_extended import create_access_token
from application import create_app
from models.models import db, Blacklist

class TestCheckBlacklist(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'true'
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Initialize the app context and db
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)  # Ensure that db is initialized

        self.jwt_token = create_access_token(identity='test_user')

    def tearDown(self):
        self.app_context.pop()

    @patch('models.models.Blacklist.query')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_check_blacklist_email_exists(self, mock_get_jwt_identity, mock_blacklist_query):
        mock_get_jwt_identity.return_value = 'test_user'
        
        # Mock the Blacklist object to be returned
        mock_mail = MagicMock()
        mock_mail.blocked_reason = "spam"
        mock_blacklist_query.filter.return_value.first.return_value = mock_mail

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={'Authorization': f'Bearer {self.jwt_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mail_blacklisted'], True)
        self.assertEqual(response.json['blacklist_reason'], "spam")
        mock_blacklist_query.filter.assert_called_once()

    @patch('models.models.Blacklist.query')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_check_blacklist_email_not_exists(self, mock_get_jwt_identity, mock_blacklist_query):
        mock_get_jwt_identity.return_value = 'test_user'
        mock_blacklist_query.filter.return_value.first.return_value = None

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={'Authorization': f'Bearer {self.jwt_token}'}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['mail_blacklisted'], False)
        mock_blacklist_query.filter.assert_called_once()

if __name__ == '__main__':
    unittest.main()
