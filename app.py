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
import time
import random
import threading
import sys

''' Globals '''

USER_INFO_FILE = 'eui_UI/usersettings.yaml'

# Grab stored user settings/configurations
with open(USER_INFO_FILE) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    USER_SETTINGS = yaml.load(file, Loader=yaml.FullLoader)

# Database file with pomodoro usage statistics
EUI_STATS_FILE = "eui_UI/sample_eui_stats.db"      # using sample/toy database file
# EUI_STATS_FILE = "/eui_UI/eui_stats.db"             # actual database file

# for playMelody() -- London Bridge

c = [32, 65, 131, 262, 523]
db = [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb = [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb = [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab = [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb = [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

''' BEATS:
        0.5 = eigth note
        1 = quarter note
        2 = half note
        3 = dotted half note
        4 = whole note
'''

londonBridge = [g[2], a[2], g[2], f[2], e[2], f[2], g[2], d[2],
                e[2], f[2], e[2], f[2], g[2], g[2], a[2], g[2],
                f[2], e[2], f[2], g[2], d[2], g[2], e[2], c[2]]
LBbeats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1,
                1, 1, 1, 2, 2, 2, 1, 1]

# Pin for Sound
SOUNDPIN = 12

# Pins for lights
DATA = 21 #SOUNDPIN
STOR = 13
SHIFT = 18
NSHIFT = 16

# Pins for Motors
IN1 = 27 #2
IN2 = 22 #3
EN1 = 4
IN3 = 1
IN4 = 0
EN2 = 5

# Pin for OLED display
RST = 26 #24

# Pins for Buttons
RESET_BTN = 23 #red
POMODORO_BTN = 24 #blue
RESPOND_YES_BTN = None
RESPOND_NO_BTN = None

''' State machine functions '''

STATE = "IDLE"
STATELOCK = threading.Lock()
alarmIsOn = False
workTimerStarted = None
restTimerStarted = None

euiGotAResponse = False     # (FOR NOW: assumes user does not answer question)
euiAskAQuestion = False     # (FOR NOW: assumes eui does not ask a question)
userRespondYes = False
userRespondNo = False

'''
def yesButtonThread():
    global euiGotAResponse
    global userRespondYes

    while True:
        # if user answer "yes" and eui asked a question and have not yet gotten a response
        if (buttonPressed(RESPOND_YES_BTN) and euiAskAQuestion and not euiGotAResponse):
            euiGotAResponse = True
            userRespondYes = True

def noButtonThread():
    global euiGotAResponse
    global userRespondNo

    while True:
        # if user answer "yes" and eui asked a question and have not yet gotten a response
        if (buttonPressed(RESPOND_NO_BTN) and euiAskAQuestion and not euiGotAResponse):
            euiGotAResponse = True
            userRespondNo = True
'''

def resetButtonThread():
    global STATE
    global alarmIsOn
    global workTimerStarted
    global restTimerStarted
    global euiGotAResponse
    global euiAskAQuestion
    global userRespondYes
    global userRespondNo

    while True:
        # block while red button is not pressed
        while (not buttonPressed(RESET_BTN)):
            continue

        with STATELOCK:
            print("red pressed!")

            displayText("Session ended early... this won't count!")

            STATE = "IDLE"
            workTimerStarted = None
            restTimerStarted = None

            # reset all fields back to defaults
            euiGotAResponse = False
            euiAskAQuestion = False
            userRespondYes = False
            userRespondNo = False

        if (alarmIsOn):
            alarmOff()
            alarmIsOn = False


def stateMachine():
    global STATE
    global alarmIsOn
    global workTimerStarted
    global restTimerStarted
    global euiGotAResponse
    global euiAskAQuestion

    # start thread to always monitor & capture red button press
    btnThread = threading.Thread(target=resetButtonThread)
    btnThread.start()

    '''
    # start thread to always monitor RESPOND_YES_BTN
    btnThread2 = threading.Thread(target=yesButtonThread)
    btnThread2.start()

    # start thread to always monitor RESPOND_NO_BTN
    btnThread3 = threading.Thread(target=noButtonThread)
    btnThread3.start()
    '''

    while True:

        if (STATE == "IDLE"):
            print("STATE =", STATE)

            # block while blue button is not pressed
            while (not buttonPressed(POMODORO_BTN)):
                continue

            # set up fields for user to start work session
            with STATELOCK:
                STATE = "WORK"
                workTimerStarted = time.time()
                displayWorkModeIndicator(DATA)
                displayText("Time to start working! FIGHTING!")

        if (STATE == "WORK"):
            print("STATE =", STATE)

            try:
                # if duration of the work session is over
                if (time.time()-workTimerStarted >= (USER_SETTINGS['workPeriod']*60)):
                #if (time.time()-workTimerStarted >= (0.1*60)):	# test code

                    with STATELOCK:
                        if (STATE == "WORK"):
                            turnOffLED()                # turn off indicator lights
                            time.sleep(1)
                            alarmOn()                   # turn alarms on
                            alarmIsOn = True
                            workTimerStarted = None     # stop work timer

                    '''
                    # ask user a question if there is one
                    euiAskAQuestion = (USER_SETTINGS['workOption'] != 1)

                    if (euiAskAQuestion):
                        displayText(USER_SETTINGS['workPersonalized'])

                    # block while eui have not gotten a response
                    while (not euiGotAResponse):
                        continue

                    if (userRespondYes):        # assuming "Yes" means user did as expected
                        displayResponse(True)   # display encouraging response
                    else:                       # else user did not do as expected
                        displayResponse(False)  # display a "try again" message
                    '''

                    # add work session to database
                    insertUserData(True, euiAskAQuestion,
                                    euiGotAResponse, USER_SETTINGS['workPeriod'])

                    '''
                    euiAskedAQuestion = False   # reset s.t. eui have not asked a question
                    euiGotAResponse = False
                    '''

                    # block while blue button is not pressed && state is still WORK
                    while (not buttonPressed(POMODORO_BTN) and (STATE == "WORK")):
                        continue

                    with STATELOCK:
                        if (STATE == "WORK"):  # check if state changed (i.e. if red button pressed while waiting)
                            alarmOff()      # turn alarms off
                            alarmIsOn = False

                            # set up fields for user to start rest session
                            STATE = "REST"
                            restTimerStarted = time.time()
                            displayRestModeIndicator(DATA)

                            displayText("REST TIME :)")

            except TypeError: #if reset button is presed before timerbtn has elapsed
                continue

        if (STATE == "REST"):
            print("STATE =", STATE)

            try:
                # if duration of the rest session is over
                if (time.time()-restTimerStarted >= (USER_SETTINGS['restPeriod']*60)):
                #if (time.time()-restTimerStarted >= (0.1*60)):	# test code
                    with STATELOCK:
                        if (STATE == "REST"):
                            turnOffLED()                # turn off indicator lights
                            time.sleep(10)
                            alarmOn()                   # turn alarms on
                            alarmIsOn = True
                            restTimerStarted = None     # stop rest timer
                            #restIndicatorOn = False     # stop lights #get rid of this

                    '''
                        # ask user a question if there is one
                        euiAskAQuestion = (USER_SETTINGS['restOption'] != 1)

                        if (euiAskAQuestion):
                            displayText(USER_SETTINGS['restPersonalized'])

                        # block while eui have not gotten a response
                        while (not euiGotAResponse):
                            continue

                        if (userRespondYes):        # assuming "Yes" means user did as expected
                            displayResponse(True)   # display encouraging response
                        else:                       # else user did not do as expected
                            displayResponse(False)  # display a "try again" message
                    '''

                    # add rest session to database
                    insertUserData(False, euiAskAQuestion,
                                            euiGotAResponse, USER_SETTINGS['restPeriod'])

                    '''
                        euiAskedAQuestion = False   # reset s.t. eui have not asked a question
                        euiGotAResponse = False
                    '''

                    # block while blue button is not pressed && state is still REST
                    while (not buttonPressed(POMODORO_BTN) and (STATE == "REST")):
                        continue

                    with STATELOCK:
                        if (STATE == "REST"):  # check if state changed (i.e. if red button pressed while waiting)
                            alarmOff()      # turn alarms off
                            alarmIsOn = False

                            # set up fields for user to start work session
                            STATE = "WORK"
                            workTimerStarted = time.time()
                            displayWorkModeIndicator(DATA)

                            displayText("Time to get back to work!!")

            except TypeError: #if reset button is presed before timerbtn has elapsed
                continue


''' Run at start up '''

def setup():
    setupLED(DATA, STOR, SHIFT, NSHIFT)
    setupSound(SOUNDPIN)
    setupMotors(IN1, IN2, EN1, IN3, IN4, EN2)
    setupDisplay(RST)
    setupBtn(RESET_BTN)
    setupBtn(POMODORO_BTN)
    '''
    setupBtn(RESPOND_YES_BTN)
    setupBtn(RESPOND_NO_BTN)
    '''

def runAtStartup():
    setup()
    makeSound(SOUNDPIN)
    displayMessageAtStartup()

''' OLED Display Functions '''

def countPomodoros(weekday):

    # Form connection with the database
    try:
        conn = sqlite3.connect(EUI_STATS_FILE)
    except Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute("SELECT * FROM pomodoroStats WHERE Weekday='" + weekday + "'")
    query = cur.fetchall()

    cur.close()
    conn.close()

    return len(query)//2, query    # one pomodoro = one work period + one break period

def displayMessageAtStartup():
    message = "Hi " + USER_SETTINGS['username'] + "!\n"
    lastUsedWeekday, lastUsedDate = USER_SETTINGS['lastUsedDay']
    if (lastUsedWeekday == ""):
        message += "You completed 0 pomodoros this week...\n"
    else:
        numPomodoros, query = countPomodoros(lastUsedWeekday)

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

    message = "Good job!\n" + switcher.get(random.randint(1,5), "nothing")

    if (not encourageUser):
        message = "Ahh... Is that so...\nTry again next time...\n"

    displayText(message)    # display message on OLED


''' Functions for alarms '''

def euiMove():
    while True:
        rightTurn(IN1, IN2, EN1, IN3, IN4, EN2)
        time.sleep(0.5)
        leftTurn(IN1, IN2, EN1, IN3, IN4, EN2)
        time.sleep(0.5)
        #break

def alarmOn():
    print("alarmOn begin:", threading.active_count())


    if (USER_SETTINGS['lightOption'] != 5):     # user wanted some sort of lights
        lightShow = threading.Thread(target=LEDwave)
        lightShow.start()
    '''
    if (USER_SETTINGS['motionOption'] != 5):    # user wanted some sort of movement
        motorThread = threading.Thread(target=euiMove)
        motorThread.start()
    '''
    if (USER_SETTINGS['soundOption'] != 4):     # user wanted some sort of sound
        playSong = threading.Thread(target=playMelody, args=(londonBridge, LBbeats, 0.3, SOUNDPIN))
        playSong.start()

    print("alarmOn after:", threading.active_count())

def alarmOff():
    print("alarmOff begin:", threading.active_count())

    if (USER_SETTINGS['lightOption'] != 5):     # user wanted some sort of lights
        turnOffLED()
    '''
    if (USER_SETTINGS['motionOption'] != 5):    # user wanted some sort of movement
        stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)
    '''
    if (USER_SETTINGS['soundOption'] != 4):     # user wanted some sort of sound
        stopSound()

    print("alarmOff after:", threading.active_count())


''' Functions to Store Information to Database & Yaml '''

def getCurrDate():
    todayWeekday = datetime.today().strftime('%A')
    todayDate = datetime.today()

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

    return (todayWeekday, todayDate)

def storeCurrDayAndDate():
    today = getCurrDate()

    # update yaml data
    USER_SETTINGS['lastUsedDay'] = [today[0], today[1]]

    with open(USER_INFO_FILE, 'w') as file:
        yaml.dump(USER_SETTINGS, file)

def insertUserData(userDidWork, askedAQuestion,
                    userAnsweredQuestion, sessionDuration):
    print("Inserting data...")

    # Form connection with the database
    try:
        conn = sqlite3.connect(EUI_STATS_FILE)
    except Error as e:
        print(e)

    cur = conn.cursor()

    insertStatement = "INSERT INTO PomodoroStats (Date, Weekday, Duration, Completed_Task, Question_Answered) VALUES (?,?,?,?,?)"
    completedTask = 0   # assume user did work (0 = did work)
    questionAnswered = 0    # assume no question asked (0 = no question)

    if (not userDidWork):
        completedTask = 1   # user took a break
    if (askedAQuestion):    # user was asked a question
        if (userAnsweredQuestion):      # user answered the question
            questionAnswered = 1
        else:
            questionAnswered = 2        # user did not answer the question

    today = getCurrDate()   # get today's weekday and date
    weekday = today[0]
    date = today[1]

    cur.execute(insertStatement, (date, weekday, sessionDuration, completedTask, questionAnswered))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':

    try:
        runAtStartup()
        stateMachine()

    except KeyboardInterrupt:
        stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)
        turnOffLED()
        GPIO.cleanup()
        sys.exit()
