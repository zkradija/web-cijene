import sys
import pyodbc as odbc
import config

def insert_SQL(result):
    server = config.server
    database = config.database
    username = config.username
    password = config.password

    conn_str =  f'SERVER={server};' \
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
        insert into cijene 
        (WebMjestoId,TrgovinaId,datum,poveznica,kategorija,sifra,naziv,cijena) 
        values (?,?,?,?,?,?,?,?)
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

if __name__ == '__main__':
    insert_SQL()