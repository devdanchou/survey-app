from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def to_home():
    """Directs user to start the survey"""
    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", title=title,
                           instructions=instructions)


@app.post('/begin')
def to_question_0():
    """Redirect to the first question
    and make sure there is no previous responses"""

    responses.clear()
    return redirect('/questions/0')


@app.get('/questions/<int:qidx>')
def to_question(qidx):
    """Go to question with a certain number """

    question = survey.questions[qidx]
    return render_template('question.html', question=question)

# post request to /answer
#     hand over the answer from the user to the responses list
#     redirect to the next question

@app.post('/answer')
def add_response():

    response = request.form["answer"]
    responses.append(response)
    next_question = len(responses)
    next_question_index = len(responses)

    if next_question_index >= len(survey.questions)
        return redirect('/completion')

    return redirect(f'/questions/{next_question}')


@app.get('/completion')
def to_completion():

