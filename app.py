import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/question')
def question():
    data = json.load(open('questions.json'))
    for q in data
    return data




if __name__ == '__main__':
    app.run()
