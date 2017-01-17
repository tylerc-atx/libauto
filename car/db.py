import sqlite3


class KeyValueStore(object):

    CREATE_TABLE = '''
        CREATE TABLE IF NOT EXISTS key_value_store (
            k BLOB PRIMARY KEY,
            v BLOB
        )
    '''

    def __init__(self, db_file_path, same_thread=False):
        self.db_file_path = db_file_path
        self.db = None
        self.first = True
        if same_thread:
            self.db = self.get_db()

    def get_db(self):
        if self.db:
            return self.db
        else:
            db = sqlite3.connect(self.db_file_path)
            if self.first:
                db.execute(KeyValueStore.CREATE_TABLE)
                db.commit()
                self.first = False
            return db

    def get(self, key, default_value=None):
        query = 'SELECT v FROM key_value_store WHERE k=?'
        db = self.get_db()
        cur = db.execute(query, (key, ))
        rv = cur.fetchall()
        value = rv[0][0] if rv else default_value
        cur.close()
        db.commit()
        return value

    def put(self, key, value):
        query = 'INSERT OR REPLACE INTO key_value_store (k, v) VALUES (?, ?)'
        db = self.get_db()
        cur = db.execute(query, (key, value))
        c = cur.rowcount
        cur.close()
        db.commit()
        return c

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.put(key, value)

