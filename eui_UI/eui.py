# Import Flask Library
from flask import Flask, redirect, render_template, request
app = Flask(__name__, static_folder='assets')

# Globals
USERNAME = "Buddy"
workPeriod = 25
restPeriod = 5
numReminder = 2 
numSnooze = 0

workOption = 1
restOption = 1
workPersonalized = ""
restPersonalized = ""



# Load pages
@app.route("/")
def loadHome():
    return render_template('index.html', username=USERNAME)
    # return app.send_static_file('index.html')

@app.route('/editname', methods=['GET', 'POST'])
def editName():
    username = request.form['username']

    if (username != ""):
        global USERNAME
        USERNAME = username

    return render_template('index.html', username=USERNAME)

@app.route("/pomodoro")
def loadPomodoro():
    return render_template('pomodoro.html', workPeriod=workPeriod, restPeriod=restPeriod, 
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
    getOption = request.form['workOptions']

    if (getOption == "work_option1"):
        workOption = 1
        workPersonalized = ""
    elif (getOption == "work_option2"):
        workOption = 2
        workPersonalized = ""
    else:
        getVal = request.form['workPersonalized']
        if (getVal != ""):
            workPersonalized = getVal

    global restPersonalized
    getOption = request.form['restOptions']

    if (getOption == "rest_option1"):
        restOption = 1
        restPersonalized = ""
    elif (getOption == "rest_option2"):
        restOption = 2
        restPersonalized = ""
    else:
        getVal = request.form['restPersonalized']
        if (getVal != ""):
            restPersonalized = getVal

    return render_template('pomodoro.html', workPeriod=workPeriod, restPeriod=restPeriod, 
                            numReminder=numReminder, numSnooze=numSnooze, 
                            setWorkPersonalized=workPersonalized, setRestPersonalized=restPersonalized)

@app.route("/statistic")
def loadStatistic():
    return render_template('statistic.html')

@app.route("/alert")
def loadAlert():
    return render_template('alert.html')

@app.route("/contact_us")
def loadContactUs():
    return render_template('contact_us.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

