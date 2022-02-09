from dotenv import load_dotenv
import tweepy
import os
from test import quoteimage
import random

load_dotenv()
auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

api=tweepy.API(auth, wait_on_rate_limit=True)

bookpath="./libro.txt"
file = open(bookpath, "r", encoding="utf-8").read()
dot_indexes=[index for index, value in enumerate(file) if value == "."]
index=random.choice(dot_indexes)
quoteimage(file, index).save("image.png")

api.update_status_with_media("", filename="image.png")