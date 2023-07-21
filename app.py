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

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions
    )


@app.post('/begin')
def to_question_0():
    """Redirect to the first question
    and make sure there is no previous responses"""

    responses.clear()
    return redirect('/questions/0')


@app.get('/questions/<int:qidx>')
def to_question(qidx):
    # display or show question for func name
    """Go to question with index qidx """

    question = survey.questions[qidx]
    return render_template('question.html', question=question)


@app.post('/<int:qidx>/answer')
def add_response(qidx):
    """Get the answer from a question than go to the next question,
       if all questions are answered, go to thank you page.
    """
    current_answer = request.form["answer"]
    responses.append(current_answer)

    next_question_index = qidx+1

    if next_question_index >= len(survey.questions):
        return redirect('/completion')

    return redirect(f'/questions/{next_question_index}')


@app.get('/completion')
def to_completion():
    """Go to the thank you page and display the questions and answers"""

    return render_template('completion.html', responses=responses,
                           len = len(responses), questions = survey.questions)
