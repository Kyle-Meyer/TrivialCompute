import psycopg2

class databaseConnection(object):
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def executeQueryFetchAll(self, query, params=None):
        if not self.conn:
            self.connect()

        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def executeQueryFetchOne(self, query, params=None):
        if not self.conn:
            self.connect()

        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()        

    def getQuestionAndAnswerByCategory(self, category):
        query = "SELECT question, answer FROM questions WHERE category = %s ORDER BY RANDOM() LIMIT 1"
        params = (category,)
        return self.executeQueryFetchOne(query, params)

    def getRandomQuestionAndAnswer(self):
        query = "SELECT question, answer FROM questions ORDER BY RANDOM() LIMIT 1"
        return self.executeQueryFetchOne(query)       