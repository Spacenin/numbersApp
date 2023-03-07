from twilio.rest import Client
import bible

#Send a message to a number
def sendMsg(content, number, secretData):
    #Setup connection
    client = Client(secretData["twilio"]["account_sid"], secretData["twilio"]["auth_token"])

    #Create message
    client.messages.create(
        body=content,
        from_=secretData["twilio"]["twi_number"],
        to="+1"+number
    )

#Send all messages
def sendAll(numbers, secretData):
    #Loop through all the numbers
    for number in numbers:
        #Message content array
        content = []

        #Get the apps they're subscribed to
        apps = number[1]

        #Bible
        if apps & 1:
            #Run Bible
            content.append(bible.runApp(secretData))

        #Recipe
        #if apps & 2:
            #Run recipe

        msg = "Good morning " + number[0] + "!\n\n"

        #Go through and create string for message
        for thingy in content:
            msg += thingy + "\n"

        msg += "Have a good day!"

        #Send the message
        sendMsg(msg, number[0], secretData)