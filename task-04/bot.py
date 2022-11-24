import os
from dotenv import load_dotenv
import telebot
import requests
import json
import csv

# Get your environment variables 
load_dotenv()
YOURKEY= os.getenv('YOURKEY')
APIKEY = os.getenv('APIKEY')

bot = telebot.TeleBot(APIKEY)

fout = open("moviesearch.csv",'w')
csvwriter = csv.writer(fout)
csvwriter.writerow(['Title','Year','imdbRating'])
fout.close()


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    bot.reply_to(
        message, 'Hello there! I am a bot that will show movie information for you and export it in a CSV file.\n\n')
    
@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nHave a good time')
    


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/movie MOVIE_NAME\" command to get the details of a particular movie. For eg: \"/movie The Shawshank Redemption\"\n\n2.0. You can use \"/export\" command to export all the movie data in CSV format.\n\n3.0. You can use \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['movie'])
def getMovie(message):
    bot.reply_to(message, 'Getting movie info...')
    
    # Get movie information from the API
    texts = message.text.split()
    movie_name = '+'.join(texts[1:])
    url = "http://www.omdbapi.com/?i=tt3896198&apikey={YOURKEY}&t={movie_name}".format(YOURKEY=YOURKEY,movie_name = movie_name)
    r = requests.get(url)
    data = json.loads(r.text)
    
    #Show the movie information in the chat window
    movie_title = data["Title"]
    year_of_release = data["Year"]
    imdb_rating = data["imdbRating"]
    bot.reply_to(message, 'Title : {movie_title} \n Year : {year_of_release} \n imdbRating : {imdb_rating} \n'.format(movie_title=movie_title,year_of_release=year_of_release,imdb_rating=imdb_rating))
    # TODO: 2.1 Create a CSV file and dump the movie information in it
    filename = "moviesearch.csv"
    with open(filename, 'a') as csvfile:
    	csvwriter = csv.writer(csvfile)
    	csvwriter.writerow([movie_title,year_of_release,imdb_rating])

  
@bot.message_handler(func=lambda message: botRunning, commands=['export'])
def getList(message):
    bot.reply_to(message, 'Generating file...')
    #Send downlodable CSV file to telegram chat
    doc = open('moviesearch.csv','r')
    bot.send_document(message.chat.id,doc)

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    
bot.infinity_polling()
