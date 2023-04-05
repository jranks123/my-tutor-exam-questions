import openai
import config, os

openai.api_key = config.OPENAI_API_KEY
print("key = " + openai.api_key)

def create_question(subject, level, topic):
    """Create a exam question. The exam question must be an question that can receive a text-based
    answer. I'm going to ask a student this question and ask you to mark their answer later, so make sure it's a question that you would
    be confident ansering yourself correctly
    """
    print(subject)
    print(level)
    print(topic)

    options = {
        "model": "text-davinci-003",
        "prompt": "Create a " + level + " " + subject + " example exam question. It is very important that you do not give the answer. The exam question must be an question that can receive a text-based answer. Y",
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
