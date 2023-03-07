import mysql.connector
from mysql.connector import Error

#Get connection to mysql database
def getConnection(secretData):
    connection = None

    #Create the connection
    try:
        connection = mysql.connector.connect(host=secretData["mysql"]["host"], user=secretData["mysql"]["user"], passwd=secretData["mysql"]["pass"], database=secretData["mysql"]["db"])
    
    except Error as err:
        print(f"Error: ' {err}'")
    
    return(connection)

#Get numbers as array
def getNumbers(secretData):
    #Create connection
    connection = getConnection(secretData)

    #If the connection worked
    if connection:
        cursor = connection.cursor()

        #Setup query
        query = "SELECT * FROM numbers"

        #Run query and parse results
        try:
            cursor.execute(query)
            resultSet = cursor.fetchall()

        except Error as err:
            print(f"Error: '{err}'")
            resultSet = None

        #Returned as array of tuples
        return(resultSet)
    #Otherwise, return nothing
    else:
        return(None)
