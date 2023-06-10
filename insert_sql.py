import sys
import pyodbc as odbc
import config

# config contains sensitive data, hence it's hidden

def insert_sql(result):
    server = config.server
    database = config.database
    username = config.username
    password = config.password

    conn_str =  f'DRIVER={{ODBC Driver 17 for SQL Server}};' \
                f'SERVER={server};' \
                f'DATABASE={database};' \
                f'UID={username};' \
                f'PWD={{{password}}};'

    try:
        conn = odbc.connect(conn_str)
        cursor = conn.cursor()

        insert_statement = '''
            INSERT INTO Cijene 
            (WebMjestoId, TrgovinaId, datum, Poveznica, Kategorija, Sifra, Naziv, Cijena) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''  # noqa: E501

        for r in result:
            cursor.execute(insert_statement, r)

        print(f'{len(result)} records inserted successfully')
        cursor.commit()
    except Exception as e:
        if 'cursor' in locals():
            cursor.rollback()
        print(e)
        print('Task is terminated')
        sys.exit()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()