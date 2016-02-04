import json
import random
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/question')
def question():
    data = json.load(open('questions.json'))
    context = {}
    for q in filter(None, data['questions']):
        title, *answers = q
        correct, *incorrects = answers
        random.shuffle(answers)
        return render_template('question.html', **{
            'question_title': title,
            'answers': answers,
        })

    return data




if __name__ == '__main__':
    app.run(debug=1)
