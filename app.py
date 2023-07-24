from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import config
import aifunctions
import time
import openai

app = Flask(__name__, static_folder=config.UPLOAD_FOLDER)

app = Flask(__name__)

app.secret_key = 'your_secret_key_2'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/prompt', methods=['GET'])
def home():
    return render_template('general_prompt.html', **locals())

@app.route('/api', methods=['POST'])
def get_gpt_response():
    prompt = request.json['prompt']
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
    return jsonify(response.choices[0].text.strip())


@app.route('/', methods=["GET", "POST"])
def index():
    subject = session.get('subject') if session.get('subject') else 'English'
    level = session.get('level') if session.get('level') else 'GCSE'
    exam_board = session.get("exam-board") if session.get("exam-board") else 'Edexcel'
    topic = session.get("topic") if session.get("topic") else ""
    mark_scheme = session.get("mark_scheme") if session.get("mark_scheme") else ""
    marks = session.get("marks") if session.get("marks") else 3

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
    #hint = aifunctions.get_hint(subject, level, exam_board, '\n'.join(question), marks)
    #session["hint"] = hint
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
    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    topic = session.get("topic")
    marks = session.get("marks")
    question = session.get("question")

    question = aifunctions.same_again(subject, level, exam_board, marks, topic, question)
    hint = aifunctions.get_hint(subject, level, exam_board, '\n'.join(question), marks)
    session["hint"] = hint
    session["question"] = question
    return "Updated Question"

@app.route('/new_topic', methods=['POST'])
def new_topic():
    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    topic = session.get("topic")
    marks = session.get("marks")
    question = session.get("question")

    question = aifunctions.create_question(subject, level, exam_board, marks, "", "")
    hint = aifunctions.get_hint(subject, level, exam_board, '\n'.join(question), marks)
    session["hint"] = hint
    session["question"] = question
    return "Updated Question"

@app.route('/get-feedback', methods=['POST'])
def get_feedback():
    while session.get('mark_scheme') == 'loading':
        time = 1
        #do nothing
    # Get the question data from the form
    answer = request.form.get('answer')
    session['answer'] = answer

    question = session.get('question')
    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    marks = session.get("marks")
    mark_scheme = session.get("mark_scheme")
    print(mark_scheme)
    response = aifunctions.get_feedback(subject, level, exam_board, '\n'.join(question), answer, marks, mark_scheme)

    return jsonify({'result': response})


@app.route('/get-mark-scheme', methods=['POST'])
def get_mark_scheme():
    print("getting mark scheme")
    session['mark_scheme'] = "loading"
    # Get the question data from the form
    question = session.get('question')
    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    marks = session.get("marks")
    mark_scheme = aifunctions.create_mark_scheme(subject, level, exam_board, '\n'.join(question), marks)
    print("\n oioi")
    print(mark_scheme)
    session['mark_scheme'] = mark_scheme
    return jsonify({'result': mark_scheme})

@app.route('/get-star-answer', methods=['POST'])
def get_star_answer():

    wait = 1
    while session.get('mark_scheme') == 'loading':
        wait = wait + 1
        wait = wait - 1

    # Get the question data from the form
    answer = request.form.get('answer')
    session['answer'] = answer

    question = session.get('question')
    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    marks = session.get("marks")
    mark_scheme = session.get("mark_scheme")

    response = aifunctions.get_star_answer(subject, level, exam_board, '\n'.join(question), answer, marks, mark_scheme)
    answers_class = "show"
    submit_class = "hidden"

    return jsonify({'result': response})




@app.route('/answer_question', methods=['GET'])
def answer_question():

    subject = session.get('subject')
    level = session.get('level')
    exam_board = session.get("exam-board")
    topic = session.get("topic")
    marks = session.get("marks")
    hint = session.get("hint")
    question = session.get("question")
    mark_scheme = session.get("mark_scheme")

    print("****")
    print("question")
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
