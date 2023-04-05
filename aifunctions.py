import openai
import config, os

openai.api_key = config.OPENAI_API_KEY
print("key = " + openai.api_key)


def create_question(subject, level, exam_board, number_of_marks, topic, sameAgainSentence=""):

    number_of_marks = number_of_marks if number_of_marks else 3
    topic_sentance = '''The question should be on the topic of {}.'''.format(topic) if topic else ""

    message = '''Create a {} {} {} example exam question, worth {} mark(s). {} Display the number of marks it could receive in the format: "Marks available: X". {} It is important that the number of marks is exactly {}.
    It is very important that you do not give the answer. The exam question must be an question that can receive a text-based answer.'''.format(subject, level, exam_board, number_of_marks, sameAgainSentence, topic_sentance, number_of_marks, exam_board)

    print(message)

    options = getDaVinciOptions(message)
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


def getDaVinciOptions(message):
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

def getChatGPTOptionsSingleMessage(message):
    options = {
        "messages": [{"role": "user", "content": message}],
        "temperature": 1,
        "max_tokens": 1024,
        "n": 1,
        "stop":None,
        "model": "gpt-3.5-turbo",
    }
    return options

def analyse_answer(subject, level, exam_board, question, answer, marks):

    messageBase = '''The following is a {} {} example exam question, for the exam board {}. "{}"'''.format(subject, level, exam_board, question)

    messageVariantOne = '''A student gave the following answer: "{}" to the question {}. Leave a comment on their work saying how many marks out of {} this answer get and how could this answer be improved. Use \n for new lines
    Please be as specific as you can be. The tone should be friendly but definitely not patronizing.'''.format(answer, question, marks)
    messageVariantTwo = '''Give a perfect answer to this question. This answer should get {} marks in a {} {} exam for the question. Remember to show all your working. Your answer should be in the format of a pupil writing an answer in an exam. Use \n for new lines'''.format(marks, subject, level, question)

    messageOne = messageBase+messageVariantOne
    print(messageOne)

    messageTwo = messageBase+messageVariantTwo
    print(messageTwo)

    try:
        responseOne = openai.Completion.create(**getDaVinciOptions(messageOne))['choices'][0]['text'].strip().split('\n')
        print("*Response one*")
        print(responseOne)
        responseTwo = openai.ChatCompletion.create(**getChatGPTOptionsSingleMessage(messageTwo))['choices'][0]['message']["content"].strip().split('\n')
        print("*Response two*")
        print(responseTwo)
    except Exception as e:
        print(f"Problem with: {e}")
        return

    response = {
        "feedback": responseOne,
        "perfect_answer": responseTwo
    }

    return response


def completionQuery(options):
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


def chatCompletionQuery(options):
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


def getChoices(openAIResponse, type="chatCompletionQuery"):
    """
    Returns a choice from the openai api response. This is generally the words you're looking for </force>
    """
    try:
        if type == "chatCompletionQuery":
            text = openAIResponse['choices'][0]["message"]['content']
        else:
            text = openAIResponse['choices'][0]["text"]

        return text
    except Exception as e:
        print(f"Unable to find choices: {e}.")
        return None
