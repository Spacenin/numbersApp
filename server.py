from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import re
import mysql.connector as mysql

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
    print(sender)

    #If subscribe message
    if re.search("subscribe", body, flags=re.IGNORECASE) != None:
        resp.message("Which application would you like to subscribe to? Respond with:\n" + \
                    "1. \'bible\' - send daily Bible verses\n" + \
                    "2. \'recipe\' - send daily recipes from a selection of websites\n" + \
                    "3. \'weather\' - send daily weather updates")
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

#Subscribe to a specific app, adding it to the mysql db
#def sub(number):
    
