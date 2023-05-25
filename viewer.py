import psycopg2
from configparser import ConfigParser
#calss which will return all data  to update progress on all events for all tasks on specific dates, for example weekly view.

class ProgressPerTime:
    def __init__(self, task_id=None, name=None,  link=None, description=None, group_id=None,  status=None, priority=None, progress_id=None,start_date_time=None,comment=None, end_date_time=None ):
        self.task_id = task_id
        self.name = name# tasks name 
        self.link = link# link to something 
        self.description = description# task descripiotn
        self.group_id = group_id# part of group id
        self.status = status
        self.priority = priority
        self.progress_id = progress_id#id of progres
        self.comment = comment# comment for priority 
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

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

    def view_tasks_progress(self, start_date_time, end_date_time):
        conn = self._database_connection()
        cur = conn.cursor()
        cur.execute("SELECT tasks.task_id,tasks.name,tasks.link, tasks.description, tasks.group_id, tasks.status,tasks.priority, progress.progress_id, progress.start_date_time, progress.end_date_time, progress.progress_time, progress.comments FROM tasks INNER JOIN progress ON tasks.task_id = progress.task_id  WHERE progress.start_date_time >= %s AND progress.end_date_time <= %s", (start_date_time, end_date_time))
        tasks_progress = cur.fetchall()
        cur.close()
        conn.close()
        return tasks_progress

