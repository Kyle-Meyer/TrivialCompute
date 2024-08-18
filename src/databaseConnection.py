import psycopg2
import json
from colors import *

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
        query = "SELECT id, question, answer, \"imageBase64\" FROM questions WHERE category = %s ORDER BY RANDOM() LIMIT 1"
        params = (category,)
        return self.executeQueryFetchOne(query, params)

    def getQuestionAndAnswerByCategoryThatWasntAlreadyAsked(self, category, askedQuestionsInCategory):
        if askedQuestionsInCategory == [] or askedQuestionsInCategory == None:
            return self.getQuestionAndAnswerByCategory(category)
        else:
            query = "SELECT id, question, answer, \"imageBase64\" FROM questions WHERE category = %s AND id NOT IN %s ORDER BY RANDOM() LIMIT 1"
            params = (category, tuple(askedQuestionsInCategory))
            return self.executeQueryFetchOne(query, params)  
    
    # def getQuestionAndAnswerByCategories(self, categories):
    #     placeholders = ', '.join(['%s' for _ in categories])
    #     query = f"SELECT question, answer, \"imageBase64\" FROM questions WHERE category IN ({placeholders}) ORDER BY RANDOM() LIMIT 1"
    #     return self.executeQueryFetchOne(query, categories)
    
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

    def getGameStateOfLastSavedGame(self):
        query = "SELECT * FROM saved_game_states ORDER BY date DESC"
        return self.executeQueryFetchOne(query)

    def saveCurrentGameState(self, playerList, setupInfo, currPlayerIndex):

        # Initialize dictionaries
        player_position_data = {}
        player_score_data = {}
        player_report_card_data = {}

        count = 0
        # Populate dictionaries with incrementing player count
        for player in playerList:
            player_position_data[f'player{count}'] = player.currCoordinate
            player_score_data[f'player{count}'] = player.playerScore
            print(player.playerReportCard)
            player_report_card_data[f'player{count}'] = self.convertTupleKeysToStringsAndTupleValuesToList(player.playerReportCard)
            count += 1

        # Convert the dictionary to a JSON string
        json_player_position_data = json.dumps(player_position_data)
        json_player_score_data = json.dumps(player_score_data)
        json_player_report_card_data = json.dumps(player_report_card_data)
        json_setupInfo = json.dumps(setupInfo)

        query = "INSERT INTO saved_game_states (\"playerPositions\", \"playerScores\", \"playerReportCards\", \"setupInfo\", \"currentPlayerIndex\", \"date\") VALUES (%s , %s, %s, %s, %s, current_timestamp)"
        params = (json_player_position_data, json_player_score_data, json_player_report_card_data, json_setupInfo, currPlayerIndex)
        return self.executeQueryInsert(query, params)

    def convertTupleKeysToStringsAndTupleValuesToList(self, dictionaryToConvert):
        new_dict = {}
        for key, value in dictionaryToConvert.items():
            # Convert the key from a tuple to a string if it's a tuple
            if isinstance(key, tuple):
                key = str(key)  # Convert tuple to its string representation
            # Recursively process nested dictionaries and lists
            if isinstance(value, dict):
                value = convert_tuple_keys_to_strings(value)
            elif isinstance(value, list):
                value = [convert_tuple_keys_to_strings(item) if isinstance(item, dict) else item for item in value]
            new_dict[key] = value
        return new_dict

    def getQuestionAndAnswerById(self, id):
        query = "SELECT question, answer, \"imageBase64\" FROM questions WHERE id = %s"
        params = (id,)
        return self.executeQueryFetchOne(query, params)

    def savePlayerGrades(self, playerList, setupInfo):
        for player in playerList:
            for category in setupInfo['categories']:
                gradeForCategory = 0
                if category['color'] == match_red:
                    if player.playerReportCard[match_red][1] == 0:
                        gradeForCategory = 0
                    else:    
                        gradeForCategory = (player.playerReportCard[match_red][0] / player.playerReportCard[match_red][1]) * 100
                elif category['color'] == match_blue:
                    if player.playerReportCard[match_blue][1] == 0:
                        gradeForCategory = 0
                    else:
                        gradeForCategory = (player.playerReportCard[match_blue][0] / player.playerReportCard[match_blue][1]) * 100
                elif category['color'] == match_green:
                    if player.playerReportCard[match_green][1] == 0:
                        gradeForCategory = 0
                    else:    
                        gradeForCategory = (player.playerReportCard[match_green][0] / player.playerReportCard[match_green][1]) * 100
                else:
                    if player.playerReportCard[match_yellow][1] == 0:
                        gradeForCategory = 0
                    else:    
                        gradeForCategory = (player.playerReportCard[match_yellow][0] / player.playerReportCard[match_yellow][1]) * 100

                query = "INSERT INTO player_grades (\"name\", \"category\", \"grade\", \"date\") VALUES (%s , %s, %s, current_timestamp)"

                params = (player.playerName, category['name'], gradeForCategory)
                self.executeQueryInsert(query, params) 
        return