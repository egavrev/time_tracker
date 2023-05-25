import psycopg2

class Groups:
    def __init__(self, group_name, description):
        self.group_name = group_name
        self.description = description

    def create_group(self):
        conn = psycopg2.connect(
            host="localhost",
            database="database_name",
            user="database_user",
            password="database_password"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO groups (group_name, description) VALUES (%s, %s)", (self.group_name, self.description))
        conn.commit()
        cur.close()
        conn.close()

    def read_group(self, group_id):
        conn = psycopg2.connect(
            host="localhost",
            database="database_name",
            user="database_user",
            password="database_password"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM groups WHERE id = %s", (group_id,))
        group = cur.fetchone()
        cur.close()
        conn.close()
        return group

    def update_group(self, group_id, group_name, description):
        conn = psycopg2.connect(
            host="localhost",
            database="database_name",
            user="database_user",
            password="database_password"
        )
        cur = conn.cursor()
        cur.execute("UPDATE groups SET group_name = %s, description = %s WHERE id = %s", (group_name, description, group_id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_group(self, group_id):
        conn = psycopg2.connect(
            host="localhost",
            database="database_name",
            user="database_user",
            password="database_password"
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM groups WHERE id = %s", (group_id,))
        conn.commit()
        cur.close()
        conn.close()