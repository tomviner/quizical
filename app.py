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
def index():
    session["current_question"] = 0
    session["score"] = 0
    session["answers"] = []
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_image(path):
    return send_from_directory('static', path)

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
    title, correct, answers = get_question()
    if option not in answers:
        return abort(
            400,
            "{option} is not an option for {title}".format(**locals()))

    session["score"] += int(option == correct)
    session["current_question"] += 1
    session["answers"].append({
        'title': title,
        'is_correct': option == correct,
        'user_answer': option,
        'correct_answer': correct,
    })
    if not get_question():
        return redirect(url_for('.score'))

    return redirect(url_for('.question'))

@app.route('/score', methods=["GET"])
def score():
    return render_template('results.html', **{
        'correct': session["score"],
        'total': len(data['questions'])-1,
        'questions': session["answers"],
    })

if __name__ == '__main__':
    app.run(debug=1)
