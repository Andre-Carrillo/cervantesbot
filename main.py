from Twitter import Twitter
import time

bookpath="./textfiles/libro.txt"
file = open(bookpath, "r", encoding="utf-8").read()
Bot = Twitter(file)
def main(hours):
    counter=0
    while counter<hours*360:
        mentions_dictionary = Bot.getmentions()
        for id, command in mentions_dictionary.item():
            Bot.answermention(id, command)
        time.sleep(10)
        counter+=1
if __name__=="__main__":
    main(4)