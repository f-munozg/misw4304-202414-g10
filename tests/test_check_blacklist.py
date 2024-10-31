import unittest
from unittest.mock import patch, MagicMock
from flask import json
from flask_jwt_extended import create_access_token
from application import create_app
from models.models import db, Blacklist

class TestCheckBlacklist(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        # Se inicializa una base de datos inexistente para evitar errores de inicializar
        # REVISAR
        db.init_app(self.app)

        self.jwt_token = create_access_token(identity='test_user')

    def tearDown(self):
        self.app_context.pop()

    @patch('models.models.Blacklist.query')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_check_blacklist_success(self, mock_get_jwt_identity, mock_blacklist_query):
        mock_get_jwt_identity.return_value = 'test_user'
        
        mock_mail = MagicMock()
        mock_mail.blocked_reason = "spam"
        
        # Se configura el filtro y el valor a retornar
        mock_blacklist_query.filter.return_value.first.return_value = mock_mail

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={'Authorization': f'Bearer {self.jwt_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mail_blacklisted'], True)
        self.assertEqual(response.json['blacklist_reason'], "spam")
        
        # Se verifica que el filtro es llamado con el email correcto
        mock_blacklist_query.filter.assert_called_once()
        called_args = mock_blacklist_query.filter.call_args[0]

        # Se verifica que el argumento es una expresión válida de SQLAlchemy
        self.assertTrue(any(isinstance(arg, type(Blacklist.email == "test@example.com")) for arg in called_args))

    @patch('models.models.Blacklist.query')
    @patch('flask_jwt_extended.get_jwt_identity')
    def test_check_blacklist_email_not_found(self, mock_get_jwt_identity, mock_blacklist_query):
        mock_get_jwt_identity.return_value = 'test_user'
        
        # Se configura el valor a retornar como None
        mock_blacklist_query.filter.return_value.first.return_value = None

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={'Authorization': f'Bearer {self.jwt_token}'}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['mail_blacklisted'], False)
        
        # Se verifica que el filtro es llamado con el email correcto
        mock_blacklist_query.filter.assert_called_once()
        called_args = mock_blacklist_query.filter.call_args[0]

        # Se verifica que el argumento es una expresión válida de SQLAlchemy
        self.assertTrue(any(isinstance(arg, type(Blacklist.email == "test@example.com")) for arg in called_args))

if __name__ == '__main__':
    unittest.main()