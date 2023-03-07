import json
import db
import sms

#Basic run app function, called upon invoking the file
def run():
    #Setup secrets
    secretData = None

    #Open secrets file and store it into json
    with open("/home/pi/Code/numbersApp/numbersApp/secrets.json", "r") as secretsFile:
        secretData = json.load(secretsFile)

    #Get the numbers
    numbers = db.getNumbers(secretData)

    #Send them messages
    sms.sendAll(numbers, secretData)

#Run the app 
if __name__ == "__main__":
    run()