import openai
import config, os

openai.api_key = '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'



def create_question(subject, level, exam_board, number_of_marks, topic, same_again_sentence):

    number_of_marks = number_of_marks if number_of_marks else 3
    topic_sentance = '''The question should be on the topic of {}.'''.format(topic) if topic else " "

    exam_board_sentence = 'Model the question on previous {} {} {} papers.'.format(subject, level, exam_board) if len(exam_board) > 0 else " "

    message = '''Create a {} {} {} example exam question, worth {} mark(s), which we will refer to as <question>. {} {} {}. It is important that the number of marks is exactly {}.
    If you refer to a text, either refer to it by name or quote it.
    The exam question must be an question that can receive a text-based answer.
    You must include all the information required to answer the question.
    If it is a maths question, make sure you follow the san mateo county community college district standard for writing maths in ascii.
    Also return a detailed accompanying mark scheme, which we will refer to as <mark_scheme>, for this question outlining what an answer would need to demonstrate for a range of possible marks, including maximum marks. Be as detailed as possible, using your knowledge of previous {} {} {} mark schemes. Leave a new line between each mark explanation.
    Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)]. *SPLIT* <mark_scheme>.`
    '''.format(subject, level, exam_board, number_of_marks, exam_board_sentence, same_again_sentence,  topic_sentance, number_of_marks, exam_board, subject, level )

    print(message)

    options = get_da_vinci_options(message)
    print(options)
    try:
        print('\n\n***BOUT to try \n\n\n')
        response = openai.Completion.create(**options)['choices'][0]["text"].strip().split('*SPLIT*')
        question = response[0].split('\n')
        print(question)
        mark_scheme = response[1].split('\n')
        print(mark_scheme)
    except Exception as e:
        print(f"Problem with: {e}")

    return (question, mark_scheme)


def create_mark_scheme(subject, level, exam_board, number_of_marks, topic, same_again_sentence):

    number_of_marks = number_of_marks if number_of_marks else 3
    topic_sentance = '''The question should be on the topic of {}.'''.format(topic) if topic else " "

    exam_board_sentence = 'Model the question on previous {} {} {} papers.'.format(subject, level, exam_board) if len(exam_board) > 0 else " "

    message = '''Create a mark scheme for the following {} {} {} example exam question, which is worth {} mark(s). It should outline what an answer would need to demonstrate for a range of possible marks, including maximum marks. Be as detailed as possible, using your knowledge of previous {} {} {} mark schemes. Leave a new line between each mark explanation.
    '''.format(level, subject exam_board, number_of_marks, level, subject, exam_board )

    print(message)

    options = get_da_vinci_options(message)
    print(options)
    try:
        print('\n\n***BOUT to try \n\n\n')
        response = openai.Completion.create(**options)['choices'][0]["text"].strip()
    except Exception as e:
        print(f"Problem with: {e}")

    return response




def same_again(subject, level, exam_board, number_of_marks, topic, question):
    sameAgainSentence = "It should be very similar to the question {}, but not exactly the same. Keep the subject area as similar as possible, but make sure it has a different answer.".format(question)
    return create_question(subject, level, exam_board, number_of_marks, topic, sameAgainSentence)


def get_da_vinci_options(message):
    options = {
        "model": "text-davinci-003",
        "prompt": message,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    return options

def get_chat_gpt_options_string_single_message(message):
    options = {
        "messages": [{"role": "user", "content": message}],
        "temperature": 1,
        "max_tokens": 1024,
        "n": 1,
        "stop":None,
        "model": "gpt-3.5-turbo",
    }
    return options


def get_message_base(subject, level, exam_board, question):

    exam_board_sentence = ", for the exam board {}".format(exam_board) if len(exam_board) > 0 else ""
    return '''The following is a {} {} example exam question{}. "{}"'''.format(subject, level, exam_board_sentence, question)

def get_feedback(subject, level, exam_board, question, answer, marks, mark_scheme):

    messageBase = get_message_base(subject, level, exam_board, question)

    answer = answer if len(answer) > 0 else "I am not able to write an answer to this question"

    messageVariant = '''A student gave the following answer: "{}" to the question {}. Leave a comment on their work saying how many marks out of {} this answer get according to the following mark scheme: "{}". Then explain how could this answer be improved. Use \n for new lines
    Please be as specific as you can be. The tone should be friendly but definitely not patronizing. Refer to the student in the second person. Remember that, for maths, it is 100% fine to just write the maths, no verbose explaination is needed '''.format(answer, question, marks, mark_scheme, exam_board, subject, level )
    message = messageBase+messageVariant
    print(message)

    try:
        print("*Trying Feedback*")
        response = openai.Completion.create(**get_da_vinci_options(message))['choices'][0]['text'].strip().split('\n')
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
        response = openai.Completion.create(**get_da_vinci_options(message))['choices'][0]['text'].strip().split('\n')
        print("*Hint *")
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    return response




def completion_query(options):
    """
    This method calls the openai CompletionCreate method. Use this if you're just sending standard prompt string.
    Options should be:
        model="text-davinci-003",
        prompt="Dear AI, do stuff for me",
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    """
    try:
        response = openai.Completion.create(**options)
    except Exception as e:
        print(f"Problem with: {e}")

    return response


def chat_completion_query(options):
        """
        This method calls the openAI ChatCompletionCreate method. Use this if you want to send priming sequences.
        Options should be:
            messages=messages,
            temperature=1,
            max_tokens=1024,
            n=1,
            stop=None,
        The messages is an array of objects, system, user and assisant, eg:
        priming_sequence = [
            {"role": "system", "content": "You are an AI writer. You write compelling and informative content designed to help people understand complex topics."},
            {"role": "user", "content": "Mike: Hi, I'm a programmer setting up your environment."},
            {"role": "assistant", "content": "It's nice to meet you."},
        ]
        """
        options["model"] = "gpt-3.5-turbo"
        try:
            return openai.ChatCompletion.create(
                **options
            )
        except Exception as e:
            print(f"Problem with: {e}.")


def get_choices(openAIResponse, type="chat_completion_query"):
    """
    Returns a choice from the openai api response. This is generally the words you're looking for </force>
    """
    try:
        if type == "chat_completion_query":
            text = openAIResponse['choices'][0]["message"]['content']
        else:
            text = openAIResponse['choices'][0]["text"]

        return text
    except Exception as e:
        print(f"Unable to find choices: {e}.")
        return None
