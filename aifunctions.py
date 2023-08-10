import openai
import config, os

openai.api_key = config.OPENAI_API_KEY

def get_chat_gpt_options_string_single_message(message, model = "gpt-4" , temperature = 0.7):

    print("**model***")
    print(model)
    options = {
        "messages": [{"role": "user", "content": message}],
        "temperature": temperature,
        "max_tokens": 1024,
        "n": 1,
        "stop":None,
        "model": model,
    }
    return options



def create_question(subject, level, exam_board, number_of_marks, topic, same_again_sentence):
    number_of_marks = number_of_marks if number_of_marks else 3
    topic_sentance = '''The question should be on the topic of {}.'''.format(topic) if topic else " "

    exam_board_sentence = 'Model the question on previous {} {} {} papers.'.format(level,subject,exam_board) if len(exam_board) > 0 else " "

    message = '''Create a {} {} {} example exam question, worth {} mark(s), which we will refer to as <question>. {} {} {}. It is important that the number of marks is exactly {}.
    If you refer to a text, either refer to it by name or quote it.
    The exam question must be a question that can receive a text-based answer.
    You must include all the information required to answer the question.
    If it is a maths question, make sure you follow the san mateo county community college district standard for writing maths in ascii.
    Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)].`
    '''.format(subject, level, exam_board, number_of_marks, exam_board_sentence, same_again_sentence,  topic_sentance, number_of_marks, exam_board, subject, level )

    print(message)

    try:
        print('\n\n***BOUT to try \n\n\n')
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
    except Exception as e:
        print(f"Problem with: {e}")

    return response


def create_mark_scheme(subject, level, exam_board, question, number_of_marks):

    number_of_marks = number_of_marks if number_of_marks else 3
    message = '''The following is a {} {} {} example exam question, which is worth {} mark(s): `{}`.
        Now, create a mark scheme for this question. We will now refer to this as <mark_scheme> It should outline what an answer would need to demonstrate for a range of possible marks, including maximum marks. The person using this mark scheme may not be familar with the subject matter, so be very specific
        when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them.
        Using your knowledge of previous {} {} {} mark schemes when creating this mark scheme. If it is a maths question, make sure you include the correct answer to the question (which is `{}`)  in your the mark scheme.
        Leave a new line between each mark explanation. Give the answer in the format: `\n<mark_scheme>\n`.'''.format(level, subject, exam_board, number_of_marks, question, level, subject, exam_board, question )

    print(message)

    try:
        print('\n\n***BOUT to try \n\n\n')
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
    except Exception as e:
        print(f"Problem with: {e}")

    return response



def same_again(subject, level, exam_board, number_of_marks, topic, question):
    sameAgainSentence = "It should be very similar to the question {}, but not exactly the same. Keep the subject area as similar as possible, but make sure it has a different answer.".format(question)
    return create_question(subject, level, exam_board, number_of_marks, topic, sameAgainSentence)


def get_message_base(subject, level, exam_board, question):

    exam_board_sentence = ", for the exam board {}".format(exam_board) if len(exam_board) > 0 else ""
    return '''The following is a {} {} example exam question{}. "{}"'''.format(subject, level, exam_board_sentence, question)

def get_feedback(subject, level, exam_board, question, answer, marks, mark_scheme):

    messageBase = get_message_base(subject, level, exam_board, question)

    answer = answer if len(answer) > 0 else "I am not able to write an answer to this question"

    messageVariant = '''A student gave the following answer: "{}" to the question {}. Leave a comment on their work saying how many marks out of {} this answer get according to the following mark scheme: "{}". Then explain how could this answer be improved. Use \n for new lines
    Please be as specific as you can be. The tone should be friendly but definitely not patronizing. Refer to the student in the second person. Remember that, for maths, it is fine to just write the maths, no verbose explaination is needed '''.format(answer, question, marks, mark_scheme, exam_board, subject, level )
    message = messageBase+messageVariant
    print(message)

    try:
        print("*Trying Feedback*")
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
        print("*Feedback*")
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    return response

def get_star_answer(subject, level, exam_board, question, answer, marks, mark_scheme):
    messageBase = get_message_base(subject, level, exam_board, question)
    messageVariant = '''Give a perfect answer to this question. This answer should get full marks in a {} {} {} exam for the question, according to the following mark scheme: `{}`.
    Remember to show all your working. Your answer should be in the format of a pupil writing an answer in an exam, and should be appropriate for a {} level answer. Do not repeat the question back in your answer. Use \n for new lines'''.format(subject, exam_board, level, mark_scheme, level )
    message = messageBase+messageVariant
    print(message)

    try:
        print("*\ngetting perfect answer*")
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
        print("*Perfect response*")
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    return response

def get_hint(subject, level, exam_board, question, marks):
    messageBase = get_message_base(subject, level, exam_board, question)
    messageVariant = '''A student is struggling to answer this question. Create a hint for them that doesn't give the answer away but will guide them in the right direction. The tone should be friendly but definitely not patronizing. Refer to the student in the second person. Do not return your answer in quotes.'''
    message = messageBase+messageVariant
    print("****HINT****")
    print(message)

    try:
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
        print("*Hint *")
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    return response
