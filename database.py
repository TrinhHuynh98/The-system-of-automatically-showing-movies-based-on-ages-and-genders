import sqlite3
from sqlite3 import Error
DATABASE_FILE = r"movie_database.db"
import os
class DB:
    def __init__(self):
        self.conn = None
    def connect(self):
        """ create a database connection to a SQLite database """
        try:
            if os.path.exists(DATABASE_FILE):
                self.conn = sqlite3.connect(DATABASE_FILE)
            else:
                self.create_table() 
        except Error as e:
            print(e)

    def create_table(self):
        try:
            query = '''CREATE TABLE movie (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name text NOT NULL,
                movie_gender text NOT NULL,
                movie_age_from INTEGER NOT NULL,
                movie_age_to INTEGER NOT NULL,
                movie_image text NOT NULL
            );'''
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)

    def add_movie(self,image,name,gender,age_from,age_to):
        query = """INSERT INTO movie (movie_image,movie_name,movie_gender,movie_age_from,movie_age_to)
        VALUES ('{}','{}','{}',{},{})""".format(image,name,gender,age_from,age_to)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error:", error)

    def update_movie(self,id,image,name,gender,age_from,age_to):
        query = """UPDATE movie SET movie_image='{}',movie_name = '{}',
        movie_gender ='{}', movie_age_from = {}, movie_age_to={}
        WHERE movie_id = {}""".format(image,name,gender,age_from,age_to,id)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error:", error)

    def delete_movie(self,id):
        query = """DELETE FROM movie WHERE movie_id={}""".format(id)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error:", error)

    def get_movie_by_id(self,id):
            query = "SELECT * FROM movie WHERE movie_id={}".format(id)
            result = []
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                result =  cursor.fetchone()
                cursor.close()
                return result
            except sqlite3.Error as error:
                print("Error:", error)
    def get_all_movie(self):
            query = "SELECT * FROM movie"
            result = []
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                result =  cursor.fetchall()
                cursor.close()
                return result
            except sqlite3.Error as error:
                print("Error:", error)

    def get_movie_by_age_and_gender(self,age,gender):
        if gender == 1:
            gender = "male"
        else:
            gender = "female"
            

        query = "SELECT * FROM movie where movie_age_from <= {} and movie_age_to >= {} and (movie_gender = \'{}\' or movie_gender = 'both') ".format(int(age),int(age),gender)
        result = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result =  cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as error:
            print("Error:", error)

    def close(self):
        self.conn.close()
