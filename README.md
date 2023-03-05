# numbersApp
This repo stores the files for both server (EC2) and client (pi) sides of the numbersApp, which allows users to subscribe to daily text message applications I have written.
The EC2 instance catches all sent messages, and deals with them correspondingly in the database, which is also hosted on the EC2 instance. The database stores name, number, and apps as a binary value, which is edited by sending messages to the server. The raspberry pi then retrieves all values in the database, and every morning at 7 AM, sends the messages to those who have set to recieve them. 
