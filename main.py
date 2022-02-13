from twitter import Twitter
import time


def main(hours):
    counter=0
    while counter<hours*360:
        mentions_dictionary = Bot.get_mentions()
        for id, command in mentions_dictionary.items():
            Bot.answer_mention(id, command)
        time.sleep(10)
        counter+=1

        
if __name__=="__main__":
    bookpath="./textfiles/libro.txt"
    print("Starting bot ...")
    with open(bookpath, "r", encoding="utf-8") as file:
        Bot = Twitter(file)
        main(4)