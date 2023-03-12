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
        mydb.commit()

        return(0)
    #Otherwise, update record
    else:
        #Check if already subscribed
        if app & results[0][0] == 0b000:
            updateQuery = "UPDATE numbers SET apps = " + str(results[0][0] + app) + \
                " WHERE number = \"" + number + "\";"
            mycursor.execute(updateQuery)
            mydb.commit()

            return(0)
        #Otherwise, print nothing done
        else:
            print(number + " is already subscribed to service " + str(app))

            return(-1)

#Unsubscribe from a specific app, subtracting from the user's app val in db
def unsub(number, app):
    #Check what is already there
    selectQuery = "SELECT apps FROM numbers WHERE number=\'" + number + "\';"

    #Get results
    mycursor.execute(selectQuery)
    results = mycursor.fetchall()

    numAppVal = results[0][0] 

    #If theyre not subbed tn anything, return error
    if numAppVal == 0:
        print(number + " is currently unsubscribed from everything")

        return(-1)
    else:
        #If you can unsub, unsub
        if numAppVal & app != 0:
            updateQuery = "UPDATE numbers SET apps = " + str(numAppVal - app) + \
                    " WHERE number = \"" + number + "\";"
            mycursor.execute(updateQuery)
            mydb.commit()

            return(0)
        #Otherwise, return error
        else:
            print(number + " is currently unsubscribed from service + " + str(app))

            return(-1)
    
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
    if re.search("^subscribe?", body, flags=re.IGNORECASE) != None:
        resp.message("Which application would you like to subscribe to? Respond with:\n" + \
                    "1. \'bible\' - send daily Bible verses\n" + \
                    "2. \'recipe\' - send daily recipes from a selection of websites")
    #If they want to sub to bibleApp
    elif re.search("^bible?", body, flags=re.IGNORECASE) != None:
        if sub(sender, 0b001) == 0:
            resp.message("You successfully subscribed to Bible! Hope you have a blessed day!")
        else:
            resp.message("Subscription failed.... are you already subscribed?")
    #If they want to sub to recipeApp
    elif re.search("^recipe?", body, flags=re.IGNORECASE) != None:
        if sub(sender, 0b010) == 0:
            resp.message("You successfully subscribed to recipe! Hope you enjoy!")
        else:
            resp.message("Subscription failed.... are you already subscribed?")
    #If they ask to unsubscribe
    elif re.search("^unsub?", body, flags=re.IGNORECASE) != None:
        resp.message("Which application would you like to unsubscribe from? Respond with:\n" + \
                    "1. \'unBible\'\n" + \
                    "2. \'unRecipe\'")
    #If they selected to unsub from bible
    elif re.search("^unBible?", body, flags=re.IGNORECASE) != None:
        if unsub(sender, 0b001) == 0:
            resp.message("You successfully unsubscribed from Bible! :(")
        else:
            resp.message("Unsub failed... were you even subscribed?")
    #If they selected to unsub from recipe
    elif re.search("^unRecipe?", body, flags=re.IGNORECASE) != None:
        if unsub(sender, 0b010) == 0:
            resp.message("You successfully unsubscribed from recipe! :(")
        else:
            resp.message("Unsub failed... were you even subscribed?")
    #If help message
    elif re.search("^help me?", body, flags=re.IGNORECASE) != None:
        resp.message("These are the available messages to send:\n" + \
                    "1. \'subscribe\' - subscribe to an application\n" + \
                    "2. \'unsub\' - unsubscribe from an application\n" + \
                    "3. \'help me\' - view this message")
    #If they say hello :)
    elif re.search("hello", body, flags=re.IGNORECASE) != None:
        resp.message("Hello! You can respond with the command \'help me\' to see what is available.")
    #Otherwise, give them an error msg
    else:
        resp.message("Invalid response! You may text \'help me\' to see available responses.")
    
    #Send back response
    return str(resp)

#Run the app on the public IP
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    mydb.close()
