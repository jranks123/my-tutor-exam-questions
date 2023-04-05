import openai
import config, os

openai.api_key = config.OPENAI_API_KEY
print("key = " + openai.api_key)

def create_question(subject, level, exam_board, number_of_marks, topic):
    """Create a exam question. The exam question must be an question that can receive a text-based
    answer. I'm going to ask a student this question and ask you to mark their answer later, so make sure it's a question that you would
    be confident ansering yourself correctly
    """
    print(subject)
    print(level)
    print(exam_board)
    print(number_of_marks)

    topic_sentance = '''The question should be on the topic of {}.'''.format(topic)

    message = '''Create a {} {} {} example exam question, worth {} mark(s), and display the number of marks it could receive. {} It is important that the number of marks is exactly {}.
    It is very important that you do not give the answer. The exam question must be an question that can receive a text-based answer'''.format(subject, level, exam_board, number_of_marks, topic_sentance, number_of_marks, exam_board)

    print(message)

    options = {
        "model": "text-davinci-003",
        "prompt": message,
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = openai.Completion.create(**options)
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")

    return response['choices'][0]["text"]


def getOptions(message):
    options = {
        "model": "text-davinci-003",
        "prompt": message,
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    return options

def analyse_answer(subject, level, exam_board, question, answer):

    messageBase = '''The following is a {} {} example exam question, for the exam board {}.
    \n \n {} \n \n. A student gave the following answer: \n \n {} \n
    Imagine you are an exam marker for this exam board.'''.format(subject, level, exam_board, question, answer)

    messageVariantOne = '''How could this answer be improved? Please be as specific as you can be. Write your answer as if you were giving it directly to the student. The tone should be friendly but not patronizing. And if the answer is perfect, tell them so!'''
    messageVariantTwo = '''What would a perfect answer to this question be?'''

    try:
        responseOne = openai.Completion.create(**getOptions(messageBase+messageVariantOne))
        responseTwo = openai.Completion.create(**getOptions(messageBase+messageVariantTwo))
        print(response)
    except Exception as e:
        print(f"Problem with: {e}")

    response = {
        "feedback": responseOne['choices'][0]["text"],
        "perfect_answer": responseTwo['choices'][0]["text"]
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
