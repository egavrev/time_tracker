import psycopg2
from configparser import ConfigParser

class Progress:
    def __init__(self, task_id=None, start_date_time=None, end_date_time=None, progress_time=None, comments=None):
        self.task_id= task_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.progress_time = progress_time
        self.comments = comments

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

    def create_progress(self):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO progress (task_id, start_date_time, end_date_time, progress_time, comments) VALUES (%s, %s, %s, %s, %s)", (self.task_id,self.start_date_time, self.end_date_time, self.progress_time, self.comments))
        conn.commit()
        cur.close()
        conn.close()

    def read_progress(self, progress_id):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM progress WHERE progress_id = %s", (progress_id,))
        progress = cur.fetchone()
        cur.close()
        conn.close()
        return progress

    def update_progress(self, progress_id, start_date_time, end_date_time, progress_time, comments):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("UPDATE progress SET start_date_time = %s, end_date_time = %s, progress_time = %s, comments = %s WHERE progress_id = %s", (start_date_time, end_date_time, progress_time, comments, progress_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_progress(self, progress_id):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM progress WHERE progress_id = %s", (progress_id,))
        conn.commit()
        cur.close()
        conn.close()