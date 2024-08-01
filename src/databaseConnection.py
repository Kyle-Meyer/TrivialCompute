import psycopg2
import json

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

    def executeQueryInsert(self, query, params=None):
        if not self.conn:
            self.connect()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()  # Commit the transaction
        except Exception as e:
            self.conn.rollback()  # Rollback in case of error
            print(f"An error occurred: {e}")             

    def getQuestionAndAnswerByCategory(self, category):
        query = "SELECT question, answer FROM questions WHERE category = %s ORDER BY RANDOM() LIMIT 1"
        params = (category,)
        return self.executeQueryFetchOne(query, params)
    
    def getQuestionAndAnswerByCategories(self, categories):
        placeholders = ', '.join(['%s' for _ in categories])
        query = f"SELECT question, answer FROM questions WHERE category IN ({placeholders}) ORDER BY RANDOM() LIMIT 1"
        return self.executeQueryFetchOne(query, categories)

    def getRandomQuestionAndAnswer(self):
        query = "SELECT question, answer FROM questions ORDER BY RANDOM() LIMIT 1"
        return self.executeQueryFetchOne(query)       
    
    def getCategories(self):
        query = "SELECT id, name FROM categories"
        return self.executeQueryFetchAll(query)

    def getPlayerPositionsOfLastSavedGame(self):
        query = "SELECT \"playerPositions\" FROM saved_game_states ORDER BY date DESC"
        return self.executeQueryFetchOne(query)

    def saveCurrentGameState(self, playerList, currPlayer, playerOrder):
        count = 0

        # Initialize dictionary
        player_position_data = {}

        # Populate dictionary with incrementing count
        for player in playerList:
            player_position_data[f'player{count}'] = player.currCoordinate
            count += 1

        # Convert the dictionary to a JSON string
        json_player_position_data = json.dumps(player_position_data)
        
        #TODO format currPlayer and playerOrder and use those values in the insert statement instead of the test values
        
        query = "INSERT INTO saved_game_states (\"playerPositions\", \"playerScores\", \"playerOrder\", \"currentPlayer\", \"date\") VALUES (%s , %s, %s, %s, current_timestamp)"
        params = (json_player_position_data, [], [], 'testCurrPlayer',)
        return self.executeQueryInsert(query, params)
