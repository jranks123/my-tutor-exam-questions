from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import config
import aifunctions

app = Flask(__name__, static_folder=config.UPLOAD_FOLDER)

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=["GET", "POST"])
def index():
    subject = session['subject'] if session['subject'] else 'Maths'
    level = session['level'] if session['level'] else 'GCSE'
    exam_board = session["exam-board"] if session["exam-board"] else 'Edexcel'
    topic = session["topic"] if session["topic"] else ""
    marks = session["marks"] if session["marks"] else 3

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
    question = aifunctions.create_question(subject, level, exam_board, marks, topic, "")
    session["question"] = question
    session["subject"] = subject
    session["level"] = level
    session["exam-board"] = exam_board
    session["marks"] = marks
    session["topic"] = topic

    # Redirect to the questions page
    return redirect(url_for('answer_question'))


@app.route('/same_again', methods=['POST'])
def same_again():
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    topic = session["topic"]
    marks = session["marks"]
    question = session["question"]

    question = aifunctions.same_again(subject, level, exam_board, marks, topic, question)
    session["question"] = question

    return "Updated Question"

@app.route('/new_topic', methods=['POST'])
def new_topic():
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    topic = session["topic"]
    marks = session["marks"]
    question = session["question"]

    question = aifunctions.create_question(subject, level, exam_board, marks, "", "")
    session["question"] = question

    return "Updated Question"

@app.route('/get-feedback', methods=['POST'])
def get_feedback():

    # Get the question data from the form
    answer = request.form.get('answer')
    session['answer'] = answer

    question = session['question']
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    marks = session["marks"]

    response = aifunctions.get_feedback(subject, level, exam_board, '\n'.join(question), answer, marks)
    answers_class = "show"
    submit_class = "hidden"

    return jsonify({'result': response})

@app.route('/get-star-answer', methods=['POST'])
def get_star_answer():

    # Get the question data from the form
    answer = request.form.get('answer')
    session['answer'] = answer

    question = session['question']
    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    marks = session["marks"]

    response = aifunctions.get_star_answer(subject, level, exam_board, '\n'.join(question), answer, marks)
    answers_class = "show"
    submit_class = "hidden"

    return jsonify({'result': response})




@app.route('/answer_question', methods=['GET'])
def answer_question():

    subject = session['subject']
    level = session['level']
    exam_board = session["exam-board"]
    topic = session["topic"]
    marks = session["marks"]
    question = session["question"]

    print("****")
    print("question")
    question = session['question']
    print(question)
    answers_class = "hidden"
    submit_class = "show"
    answer = ""

    return render_template('answer_question.html', **locals())



@app.route('/generate_question', methods=["GET", "POST"])
def somePage():
    return render_template('generate_question.html', **locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
