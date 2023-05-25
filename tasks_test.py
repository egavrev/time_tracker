import unittest
from unittest.mock import patch, MagicMock


class TestTasks(unittest.TestCase):
    
    @patch('tasks.psycopg2.connect')
    def test_read_all_tasks(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 'Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE')]
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        tasks = Tasks('', '', '', 0, 0, '')
        result = tasks.read_all_tasks()
        
        self.assertEqual(result, [(1, 'Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE')])
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tasks")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('tasks.psycopg2.connect')
    def test_create_task(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        tasks = Tasks('Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE')
        tasks.create_task()
        
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO tasks (name, link, description, group_id, priority, status) VALUES (%s, %s, %s, %s, %s, %s)", ('Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE'))
        mock_connect.return_value.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('tasks.psycopg2.connect')
    def test_read_task(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 'Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE')
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        tasks = Tasks('', '', '', 0, 0, '')
        result = tasks.read_task(1)
        
        self.assertEqual(result, (1, 'Task 1', 'https://task1.com', 'Description of task 1', 1, 1, 'INCOMPLETE'))
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tasks WHERE task_id = %s", (1,))
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('tasks.psycopg2.connect')
    def test_update_task_status(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        tasks = Tasks('', '', '', 0, 0, '')
        tasks.update_task_status(1, Status.IN_PROGRESS)
        
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("UPDATE tasks SET status = %s WHERE id = %s", ('IN_PROGRESS', 1))
        mock_connect.return_value.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()
