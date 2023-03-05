from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import re
import mysql.connector
import json

#Creds to use for mysql connection
sqlhost = ""
sqluser = ""
sqlpassword = ""
sqldatabase = ""

#Get mysql creds
with open("secrets.json", "r") as file:
    creds = json.load(file)
    sqlhost = creds["host"]
    sqluser = creds["user"]
    sqlpassword = creds["password"]
    sqldatabase = creds["database"]

#Connect to db
mydb = mysql.connector.connect(host=sqlhost, user=sqluser, passwd=sqlpassword, database=sqldatabase)

mycursor = mydb.cursor()

#Subscribe to a specific app, adding it to the mysql db
def sub(number, app):
    #Check what they already are in
    selectQuery = "SELECT apps FROM numbers WHERE number=\'" + number + "\';"
    
    #Get results
    mycursor.execute(selectQuery)
    results = mycursor.fetchall()
    
    #If not already in the database, insert
    if not results:
        insertQuery = "INSERT INTO numbers (number, apps) VALUES (\"" + \
                number + "\", " + str(app) + ");"
        
        mycursor.execute(insertQuery)
        dbcursor.commit()
    #Otherwise, update record
    else:
        #Check if already subscribed
        if app & results[0][0] == 0b000:
            updateQuery = "UPDATE numbers SET apps = " + str(results[0][0] + app) + \
                " WHERE number = \"" + number + "\";"
            mycursor.execute(updateQuery)
            mydb.commit()
        #Otherwise, print nothing done
        else:
            print(number + " is already subscribed to service " + str(app))
    
#Flask app
app = Flask(__name__)

#sms http route, use either GET or POST
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    #Start our TwiML response
    resp = MessagingResponse()

    #Get body of message
    body = request.values.get('Body', None)
    
    #Get the phone number of sender
    sender = request.values.get('From', None)
    sender = sender.replace("+1", "")

    #If subscribe message
    if re.search("subscribe", body, flags=re.IGNORECASE) != None:
        resp.message("Which application would you like to subscribe to? Respond with:\n" + \
                    "1. \'bible\' - send daily Bible verses\n" + \
                    "2. \'recipe\' - send daily recipes from a selection of websites\n" + \
                    "3. \'weather\' - send daily weather updates")
    #If they want to sub to bibleApp
    elif re.search("bible", body, flags=re.IGNORECASE) != None:
        sub(sender, 0b001)
    #If they want to sub to recipeApp
    elif re.search("recipe", body, flags=re.IGNORECASE) != None:
        sub(sender, 0b010)
    #If they want to sub to weather
    elif re.search("weather", body, flags=re.IGNORECASE) != None:
        sub(sender, 0b100)
    #If help message
    elif re.search("help me", body, flags=re.IGNORECASE) != None:
        resp.message("These are the available messages to send:\n" + \
                    "1. \'subscribe\' - subscribe to an application\n" + \
                    "2. \'unsub\' - unsubscribe from an application\n" + \
                    "3. \'help me\' - view this message")
    #Otherwise, give them an error msg
    else:
        resp.message("Invalid response! You may text \'help me\' to see available responses.")
    
    #Send back response
    return str(resp)

#Run the app on the public IP
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    mydb.close()
