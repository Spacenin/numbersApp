import re
import requests
import random

#Base url for the API
bibleUrl = "https://api.scripture.api.bible/v1/bibles/"
#ID of the Bible we want, specifically the American Standard Version
bibleId = "06125adad2d5898a-01"

#Get Bible verse and parse it out
def getVerse(apiKey):
    #Get books of the bible
    bookList = requests.get(bibleUrl+bibleId+"/books", headers={"api-key":apiKey}).json()["data"]
    
    #Create book ID list from that list
    bookIDList = []

    for book in bookList:
        bookIDList.append(book["id"])
    
    #Select random book from that list
    bookSelected = random.choice(bookIDList)

    #Get chapters for that book
    chapterList = requests.get(bibleUrl+bibleId+"/books/"+bookSelected+"/chapters", headers={"api-key":apiKey}).json()["data"]

    #Create chapter ID list from that list
    chapterIDList = []

    for chapter in chapterList:
        chapterIDList.append(chapter["id"])

    #Select random chapter from that list
    chapterSelected = random.choice(chapterIDList)

    #Get verses for that chapter
    verseList = requests.get(bibleUrl+bibleId+"/chapters/"+chapterSelected+"/verses", headers={"api-key":apiKey}).json()["data"]

    #Create list of verse IDs
    verseIDList = []

    for verse in verseList:
        verseIDList.append(verse["id"])
    
    #Select random verse from that list
    verseSelected = random.choice(verseIDList)

    #Make sure we don't get the intro verse
    while (re.search("intro", verseSelected) != None):
        verseSelected = random.choice(verseIDList)

    #Get that verse and return it
    verseText = requests.get(bibleUrl+bibleId+"/verses/"+verseSelected, headers={"api-key":apiKey}).json()["data"]["content"]

    #Create verse object to return
    verseObj = {
        "title": verseSelected,
        "text": re.search("(?<=<\/span>).*?(?=<\/p>)", verseText).group()
    }

    #Return only the verse content, not the weird HTML stuff
    return(verseObj)

#Run the app :)
def runApp(secretData):
    verse = getVerse(secretData["bible"]["api_key"])

    #Create verse as string
    verseString = "Here is youur daily Bible verse: \n" + verse["title"] + "\n" + verse["text"] + "\n"
    
    return(verseString)