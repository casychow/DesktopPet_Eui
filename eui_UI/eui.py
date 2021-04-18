# Import Flask Library
from flask import Flask, redirect, render_template
app = Flask(__name__, static_folder='')

# Load pages 
@app.route("/")
def loadHome():
    return render_template('index.html')

@app.route("/pomodoro")
def loadPomodoro():
    return render_template('pomodoro.html')

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

