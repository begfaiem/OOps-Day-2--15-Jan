import logging
import mysql.connector as conn
import csv

# Configuring logging to write to a file named "sql_bulk_upload.log"
# Setting the logging level to DEBUG
# Using filemode 'w' to overwrite the log file if it exists
# The log message format includes timestamp, log level, and the actual log message
logging.basicConfig(filename="sql_bulk_upload.log", level=logging.DEBUG, filemode='w', format="% (asctime)s %(levelname)s %(message)s")

# Defining a class named MySQL_Bulk_Upload
class MySQL_Bulk_Upload():

    # Constructor method to initialize the class with connection details
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
     
    # Method to create a connection to the MySQL database
    def create_connection(self):
        try:
            # Establishing a connection using the provided credentials
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
            cursor = mydb.cursor()

            # Storing the connection and cursor as class attributes
            self.mydb = mydb
            self.cursor = cursor

            # Logging and printing a success message
            logging.info("Connection to DB successful")
            print("Connection to DB successful")
        except Exception as e:
            # Logging and printing an error message if an exception occurs
            logging.error("Exception occurred", e)
    
    # Method to create a table in the database
    def create_table(self, table_name, columns):
        try:

            # Storing table name and columns as class attributes
            self.table_name = table_name
            self.columns = columns

            # Executing SQL query to create a table (if not exists)
            self.cursor.execute(f"CREATE TABLE if not exists {self.table_name}({self.columns})")
            
            # Committing the changes to the database
            self.mydb.commit()

            # Logging and printing a success message
            logging.info("Table has created")
            print("Table has created")
        except Exception as e:
            # Logging and printing an error message if an exception occurs
            logging.error("Exception occurred", e)

    # Method to insert data into the created table from a CSV file
    def insert_data(self, csv_file):
        try:
            with open(csv_file, "r") as f:
                # Reading CSV data using csv.reader
                data = csv.reader(f, delimiter='\n')

                # Skipping the header row
                next(data)

                # Iterating through rows and executing SQL insert queries
                for i in data:
                    self.cursor.execute(f'insert into {self.database}.{self.table_name} values({str(i[0])})')
            
            # Committing the changes to the database
            self.mydb.commit()

            # Logging a success message
            logging.info("Bulk Upload is successful")

        except Exception as e:
             # Printing the exception and logging an error message
            print(e)
            logging.error("Exception occurred", e)

    # Method to retrieve and display data from the created table
    def show_data(self):
        try:
            # Executing SQL query to select all data from the table
            self.cursor.execute(f"SELECT * from {self.table_name}")

            # Logging a success message
            logging.info("Showing Data from table is successful")

            # Printing the fetched data
            print(self.cursor.fetchall())
        except Exception as e:
            # Logging and printing an error message if an exception occurs
            logging.error("Exception occurred", e)

# Creating an instance of the MySQL_Bulk_Upload class
obj = MySQL_Bulk_Upload("localhost", "abc", "password", "ineuronq4")

# Calling methods to perform database operations
obj.create_connection()
obj.create_table("glassdata2", "col1 INT(10), col2 float(30,10), col3 float(30,10), col4 float(30,10), col5 float(30,10), col6 float(30,10), col7 float(30,10), col8 float(30,10), col9 float(30,10), col10 float(30,10), col11 INT(10)")
obj.insert_data("glass.data")
obj.show_data()