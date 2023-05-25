import unittest
from unittest.mock import patch, MagicMock
from flask import Flask


class TestTasks(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        
        
    def test_get_all_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn('tasks', data)
        self.assertIsInstance(data['tasks'], list)
        for task in data['tasks']:
            self.assertTrue('name' in task)
            self.assertTrue('link' in task)
            self.assertTrue('description' in task)
            self.assertTrue('group_id' in task)
            self.assertTrue('priority' in task)
            self.assertTrue('status' in task)