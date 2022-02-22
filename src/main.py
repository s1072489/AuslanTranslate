# Importing required libraries
import requests
import os
from bs4 import BeautifulSoup

# Variables
URL = "https://www.auslan.org.au/dictionary/"


# Main
def Auslan(text: str):
    sentence = text.lower().split(" ") # Clean sentence
    returned = [] # List for results
    num = -1 # Numbering for files

    # Getting stuff
    for query in sentence:
        num += 1 # Start number = 0

        # Getting page
        page = requests.get(f"{URL}search?query={query}")
        soup = BeautifulSoup(page.content, "html.parser")

        # Check redirect
        if len(page.history) == 1: # If not redirected:
            redirect = soup.find("table").find("p").find("a") # Get first "relevant result" 

            if redirect.text == query: # If the suggestion is what we originally searched for:
                redirect = redirect.get("href") # Get redirect page
                page = requests.get(URL + redirect.replace("/dictionary/", ""))
                soup = BeautifulSoup(page.content, "html.parser")

                # Getting video
                video = soup.find(id="signvideo")
                video = video.find("source").get("src")
                video = requests.get(video)
                open(f'./videos/{num}.mp4', 'wb').write(video.content)

                # Getting keywords
                words = soup.find(id="keywords").find("p")
                words = "".join(words.text.splitlines()).replace(" ", "").replace(",", ", ").replace("Keywords:", "")
                result = words
            else: # If the word is not in the Auslan database:
                for char in query: # Spell the word with Auslan letters

                    open(f"./videos/{num}.mp4").write() #/letters/{char}.mp4 

                    result = query + " " + char
        else:
            # Getting video
            video = soup.find(id="signvideo")
            video = video.find("source").get("src")
            video = requests.get(video)
            open(f'./videos/{num}.mp4', 'wb').write(video.content)

            # Getting word
            words = soup.find(id="keywords").find("p")
            words = "".join(words.text.splitlines()).replace(" ", "").replace(",", ", ").replace("Keywords:", "")
            result = words

        returned.append(result)

    return returned


# Running code
if __name__ == "__main__":
    while True:
        text = input("Text: ")
        auslan = Auslan(text)

        print(auslan)

        # Cleanup
        for file in os.listdir("./videos"):
            os.remove(f"./videos/{file}")
