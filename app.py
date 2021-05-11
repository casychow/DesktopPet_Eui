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
import multiprocessing

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

# Pins for lights
DATA = 21
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
START_POMODORO_SEQ = 23 #red
STOP_ALARM_BTN = 24 #blue

# Pin for Sound
SOUNDPIN = 12


workTimerStarted = False
restTimerStarted = False
euiGotAResponse = False
euiAskedQuestion = False
pomodoroStarted = False

start = 0

''' Run in the background '''

def startPomodoroSeqThread():
    global workTimerStarted
    global restTimerStarted
    global pomodoroStarted
    global start

    while True:
        while (not buttonPressed(START_POMODORO_SEQ)):  # while button not pressed
            continue

        if (workTimerStarted and pomodoroStarted):
            #if pomodoro and work session is both on, user is ending early
            workTimerStarted = False
            pomodoroStarted = False
            displayText("Work session won't count! Ended session early...")
        elif (restTimerStarted and pomodoroStarted):
            #user is ending rest early - not going to count to consecutive pomodoro
            restTimerStarted = False
            pomodoroStarted = False
            displayText("Rest session won't count! Ended session early...")
        elif (not workTimerStarted and not pomodoroStarted):          # if work timer was not started
            print("Pomodoro session has begun!")
            start = time.time()             # start work timer
            workTimerStarted = True         # mark as started work
            pomodoroStarted = True

def stopAlarmBtnThread():
    global workTimerStarted
    global restTimerStarted
    global start

    while True:
        while (not buttonPressed(STOP_ALARM_BTN)):  # while button not pressed
            continue

        alarmOff()
        print("Alarm off")

        if (workTimerStarted):
            workTimerStarted = False
            restTimerStarted = True
            time.sleep(0.5)
            start = time.time()
        elif (restTimerStarted):
            restTimerStarted = False
            workTimerStarted = True
            time.sleep(0.5)
            start = time.time()

def handleButtonPressed():
    print("worker thread here <----")
    '''
    workTimerStarted = False
    restTimerStarted = False
    pomodoroStarted = False
    euiGotAResponse = False
    '''
    global workTimerStarted
    global restTimerStarted
    global pomodoroStarted
    global euiGotAResponse
    global start

    pomThread = threading.Thread(target=startPomodoroSeqThread, name="pom")
    pomThread.start()

    stopAlarmThread = threading.Thread(target=stopAlarmBtnThread, name="start_alarm")
    stopAlarmThread.start()

    while True:
        '''
        if (buttonPressed(START_POMODORO_SEQ)):          # if timer button is pressed
            if (workTimerStarted and pomodoroStarted):
                #if pomodoro and work session is both on, user is ending early
                workTimerStarted = False
                pomodoroStarted = False
                displayText("Work session won't count! Ended session early...")
            elif (restTimerStarted and pomodoroStarted):
                #user is ending rest early - not going to count to consecutive pomodoro
                restTimerStarted = False
                pomodoroStarted = False
                displayText("Rest session won't count! Ended session early...")
            elif (not workTimerStarted and not pomodoroStarted):          # if work timer was not started
                print("Pomodoro session has begun!")
                start = time.time()             # start work timer
                workTimerStarted = True         # mark as started work
                pomodoroStarted = True

        if (buttonPressed(STOP_ALARM_BTN)):
            alarmOff()
            print("Alarm off")
            if (workTimerStarted):
                workTimerStarted = False
                restTimerStarted = True
                time.sleep(0.5)
            elif (restTimerStarted):
                restTimerStarted = False
                workTimerStarted = True
                time.sleep(0.5)
        '''


        # checks if timed session is complete (FOR NOW: assumes user does not answer question)

        if (workTimerStarted):
            #if (time.time()-start >= (USER_SETTINGS['workPeriod']*60)):
            if (time.time()-start >= (0.1*60)):
                print("Work time is over. Go rest.")

                #alarmOn()
                alarmThread = threading.Thread(target=alarmOn, name="alarm")
                alarmThread.start()

                insertUserData(True, (USER_SETTINGS['workOption'] != 1),
                                euiGotAResponse, USER_SETTINGS['workPeriod'])
                #storeSession = threading.Thread(target=insertUserData, name="storeSesh",
                #                    args=(True, (USER_SETTINGS['workOption'] != 1),
                #                    euiGotAResponse, USER_SETTINGS['workPeriod']))
                #storeSession.start()

        if (restTimerStarted):
            #if (time.time()-start >= (USER_SETTINGS['restPeriod']*60)):
            print(time.time()-start)

            if (time.time()-start >= (0.1*60)):
                print("Rest time is over. Go work.")

                #alarmOn()
                alarmThread = threading.Thread(target=alarmOn, name="alarm")
                alarmThread.start()

                insertUserData(False, (USER_SETTINGS['restOption'] != 1),
                                    euiGotAResponse, USER_SETTINGS['restPeriod'])
                #storeSession = threading.Thread(target=insertUserData, name="storeSesh",
                #                    args=(True, (USER_SETTINGS['restOption'] != 1),
                #                    euiGotAResponse, USER_SETTINGS['restPeriod']))
                #storeSession.start()

def waitForButtonsThread():
    btnThread = threading.Thread(target=handleButtonPressed, name="Button")
    btnThread.daemon = True
    btnThread.start()


''' Run at start up '''

def setup():
    setupLED(DATA, STOR, SHIFT, NSHIFT)
    setupSound(SOUNDPIN)
    setupMotors(IN1, IN2, EN1, IN3, IN4, EN2)
    setupDisplay(RST)
    setupBtn(START_POMODORO_SEQ)
    setupBtn(STOP_ALARM_BTN)

def runAtStartup():
    setup()
    makeSound(SOUNDPIN)
    displayMessageAtStartup()
    waitForButtonsThread()
    while True:
        continue

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

ALARM_PROCESSES = []

def euiMove():
    while True:
        rightTurn(IN1, IN2, EN1, IN3, IN4, EN2)
        time.sleep(0.5)
        leftTurn(IN1, IN2, EN1, IN3, IN4, EN2)
        time.sleep(0.5)

def alarmOn():
    if (USER_SETTINGS['lightOption'] != 5):     # user wanted some sort of lights
        lightShow = multiprocessing.Process(target=LEDwave)
        #lightShow = threading.Thread(target=LEDwave, name="Light Show")
        lightShow.start()
        ALARM_PROCESSES.append(lightShow)

    if (USER_SETTINGS['motionOption'] != 5):    # user wanted some sort of movement
        motorThread = multiprocessing.Process(target=euiMove)
        #motorThread = threading.Thread(target=euiMove, name="Eui Move")
        motorThread.start()
        ALARM_PROCESSES.append(motorThread)

    if (USER_SETTINGS['soundOption'] != 4):     # user wanted some sort of sound
        playSong = multiprocessing.Process(target=playMelody, args=(londonBridge, LBbeats, 0.3, SOUNDPIN))
        #playSong = threading.Thread(target=playMelody, name="Sound show", args=(londonBridge, LBbeats, 0.3, SOUNDPIN))
        playSong.start()
        ALARM_PROCESSES.append(playSong)

def alarmOff():
    if (USER_SETTINGS['lightOption'] != 5):     # user wanted some sort of lights
        turnOffLED()

    if (USER_SETTINGS['motionOption'] != 5):    # user wanted some sort of movement
        stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)

    #if (USER_SETTINGS['soundOption'] != 4):     # user wanted some sort of sound
        #stopSound()

    for process in ALARM_PROCESSES:
        process.terminate() #terminate running thread

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
    print("Inserting data")
    print(askedAQuestion)

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

    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    try:
        runAtStartup()
        #test button press here
        '''
        alarmOn()
        time.sleep(5)
        alarmOff()
        '''
    except KeyboardInterrupt:
        stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)
        turnOffLED()
        GPIO.cleanup()
        sys.exit()
