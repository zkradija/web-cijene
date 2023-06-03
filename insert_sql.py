import sys
import pyodbc as odbc
import config_test

def insert_sql(result):
    server = config_test.server
    database = config_test.database
    username = config_test.username
    password = config_test.password

    conn_str =  f'DRIVER={{ODBC Driver 17 for SQL Server}};' \
                f'SERVER={server};' \
                f'DATABASE={database};' \
                f'UID={username};' \
                f'PWD={{{password}}};'
    conn = odbc.connect(conn_str)
    cursor = conn.cursor()

    try:
        conn = odbc.connect(conn_str)
    except Exception as e:
        print(e)
        print('Task is terminated')
        sys.exit
    else:
        cursor = conn.cursor()

    insert_statement = '''
        insert into Cijene 
        (WebMjestoId,TrgovinaId,datum,Poveznica,Kategorija,Sifra,Naziv,Cijena,GtinKom) 
        values (?,?,?,?,?,?,?,?,?)
        '''

    try:
        for r in result:
            cursor.execute(insert_statement, r)
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print('Transaction rolled back')
    else:
        print(f'{len(result)} records inserted successfully')
        cursor.commit()
        cursor.close()
