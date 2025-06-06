import mysql.connector
import psycopg2


class Connection:
    def connectPost(self):
        # return psycopg2.connect("dbname=postgres host=localhost user=postgres port=5432 password=Post@007007" )
        return None


    def connectMysql(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sq@007007",
                database="MyFoodGRS",
            )
            return mydb
        except mysql.OperationalError:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sq@007007",
                database="MyFoodGRS",
            )