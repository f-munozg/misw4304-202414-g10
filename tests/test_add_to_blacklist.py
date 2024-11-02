import unittest
import os
from unittest.mock import patch, MagicMock
from flask import json
from flask_jwt_extended import create_access_token
from application import create_app
from sqlalchemy.exc import IntegrityError

class TestAddToBlacklist(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'true' 
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.jwt_token = create_access_token(identity='test_user')

    def tearDown(self):
        self.app_context.pop()

    @patch('models.models.db.session')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_add_to_blacklist_success(self, mock_get_jwt_identity, mock_db_session):
        mock_get_jwt_identity.return_value = 'test_user'
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        response = self.client.post(
            '/blacklists',
            headers={'Authorization': f'Bearer {self.jwt_token}'},
            data=json.dumps({
                "email": "test@example.com",
                "app_uuid": "12345-uuid",
                "blocked_reason": "spam"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], "Account created")
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('models.models.db.session')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_add_to_blacklist_email_already_exists(self, mock_get_jwt_identity, mock_db_session):
        mock_get_jwt_identity.return_value = 'test_user'
        mock_db_session.add = MagicMock()
        mock_db_session.commit.side_effect = IntegrityError('test', 'test', 'test')

        response = self.client.post(
            '/blacklists',
            headers={'Authorization': f'Bearer {self.jwt_token}'},
            data=json.dumps({
                "email": "test@example.com",
                "app_uuid": "12345-uuid",
                "blocked_reason": "spam"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['message'], "Email is already blacklisted")
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()