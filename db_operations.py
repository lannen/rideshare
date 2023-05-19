import sqlite3

# import MySQL
import mysql.connector

class db_operations():

    #constructor with connection path to database
    def __init__(self, conn_path):
        self.connection = mysql.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("* connection made...")

    # create users with all attributes
    # def create_user_table(self):
    #     query = '''
    #     CREATE TABLE user(
    #         userID INT NOT NULL PRIMARY KEY,
    #         driver_rider VARCHAR(40) NOT NULL,
    #         pick_up VARCHAR(40) NOT NULL,
    #         drop_off VARCHAR(40) NOT NULL
    #         );
    #     '''

    #     # table created
    #     self.cursor.execute(query)
    #     print("* user table created")

    # # create users with all attributes
    # def create_driver_table(self):
    #     query = '''
    #     CREATE TABLE driver(
    #         driverID INT NOT NULL PRIMARY KEY,
    #         Rating VARCHAR(40) NOT NULL,
    #         Rides VARCHAR(40) NOT NULL,
    #         Activate_Deactivate VARCHAR(40) NOT NULL
    #         );
    #     '''

    #     # table created
    #     self.cursor.execute(query)
    #     print("* driver table created")

    # def create_ride_table(self):
    #     query = '''
    #     CREATE TABLE driver(
    #         rideID INT NOT NULL PRIMARY KEY,
    #         driverID INT NOT NULL FOREIGN KEY FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
    #         userID INT NOT NULL FOREIGN KEY
    #         );
    #     '''

    #     # table created
    #     self.cursor.execute(query)
    #     print("* ride table created")

    # function to retrieve a single value from a table
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    # function to bulk insert records
    def bulk_insert(self, query, records):
        self.cursor.executemany(query, records)
        self.connection.commit()
        print("* query executed...")

    # function that returns the values of a single attribute
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        # results.remove(None)      # causing error bc no Null values
        return results

    # function that returns only first value with a placeholder in query
    def name_placeholder_query(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # function that returns all values with a placeholder in query
    def name_placeholder_queries(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        return results

    # destructor that closes connection to database
    def destructor(self):
        self.connection.close()
