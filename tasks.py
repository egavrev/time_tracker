import psycopg2
from configparser import ConfigParser


class Tasks:
    def __init__(self, name, link, description, group_id, priority, status):
        self.name = name
        self.link = link
        self.description = description
        self.group_id = group_id
        self.priority = priority
        self.status = status

    def _database_connection(self):
        parser = ConfigParser()
        parser.read('database.ini')
        conn = psycopg2.connect(
            host=parser.get('postgresql', 'host'),
            database=parser.get('postgresql', 'database'),
            user=parser.get('postgresql', 'user'),
            password=parser.get('postgresql', 'password')
        )
        return conn

    def read_all_tasks(self):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return tasks

    def create_task(self):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (name, link, description, group_id, priority, status) VALUES (%s, %s, %s, %s, %s, %s)", (self.name, self.link, self.description, self.group_id, self.priority, self.status))
        conn.commit()
        cur.close()
        conn.close()

    def read_task(self, task_id):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        conn.close()
        return task

    def update_task_status(self, task_id, new_status):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status.value, task_id))
        conn.commit()
        cur.close()
        conn.close()

    def update_task_group(self, task_id, new_group_id):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET group_id = %s WHERE id = %s", (new_group_id, task_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_task(self, task_id):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()
        cur.close()
        conn.close()

    def filter_tasks(group_id, priority, status):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE group_id = %s AND priority = %s AND status = %s", (group_id, priority, status))
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return tasks
