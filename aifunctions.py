import openai
import config, os

openai.api_key = config.OPENAI_API_KEY
print("key = " + openai.api_key)


def create_question(subject, level, exam_board, number_of_marks, topic, same_again_sentence):

    number_of_marks = number_of_marks if number_of_marks else 3
    topic_sentance = '''The question should be on the topic of {}.'''.format(topic) if topic else " "

    exam_board_sentence = 'Model the question on previous {} {} {} papers.'.format(subject, level, exam_board) if len(exam_board) > 0 else " "

    message = '''Create a {} {} {} example exam question, worth {} mark(s). {} {} {} Return your answer in the format `Question: <question> [<number of marks> Mark(s)]`.  It is important that the number of marks is exactly {}.
    It is very important that you do not give the answer. If you refer to a text, either refer to it by name or quote it. The exam question must be an question that can receive a text-based answer. Do not return your answer in quotes.'''.format(subject, level, exam_board, number_of_marks, exam_board_sentence, same_again_sentence,  topic_sentance, number_of_marks)

    print(message)

    options = get_da_vinci_options(message)
    print(options)
    try:
        response = openai.Completion.create(**options)['choices'][0]["text"].strip().split('\n')
        print(response)
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

def get_feedback(subject, level, exam_board, question, answer, marks):

    messageBase = get_message_base(subject, level, exam_board, question)

    answer = answer if len(answer) > 0 else "I am not able to write an answer to this question"

    messageVariant = '''A student gave the following answer: "{}" to the question {}. Leave a comment on their work saying how many marks out of {} this answer get and how could this answer be improved. Use \n for new lines
    Please be as specific as you can be. The tone should be friendly but definitely not patronizing. Refer to the student in the second person.'''.format(answer, question, marks)
    message = messageBase+messageVariant
    print(message)

    try:
        response = openai.Completion.create(**get_da_vinci_options(message))['choices'][0]['text'].strip().split('\n')
        print("*Feedback*")
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    return response

def get_star_answer(subject, level, exam_board, question, answer, marks):
    messageBase = get_message_base(subject, level, exam_board, question)
    messageVariant = '''Give a perfect answer to this question. This answer should get {} marks in a {} {} {} exam for the question. Use your knowledge of {} past exams and their marking criteria to write the answer.
    Remember to show all your working. Your answer should be in the format of a pupil writing an answer in an exam. Do not repeat the question back in your answer. Use \n for new lines'''.format(marks, subject, exam_board, exam_board, level, question)
    message = messageBase+messageVariant
    print(message)

    try:
        response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(message))['choices'][0]['message']["content"].strip().split('\n')
        print("*Perfect response*")
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
