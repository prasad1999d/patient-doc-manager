import os
import unittest
import tempfile
import json
from app import app, init_db, DB_PATH

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Ensure test DB is initialized
        init_db()

        # Login to get token
        response = self.client.post('/login', json={'user': 'testuser'})
        self.token = json.loads(response.data)['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(DB_PATH)

    def test_login_success(self):
        response = self.client.post('/login', json={'user': 'tester'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_document_list_empty(self):
        response = self.client.get('/documents', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_upload_without_file(self):
        response = self.client.post('/documents/upload', data={'patient_id': 'p123'}, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
