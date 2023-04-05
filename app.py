from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
# import marvin_functions
import aifunctions

app = Flask(__name__, static_folder=config.UPLOAD_FOLDER)

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('generate_question.html', **locals())

@app.route('/create_question', methods=['POST'])
def create_question():
    # Get the question data from the form

    print("****")
    print(request.form)

    subject = request.form.get('subject')
    level = request.form.get('level')
    marks = request.form.get('marks')
    topic = request.form.get('topic')
    exam_board = request.form.get('exam-board')




    # Call your function to create the question
    question = aifunctions.create_question(subject, level, exam_board, marks, topic)
    session["question"] = question
    session["subject"] = subject
    session["level"] = level
    session["exam-board"] = exam_board
    session["marks"] = marks

    # Redirect to the questions page
    return redirect(url_for('answer_question'))


@app.route('/same_again', methods=['POST'])
def same_again():
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    topic = session["topic"]
    marks = session["marks"]

    question = aifunctions.same_again(question, subject, level, exam_board, marks, topic)
    session["question"] = question

    return render_template('answer_question.html', **locals())

@app.route('/submit_answer', methods=['POST'])
def submit_answer():

    # Get the question data from the form
    answer = request.form.get('answer')
    session['answer'] = answer

    question = session['question']
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    marks = session["marks"]

    response = aifunctions.analyse_answer(subject, level, exam_board, '\n'.join(question), answer, marks)

    feedback = response['feedback']
    perfect_answer = response['perfect_answer']
    answers_class = "show"
    submit_class = "hidden"

    return render_template('answer_question.html', **locals())



@app.route('/answer_question', methods=['GET'])
def answer_question():
    question = session['question']
    answers_class = "hidden"
    submit_class = "show"
    answer = ""
    return render_template('answer_question.html', **locals())



@app.route('/generate_question', methods=["GET", "POST"])
def somePage():
    return render_template('generate_question.html', **locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
