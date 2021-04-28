''' NOTES (for database and user settings usage)
### Database format ###

CREATE TABLE PomodoroStats(
    Date TEXT PRIMARY KEY NOT NULL,     # enter as daytime('now') to add current daytime
    Weekday TEXT NOT NULL,              # day of the week on which task is completed
    Duration REAL NOT NULL,             # amount of time spent on task
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
                            "lightOption" : 1
                        }
'''

import datetime
import yaml     # for storing user configuration settings
import sqlite3  # for storing user's pomodoro usage statistics

# Import Flask Library
from flask import Flask, redirect, render_template, request
app = Flask(__name__, static_folder='assets')

# Grab stored user settings
with open('usersettings.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    USER_SETTINGS = yaml.load(file, Loader=yaml.FullLoader)

# Globals
streak_numOfDays = 0
streak_pomodorosOneDayAmt = 0
streak_pomodorosOneDayDate = datetime.datetime.now().strftime("%m/%d/%Y")

''' Handle Home page '''

@app.route("/")
def loadHome():
    return render_template('index.html', username=USER_SETTINGS["username"])

@app.route('/editname', methods=['GET', 'POST'])
def editName():
    username = request.form['username']

    if (username != ""):
        global USER_SETTINGS
        USER_SETTINGS['username'] = username

        # update yaml data
        with open('usersettings.yaml', 'w') as file:
            yaml.dump(USER_SETTINGS, file)

    return render_template('index.html', username=USER_SETTINGS['username'])

''' Handle Pomodoro page '''

@app.route("/pomodoro")
def loadPomodoro():
    return render_template('pomodoro.html', workOption=USER_SETTINGS['workOption'], restOption=USER_SETTINGS['restOption'], 
                            workPeriod=USER_SETTINGS['workPeriod'], restPeriod=USER_SETTINGS['restPeriod'], 
                            numReminder=USER_SETTINGS['numReminder'], numSnooze=USER_SETTINGS['numSnooze'], 
                            setWorkPersonalized=USER_SETTINGS['workPersonalized'], setRestPersonalized=USER_SETTINGS['restPersonalized'])

@app.route("/editpomodorotimer", methods=['GET', 'POST'])
def editPomodoroTimer():
    global USER_SETTINGS

    ''' Retreive Timing Fields '''

    newWorkPeriod = request.form['newWorkPeriod']
    newRestPeriod = request.form['newRestPeriod']

    if (newWorkPeriod != ""):
        USER_SETTINGS['workPeriod'] = int(newWorkPeriod)
    if (newRestPeriod != ""):
        USER_SETTINGS['restPeriod'] = int(newRestPeriod)

    newNumReminder = request.form['newNumReminder']
    newNumSnooze = request.form['newNumSnooze']

    if (newNumReminder != ""):
        USER_SETTINGS['numReminder'] = int(newNumReminder)
    if (newNumSnooze != ""):
        USER_SETTINGS['numSnooze'] = int(newNumSnooze)

    ''' Retreive Accountability Fields '''

    getOption = request.form['workOptions']

    if (getOption == "work_option1"):
        USER_SETTINGS['workOption'] = 1
        USER_SETTINGS['workPersonalized'] = ""
    elif (getOption == "work_option2"):
        USER_SETTINGS['workOption'] = 2
        USER_SETTINGS['workPersonalized'] = ""
    else:
        USER_SETTINGS['workOption'] = 3
        getVal = request.form['workPersonalized']
        if (getVal != ""):
            USER_SETTINGS['workPersonalized'] = getVal

    getOption = request.form['restOptions']

    if (getOption == "rest_option1"):
        USER_SETTINGS['restOption'] = 1
        USER_SETTINGS['restPersonalized'] = ""
    elif (getOption == "rest_option2"):
        USER_SETTINGS['restOption'] = 2
        USER_SETTINGS['restPersonalized'] = ""
    else:
        USER_SETTINGS['restOption'] = 3
        getVal = request.form['restPersonalized']
        if (getVal != ""):
            USER_SETTINGS['restPersonalized'] = getVal

    # update yaml data
    with open('usersettings.yaml', 'w') as file:
        yaml.dump(USER_SETTINGS, file)

    return render_template('pomodoro.html', workOption=USER_SETTINGS['workOption'], restOption=USER_SETTINGS['restOption'], 
                            workPeriod=USER_SETTINGS['workPeriod'], restPeriod=USER_SETTINGS['restPeriod'], 
                            numReminder=USER_SETTINGS['numReminder'], numSnooze=USER_SETTINGS['numSnooze'], 
                            setWorkPersonalized=USER_SETTINGS['workPersonalized'], setRestPersonalized=USER_SETTINGS['restPersonalized'])

''' Handle Statistics page '''

@app.route("/statistic")
def loadStatistic():
    return render_template('statistic.html', daysStreak=streak_numOfDays, highestStreakNum=streak_pomodorosOneDayAmt, 
                            highestStreakDate=streak_pomodorosOneDayDate)

''' Handle Alert page '''

@app.route("/alert")
def loadAlert():
    return render_template('alert.html', soundOption=USER_SETTINGS['soundOption'], 
                            motionOption=USER_SETTINGS['motionOption'], lightOption=USER_SETTINGS['lightOption'])

@app.route("/editalert", methods=['GET', 'POST'])
def editAlert():
    global USER_SETTINGS

    getOption = request.form['soundOptions']

    if (getOption == "sound_option1"):
        USER_SETTINGS['soundOption'] = 1
    elif (getOption == "sound_option2"):
        USER_SETTINGS['soundOption'] = 2
    elif (getOption == "sound_option3"):
        USER_SETTINGS['soundOption'] = 3
    elif (getOption == "sound_option4"):
        USER_SETTINGS['soundOption'] = 4

    getOption = request.form['motionOptions']

    if (getOption == "motion_option1"):
        USER_SETTINGS['motionOption'] = 1
    elif (getOption == "motion_option2"):
        USER_SETTINGS['motionOption'] = 2
    elif (getOption == "motion_option3"):
        USER_SETTINGS['motionOption'] = 3
    elif (getOption == "motion_option4"):
        USER_SETTINGS['motionOption'] = 4
    elif (getOption == "motion_option5"):
        USER_SETTINGS['motionOption'] = 5

    getOption = request.form['lightOptions']

    if (getOption == "light_option1"):
        USER_SETTINGS['lightOption'] = 1
    elif (getOption == "light_option2"):
        USER_SETTINGS['lightOption'] = 2
    elif (getOption == "light_option3"):
        USER_SETTINGS['lightOption'] = 3
    elif (getOption == "light_option4"):
        USER_SETTINGS['lightOption'] = 4
    elif (getOption == "light_option5"):
        USER_SETTINGS['lightOption'] = 5

    # update yaml data
    with open('usersettings.yaml', 'w') as file:
        yaml.dump(USER_SETTINGS, file)

    return render_template('alert.html', soundOption=USER_SETTINGS['soundOption'], 
                            motionOption=USER_SETTINGS['motionOption'], lightOption=USER_SETTINGS['lightOption'])

''' Load Contacts page '''

@app.route("/contact_us")
def loadContactUs():
    return render_template('contact_us.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
