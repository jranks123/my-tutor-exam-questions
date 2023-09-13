import os, csv
import openai
import time
import aifunctions
import random

openai.api_key = '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'


use_sub_topics = True

if use_sub_topics == True:
    file_name = 'res.csv'
else:
    file_name = 'res_no_subtopics.csv'

print(file_name)

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

def get_topics(file_name):
    temp_dict = {}

    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        print(reader.fieldnames)
        for row in reader:
            topic = row['topic']
            sub_topic_prompt_string = row['sub_topic_prompt_string']

            # If the topic already exists, append the sub-topic. If not, create a new entry.
            if topic in temp_dict:
                temp_dict[topic].append(sub_topic_prompt_string)
            else:
                temp_dict[topic] = [sub_topic_prompt_string]

    # Convert the dictionary to the desired data structure
    topic_to_subtopic_prompt_string_mappings = []
    for key, value in temp_dict.items():
        topic_to_subtopic_prompt_string_mappings.append({
            'topic_name': key,
            'sub_topic_prompt_strings': value
        })

    return topic_to_subtopic_prompt_string_mappings


topics = get_topics('geography_sub_topics.csv')



question_prompts = []


def get_topic_sentence(topic):
    if use_sub_topics is False:
        return '''The question should be randomly selected from all of the topic {}'''.format(topic_name)
    else:
        return '''The question should be randomly selected from the following content areas of the topic {}: (start of content list) {} (End of content list). Once you have decided which content to create a question on, the question can be randomly selected from anything in the specification about that subtopic.'''.format(topic['topic_name'], random.choice(topic['sub_topic_prompt_strings']))



def get_prompts():
    for topic in topics:
        for i in range (2):

            prompt2 = [2, topic['topic_name'], '''Create a Geography GCSE Edexcel iGCSE example exam question, worth 2 mark(s), which we will refer to as <question>. Model the question on previous GCSE Edexcel iGCSE Geography papers. {}. It is important that the number of marks is exactly 2. The question will include a 'command word or phrase' at the beginning of the question, randomly choose one of the following command phrases before choosing the content: 1. Explain one 2. Suggest 3. Identify two or 4. Explain the meaning of…’. Never include more than one of these command phrases. Limit the question to one sentence. Do not refer to an image or source or require the answer to include a diagram. The exam question must be a question that can receive a text-based answer. You must include all the information required to answer the question. Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)].` Do not include any additional information.'''.format(get_topic_sentence(topic))]


            prompt4 = [4, topic['topic_name'], '''"Create a Geography GCSE Edexcel iGCSE example exam question, worth 4 mark(s), which we will refer to as <question>. Model the question on previous GCSE Edexcel iGCSE Geography papers. The question should be randomly selected from all of the topic {}. It is important that the number of marks is exactly 4. The question will start with a 'command word', this will have an even chance of being either ‘explain’ or ‘suggest’, but never include both.  Limit the question to one sentence. Do not refer to an image or source or require the answer to include a diagram. The exam question must be a question that can receive a text-based answer. You must include all the information required to answer the question. Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)].` Do not include any additional information."'''.format(get_topic_sentence(topic))]


            prompt6 = [6, topic['topic_name'], '''Create a Geography GCSE Edexcel iGCSE example exam question, worth 6 mark(s), which we will refer to as <question>. Model the question on previous GCSE Edexcel iGCSE Geography papers. The question should be randomly selected from all of the topic {}. It is important that the number of marks is exactly 6. The question will include a 'command word', for 6 mark questions this will have a 50% chance of being either 'assess' or 'explain' but never include both. Limit the question to one sentence. The exam question must be a question that can receive a text-based answer. If you refer to case studies or examples, don't name them, let the student decide. Do not refer to an image or source or require the answer to include a diagram. You must include all the information required to answer the question. Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)].`'''.format(get_topic_sentence(topic))]

            prompt8 = [8, topic['topic_name'], '''Create a Geography GCSE Edexcel iGCSE example exam question, worth 8 mark(s), which we will refer to as <question>. Model the question on previous GCSE Edexcel iGCSE Geography papers. The question should be randomly selected from all of the topic {}. It is important that the number of marks is exactly 8. The question will include a 'command word', for 8 mark questions this will have an even chance of being either ‘evaluate’, ‘analyse’ or 'asess', but never include more than one of these. Limit the question to one sentence. The exam question must be a question that can receive a text-based answer. If you refer to case studies or examples, don't name them, let the student decide. Do not refer to an image or source or require the answer to include a diagram. You must include all the information required to answer the question.  Give your response to this request in the format `Question: <question> [<number of marks> Mark(s)].`'''.format(get_topic_sentence(topic))]

            question_prompts.extend([prompt2, prompt4, prompt6, prompt8])
    return question_prompts


question_prompts = get_prompts()

with open(file_name, 'w') as file:
    pass

with open(file_name, mode='a', newline='') as file:
    writer = csv.writer(file)

    for prompt in question_prompts:
        print(prompt[1])
        print(prompt[0])
        print(prompt[2])
        print()
        try:
            print('\n\n***BOUT to try \n\n\n')
            time.sleep(5)
            response = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(prompt[2]))['choices'][0]['message']["content"].strip().split('\n')
            new_row = [prompt[0], prompt[1], response]
            writer.writerow(new_row)
        except Exception as e:
            print(f"Problem with: {e}")
