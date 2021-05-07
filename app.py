''' NOTES (for database and user settings usage)
### Database format ###

CREATE TABLE PomodoroStats(
    Date TEXT PRIMARY KEY NOT NULL,     # enter as daytime('now') to add current daytime
    Weekday TEXT NOT NULL,              # day of the week on which task is completed
    Duration REAL NOT NULL,             # amount of time spent on task (in mins)
    Completed_Task INT NOT NULL,        # 0 = Pomodoro & 1 = break
    Question_Answered INT NOT NULL      # 0 = No question & 1 = answered & 2 = not answered 
);

### Configuration format ###

# Default user settings (as stored in "default_usersettings.yaml")
DEFAULT_USER_SETTINGS = { "username" : "Buddy",
                            "workPeriod" : 25,    # in minutes
                            "restPeriod" : 5,     # in minutes
                            "numReminder" : 0,
                            "numSnooze" : 2,
                            "workOption" : 1,
                            "workPersonalized" : "",
                            "restOption" : 1,
                            "restPersonalized" : "",
                            "soundOption" : 1,
                            "motionOption" : 1,
                            "lightOption" : 1,
                            "lastUsedDay": ['', '']     # (weekday, date)
                        }
'''

from stubby_eui import *
import yaml     # for storing user configuration settings
import sqlite3  # for storing user's pomodoro usage statistics
from datetime import datetime
import random

''' Globals '''

USER_INFO_FILE = 'eui_UI/usersettings.yaml'

# Grab stored user settings
with open(USER_INFO_FILE) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    USER_SETTINGS = yaml.load(file, Loader=yaml.FullLoader)

# database file with pomodoro usage statistics
EUI_STATS_FILE = "eui_UI/sample_eui_stats.db"      # using sample/toy database file
# EUI_STATS_FILE = "/eui_UI/eui_stats.db"             # actual database file


''' OLED Display Functions '''

def countPomodoros(conn, weekday):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pomodoroStats WHERE Weekday='" + weekday + "'")
    query = cur.fetchall()

    return len(query)//2, query    # one pomodoro = one work period + one break period

def displayMessageAtStartup():
    message = "Hi Buddy!\n"
    lastUsedWeekday, lastUsedDate = USER_SETTINGS['lastUsedDay']
    
    if (lastUsedWeekday == ""):
        message += "You completed 0 pomodoros this week...\n"
    else:
        try:
            conn = sqlite3.connect(EUI_STATS_FILE)
        except Error as e:
            print(e)
        
        numPomodoros, query = countPomodoros(conn, lastUsedWeekday)

        message += "Previously on " + lastUsedDate + ", you completed " 
        message += str(numPomodoros) + " pomodoros!\n"

    displayText(message)    # display message on OLED

def displayResponse(encourageUser):     # encourageUser is a bool
    switcher = {
        1: "WOW!!! You're amazing :)",
        2: "Keep it up! Don't give up now!",
        3: "Eui is impressed! :)",
        4: "You're doing great!",
        5: "Eui knew you can do it! <3"
    }

    if (not encourageUser):
        message = "Ahh... Is that so...\nTry again next time...\n"
    else:
        message = "Good job!\n" + switcher.get(random.randint(1,5), "nothing")
    
    displayText(message)    # display message on OLED


''' Functions to Store Information to Database & Yaml '''

def storeCurrDayAndDate():
    todayWeekday = datetime.today().strftime('%A')
    todayDate = datetime.today().strftime('%Y-%m-%d')

    switcher = {
        "Monday": "mon",
        "Tuesday": "tue",
        "Wednesday": "wed",
        "Thursday": "thu",
        "Friday": "fri",
        "Saturday": "sat",
        "Sunday": "sun"
    }

    todayWeekday = switcher.get(todayWeekday, "nothing")

    # update yaml data
    USER_SETTINGS['lastUsedDay'] = [todayWeekday, todayDate]

    with open(USER_INFO_FILE, 'w') as file:
        yaml.dump(USER_SETTINGS, file)
