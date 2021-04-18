# Import Flask Library
from flask import Flask, redirect, render_template
app = Flask(__name__, static_folder='')

# Define a route to hello function
@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

