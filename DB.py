import sqlite3

class DB:
    def save_score(nick, correct_ans, all_and, score):
        self.connection = sqlite3.connect('scores.db')
        self.cursor = connection.cursor()
        self.cursor.execute("INSERT INTO Scores (Nick, CorrectAns, AllAns, Score) VALUES ('bonek', 0, 10, 1)")
        self.connection.commit()
        self.connection.close()

    def p(self):
        self.connection = sqlite3.connect('scores.db')
        self.cursor = connection.cursor()
        for row in self.cursor.execute('SELECT * FROM scores.db ORDER BY CorrectAns, Score'):
            print row
        self.connection.close()

