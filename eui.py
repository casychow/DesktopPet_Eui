# Import Flask Library
from flask import Flask, redirect, render_template, request
app = Flask(__name__, static_folder='')

# Globals
USERNAME = "Buddy"
workPeriod = 25
restPeriod = 5

# Load pages
@app.route("/")
def loadHome():
    # return render_template('index.html', username=USERNAME)
    return app.send_static_file('index.html')

@app.route('/editname', methods=['GET', 'POST'])
def editName():
    username = request.form['username']

    if (username != ""):
        global USERNAME
        USERNAME = username

    return render_template('index.html', username=USERNAME)

@app.route("/pomodoro")
def loadPomodoro():
    return render_template('pomodoro.html', workPeriod=workPeriod, restPeriod=restPeriod)

@app.route("/editpomodorotimer", methods=['GET', 'POST'])
def editPomodoroTimer():
    global workPeriod
    global restPeriod

    workPeriod = request.form['newWorkPeriod']
    restPeriod = request.form['newRestPeriod']

    return render_template('pomodoro.html', workPeriod=workPeriod, restPeriod=restPeriod)

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

