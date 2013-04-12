import MySQLdb

class ConnectionManager:
    def __enter__(self):
        self._conn = self._get_conn()
        return self._conn

    def __exit__(self, ex_type, ex_value, trace):
        self._conn.close()

    def _get_conn(self):
        host = 'localhost'
        user = 'music'
        passwd = 'music'
        db = 'music'
        return MySQLdb.connect(host, user, passwd, db)
