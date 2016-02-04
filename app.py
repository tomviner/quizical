import json
import random
from flask import Flask, request, render_template, session, abort, redirect, url_for

app = Flask(__name__)
app.secret_key = "aoieghh;oisahg;oisaehg;oiesag;oieagh;oieah;oiea;oa"
data = json.load(open('questions.json'))

def get_question():
    q = data['questions'][session["current_question"]]
    if q is None:
        return None
    title, *answers = q
    correct, *incorrects = answers
    return title, correct, answers

@app.route('/')
def hello_world():
    session["current_question"] = 0
    session["score"] = 0
    return render_template('index.html')

@app.route('/question', methods=["GET"])
def question():
    context = {}
    title, _, answers = get_question()
    random.shuffle(answers)
    return render_template('question.html', **{
        'question_title': title,
        'answers': answers,
    })

@app.route('/question', methods=["POST"])
def submit_question():
    option = request.form["answer"]
    _, correct, answers = get_question()
    if option not in answers:
        return abort(400)

    session["score"] += int(option == correct)
    session["current_question"] += 1
    if not get_question():
        return redirect(url_for('.score'))

    return redirect(url_for('.hello_world'))

@app.route('/score', methods=["GET"])
def score():
    return "Done"






if __name__ == '__main__':
    app.run(debug=1)
