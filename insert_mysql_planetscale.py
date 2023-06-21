import sys
import config
from dotenv import load_dotenv
import os
from mysql.connector import Error
import mysql.connector

load_dotenv()

def insert_sql_planetscale(result):
    connection = mysql.connector.connect(
        host = config.PS_HOST ,
        database = config.PS_DATABASE,
        user = config.PS_USERNAME,
        passwd = config.PS_PASSWORD 
    )



    try:
        if connection.is_connected():
            cursor = connection.cursor()
        insert_statement = '''
                INSERT INTO Cijene 
                (WebMjestoId, TrgovinaId, datum, Poveznica, Kategorija, Sifra, Naziv, Cijena) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''

        for r in result:
            cursor.execute(insert_statement, r)

        print(f'{len(result)} records inserted successfully')

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        connection.close()
