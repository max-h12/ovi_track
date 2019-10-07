import smtplib
import requests
import json
import time
from datetime import date

import info

carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def send(number, carrier, message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = (number).format(carriers[carrier])
    auth = (info.email, info.password)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)

def get_goals():
#gets the current number of Ovi goals from NHL Stat API
    URL = "https://statsapi.web.nhl.com/api/v1/people/8471214/stats?stats=statsSingleSeason&season=20192020"
    PARAM = ""
    try:
    #try requesting goals
        r = requests.get(URL, PARAM)
        data = r.json()
        goals = data["stats"][0]["splits"][0]["stat"]["goals"]
        return (goals)
    except:
    #text admin (first no. in list) if exception
        phone = list(info.numbers.keys())[0]
        carrier = list(info.numbers.values())[0]
        send(phone, carrier, f"Unable to check Ovi goals at {date.today}")

def get_games():
    URL = "https://statsapi.web.nhl.com/api/v1/people/8471214/stats?stats=statsSingleSeason&season=20192020"
    PARAM = ""
    try:
    #try requesting games
        r = requests.get(URL, PARAM)
        data = r.json()
        games = data["stats"][0]["splits"][0]["stat"]["games"]
        return (games)
    except:
    #text admin (first no. in list) if exception
        phone = list(info.numbers.keys())[0]
        carrier = list(info.numbers.values())[0]
        send(phone, carrier, f"Unable to check Ovi games at {date.today}")

def get_rank():
    URL = "https://statsapi.web.nhl.com/api/v1/people/8471214/stats?stats=regularSeasonStatRankings&season=20192020"
    PARAM = ""
    try:
    #try requesting rank
        r = requests.get(URL, PARAM)
        data = r.json()
        rankG = data["stats"][0]["splits"][0]["stat"]["rankGoals"]
        rankP = data["stats"][0]["splits"][0]["stat"]["rankPoints"]
        return (f"Ovi is now {rankG} in goals scored, and {rankP} in points this season.")
    except:
    #text admin (first no. in list) if exception
        phone = list(info.numbers.keys())[0]
        carrier = list(info.numbers.values())[0]
        send(phone, carrier, f"Unable to check Ovi rank at {date.today}")

def main():
    goals = get_goals()
    updated = 0    

    for phone, carrier in info.numbers.items():
        send(phone, carrier, ("Ovechkin Goal Tracker Started!"))

    while True:
        updated = get_goals()

        if (updated != goals):
        #if there is a goal update, get data and send messages
            goals = updated
            games = get_games()
            rank = get_rank()

            for phone, carrier in info.numbers.items():
                send(phone, carrier, f"Goal scored by Alex Ovechkin! Goal #{goals} in {games} games this season")
                send(phone, carrier, rank)

        time.sleep(5)


if __name__ == "__main__":
    main()