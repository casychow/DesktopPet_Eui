import datetime
# Import Flask Library
from flask import Flask, redirect, render_template, request
app = Flask(__name__, static_folder='assets')

# Globals (these will all be stored in database)
USERNAME = "Buddy"

workPeriod = 25
restPeriod = 5
numReminder = 2 
numSnooze = 0

workOption = 1
restOption = 1
workPersonalized = ""
restPersonalized = ""

soundOption = 1
motionOption = 1
lightOption = 1

streak_numOfDays = 0
streak_pomodorosOneDayAmt = 0
streak_pomodorosOneDayDate = datetime.datetime.now().strftime("%m/%d/%Y")

# Handle Home page

@app.route("/")
def loadHome():
    return render_template('index.html', username=USERNAME)

@app.route('/editname', methods=['GET', 'POST'])
def editName():
    username = request.form['username']

    if (username != ""):
        global USERNAME
        USERNAME = username

    return render_template('index.html', username=USERNAME)

# Handle Pomodoro page

@app.route("/pomodoro")
def loadPomodoro():
    return render_template('pomodoro.html', workOption=workOption, restOption=restOption, 
                            workPeriod=workPeriod, restPeriod=restPeriod, 
                            numReminder=numReminder, numSnooze=numSnooze, 
                            setWorkPersonalized=workPersonalized, setRestPersonalized=restPersonalized)

@app.route("/editpomodorotimer", methods=['GET', 'POST'])
def editPomodoroTimer():

    ''' Retreive Timing Fields '''

    newWorkPeriod = request.form['newWorkPeriod']
    newRestPeriod = request.form['newRestPeriod']

    if (newWorkPeriod != ""):
        global workPeriod
        workPeriod = newWorkPeriod
    if (newRestPeriod != ""):
        global restPeriod
        restPeriod = newRestPeriod

    newNumReminder = request.form['newNumReminder']
    newNumSnooze = request.form['newNumSnooze']

    if (newNumReminder != ""):
        global numReminder
        numReminder = newNumReminder
    if (newNumSnooze != ""):
        global numSnooze
        numSnooze = newNumSnooze

    ''' Retreive Accountability Fields '''

    global workPersonalized
    global workOption
    getOption = request.form['workOptions']

    if (getOption == "work_option1"):
        workOption = 1
        workPersonalized = ""
    elif (getOption == "work_option2"):
        workOption = 2
        workPersonalized = ""
    else:
        workOption = 3
        getVal = request.form['workPersonalized']
        if (getVal != ""):
            workPersonalized = getVal

    global restPersonalized
    global restOption
    getOption = request.form['restOptions']

    if (getOption == "rest_option1"):
        restOption = 1
        restPersonalized = ""
    elif (getOption == "rest_option2"):
        restOption = 2
        restPersonalized = ""
    else:
        restOption = 3
        getVal = request.form['restPersonalized']
        if (getVal != ""):
            restPersonalized = getVal

    return render_template('pomodoro.html', workOption=workOption, restOption=restOption, 
                            workPeriod=workPeriod, restPeriod=restPeriod, 
                            numReminder=numReminder, numSnooze=numSnooze, 
                            setWorkPersonalized=workPersonalized, setRestPersonalized=restPersonalized)

# Handle Statistics page

@app.route("/statistic")
def loadStatistic():
    return render_template('statistic.html', daysStreak=streak_numOfDays, highestStreakNum=streak_pomodorosOneDayAmt, 
                            highestStreakDate=streak_pomodorosOneDayDate)

# Handle Alert page

@app.route("/alert")
def loadAlert():
    return render_template('alert.html', soundOption=soundOption, motionOption=motionOption, lightOption=lightOption)

@app.route("/editalert", methods=['GET', 'POST'])
def editAlert():
    getOption = request.form['soundOptions']
    global soundOption

    if (getOption == "sound_option1"):
        soundOption = 1
    elif (getOption == "sound_option2"):
        soundOption = 2
    elif (getOption == "sound_option3"):
        soundOption = 3
    elif (getOption == "sound_option4"):
        soundOption = 4

    getOption = request.form['motionOptions']
    global motionOption

    if (getOption == "motion_option1"):
        motionOption = 1
    elif (getOption == "motion_option2"):
        motionOption = 2
    elif (getOption == "motion_option3"):
        motionOption = 3
    elif (getOption == "motion_option4"):
        motionOption = 4
    elif (getOption == "motion_option5"):
        motionOption = 5

    getOption = request.form['lightOptions']
    global lightOption

    if (getOption == "light_option1"):
        lightOption = 1
    elif (getOption == "light_option2"):
        lightOption = 2
    elif (getOption == "light_option3"):
        lightOption = 3
    elif (getOption == "light_option4"):
        lightOption = 4
    elif (getOption == "light_option5"):
        lightOption = 5

    return render_template('alert.html', soundOption=soundOption, motionOption=motionOption, lightOption=lightOption)

# Load Contacts page

@app.route("/contact_us")
def loadContactUs():
    return render_template('contact_us.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

