import mysql.connector

# Establish a connection to the database
cnx = mysql.connector.connect(user='root', password='PogodiMe123',
                              host='localhost', port='3306', database='web_cijene')

# Create a cursor object
cursor = cnx.cursor()

# Execute a query
query = "SELECT * FROM web_cijene.cijene"
cursor.execute(query)

# Fetch the results
for result in cursor:
    print(result)

# Close the cursor and connection
cursor.close()
cnx.close()