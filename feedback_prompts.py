import os, csv
import openai
import time
import aifunctions
import random

openai.api_key = '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'

model = ''

use_gpt_4 = False

if use_gpt_4 == True:
    model = "gpt-4"
else:
    model = 'gpt-3.5-turbo-16k'

def get_chat_gpt_options_string_single_message(message, temperature = 0.7):



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


def get_questions():
    questions_list = []

    # Open the CSV file for reading
    with open('csvs/questions_answers.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # For each row in the csv_reader, create a dictionary and append it to the questions_list
        for row in csv_reader:
            # Create a dictionary with the desired format
            question_dict = {
                "number_of_marks": int(row[1]),   # Convert the number of marks to an integer
                "question": row[0],
                "answer": row[2]
            }

            # Append the dictionary to the questions_list
            questions_list.append(question_dict)
    return questions_list




def get_marks_prompts(questions):
    marks_scheme_prompts = []
    print("number of questions")
    print(len(questions))
    for question in questions:
        prompt = ''
        if question['number_of_marks'] == 2:
            prompt = [2, question['question'], '''The following is a Geography GCSE Edexcel iGCSE example exam question, which is worth 2 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, including maximum marks. Only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme including the assessment objectives that would be relevant to this question. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. For questions containing the command word 'identify' and 'suggest', include between 6-8 possible suggestions after the descriptions of the mark brackets, bullet pointed and briefly described in one sentence or less. Identify and describe questions are also only AO1 questions unless there is a figure or source, then they include AO2. For describe and explain questions, give an outline for the different marks followed by 5-6 suggestions for points that could be developed, briefly described in one sentence or less. For explain questions, a brief explanation is fine as long as it is relevant. Give the answer in the format: Title (Mark scheme), leave a line, specific assessment objectives assessed for this question, leave a line, mark scheme in ascending order of marks or levels. Leave a new line between each mark or level explanation.'''.format(question['question'])]
        elif question['number_of_marks'] == 4:
            prompt = [4, question['question'], '''The following is a Geography GCSE Edexcel iGCSE Geography example exam question, which is worth 4 mark(s): {}. Now, create a mark scheme for this question. It should first outline what an answer would need to demonstrate for a range of possible marks. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3) and the mark scheme will include 2 AO3 marks, otherwise don't include AO3. If the question includes the command word 'explain', answers should provide a reasoned explanation of how or why something occurs, it requires a justification/exemplification of a point. Marks can be given as one mark for identification and a second mark for development of this point, even if it is a simple point, for example a correct point followed by an explanation, justification, exemplification or cause of that point would get two marks. So full marks can be awarded for two relevant points that are both developed simply, answers do not need lots of depth, simple points should be awarded marks (make this explicit at the bottom of the mark scheme. If and only if the question says ‘explain two’ also add a statement saying that if only one point is made, no matter how developed it is, a maximum of 2 marks can be awarded). The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question and brief description of what is required for each, and disclaimer that there’s a maximum of two marks for each AO, then marking guidance on what is needed to get 1-2 or 2-4 marks as mentioned above (including detail and a simple example for the marker to differentiate between the two), then (only if the question asks for a named country or city) a disclaimer that says named countries or cities are not worth marks but are needed for full marks when mentioned in the question, then a bullet point list in brief noted format of content that could gain marks with a 1 in brackets after each point or development that could warrant a mark (include 5-8 points that would earn marks in brief note form). Any short example points are bullet pointed and there's no need to write 'e.g' next to it and no numbering should be used. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        elif question['number_of_marks'] == 6:
            prompt = [6, question['question'], '''The following is a Geography GCSE Edexcel iGCSE Geography example exam question, which is worth 6 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, in 3 bands of mark levels called 'levels'. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE  Geography mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3), otherwise don't include AO3. If the source or figure contains specific data, AO4 marks are available for geographical skills, interpreting the data and using it relevantly in the answer. If the question includes the command word 'explain', answers should provide a reasoned explanation of how or why something occurs, it requires a justification/exemplification of a point. If the question includes the command word 'assess' this means use evidence from the source or own knowledge to determine the relative significance of something, giving consideration to factors and identifying which are the most important. If a source is provided, information from this must be used to score high marks. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question, mark scheme in ascending order of levels. Within each level there is a short overview of the skills and content needed, followed by a bullet point list of the indicative content (titled 'Indicative content guidance ') that could be applicable to each assessment objective, the AO's are indicated in brackets after each bullet point. After the level 3 description include a note that says: To get level three, students do not need detailed examples or evidence, one example that is correct and relevant to the question is enough, unless it is a physical geography question, in which case examples are only needed if it is explicit in the question). Any short example points are bullet pointed and there's no need to write 'e.g' next to it. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        elif question['number_of_marks'] == 8:
            prompt = [8, question['question'], '''The following is a Geography GCSE Edexcel iGCSE example exam question, which is worth 8 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, in 3 bands of mark levels called 'levels'. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3), AO3 marks can also be received for using real world examples or case studies relevant to the question. If the source or figure contains specific data, AO4 marks are available for geographical skills, interpreting the data and using it relevantly in the answer. There are no marks for AO1 in any 8 mark question, and there are only AO2 marks available if there is no source or figure directly included in the question, if there is a source/figure, no AO2 marks or AO1 marks are available. If the question includes the command word 'analyse', top level marks must include evidence-based connections about the causes and effects or interrelationships between the components. If the question includes the command word 'evaluate', answers should measure the value or success of something and ultimately provide a substantiated judgement/conclusion, drawing on evidence such as strengths, weaknesses, alternatives and relevant data. If the question includes the command word 'examine', it must break the topic down into individual components/processes and say how each one individually contributes to the question’s theme/topic and how the components/processes work together and interrelate. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question, mark scheme in ascending order of levels. Within each level there is a short overview of the skills and content needed, followed by a bullet point list of the indicative content (titled 'Indicative content guidance ') that could be applicable to each assessment objective, the AO's are indicated in brackets after each bullet point). Any short example points are bullet pointed and there's no need to write 'e.g' next to it. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        marks_scheme_prompts.append(prompt)
    return marks_scheme_prompts



def get_feedback_prompt(number_of_marks, question, answer, mark_scheme):
    prompt = '''Here is a question from a GCSE Edexcel iGCSE geography exam: "{}" . Here is the mark scheme: "{}". Here is an answer provided by a student: "{}". Imagine you are marking the answer to this question. Give a score out of {} marks and provide the student with feedback on how they could have achieved full marks. Don’t ever give ½ marks, they must be whole (though you don’t need to mention they are whole).  Make sure that for 4 mark questions, you allow two points that are developed as two marks per developed point. If a student‘s point is not directly referenced in the mark scheme, marks can still be given if it is in the specification and is relevant to the question. We have noticed in previous assessments on chat gpt that you were not giving full marks for answers that deserved it, so if you are going to give it nearly full marks, reassess your response carefully to see whether they have in fact included enough to warrant higher marks. Present it in the following format with these titles: Score: X out of Y, Feedback: What is needed to achieve full marks:. Do not write anything after this last section.' '''.format(question, mark_scheme, answer, number_of_marks)
    return prompt

def get_marks_prompts(questions):
    marks_scheme_prompts = []
    print("number of questions")
    print(len(questions))
    for question in questions:
        prompt = ''
        if question['number_of_marks'] == 2:
            prompt = [2, question['question'], '''The following is a Geography GCSE Edexcel iGCSE example exam question, which is worth 2 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, including maximum marks. Only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme including the assessment objectives that would be relevant to this question. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. For questions containing the command word 'identify' and 'suggest', include between 6-8 possible suggestions after the descriptions of the mark brackets, bullet pointed and briefly described in one sentence or less. Identify and describe questions are also only AO1 questions unless there is a figure or source, then they include AO2. For describe and explain questions, give an outline for the different marks followed by 5-6 suggestions for points that could be developed, briefly described in one sentence or less. For explain questions, a brief explanation is fine as long as it is relevant. Give the answer in the format: Title (Mark scheme), leave a line, specific assessment objectives assessed for this question, leave a line, mark scheme in ascending order of marks or levels. Leave a new line between each mark or level explanation.'''.format(question['question'])]
        elif question['number_of_marks'] == 4:
            prompt = [4, question['question'], '''The following is a Geography GCSE Edexcel iGCSE Geography example exam question, which is worth 4 mark(s): {}. Now, create a mark scheme for this question. It should first outline what an answer would need to demonstrate for a range of possible marks. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3) and the mark scheme will include 2 AO3 marks, otherwise don't include AO3. If the question includes the command word 'explain', answers should provide a reasoned explanation of how or why something occurs, it requires a justification/exemplification of a point. Marks can be given as one mark for identification and a second mark for development of this point, even if it is a simple point, for example a correct point followed by an explanation, justification, exemplification or cause of that point would get two marks. So full marks can be awarded for two relevant points that are both developed simply, answers do not need lots of depth, simple points should be awarded marks (make this explicit at the bottom of the mark scheme. If and only if the question says ‘explain two’ also add a statement saying that if only one point is made, no matter how developed it is, a maximum of 2 marks can be awarded). The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question and brief description of what is required for each, and disclaimer that there’s a maximum of two marks for each AO, then marking guidance on what is needed to get 1-2 or 2-4 marks as mentioned above (including detail and a simple example for the marker to differentiate between the two), then (only if the question asks for a named country or city) a disclaimer that says named countries or cities are not worth marks but are needed for full marks when mentioned in the question, then a bullet point list in brief noted format of content that could gain marks with a 1 in brackets after each point or development that could warrant a mark (include 5-8 points that would earn marks in brief note form). Any short example points are bullet pointed and there's no need to write 'e.g' next to it and no numbering should be used. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        elif question['number_of_marks'] == 6:
            prompt = [6, question['question'], '''The following is a Geography GCSE Edexcel iGCSE Geography example exam question, which is worth 6 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, in 3 bands of mark levels called 'levels'. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE  Geography mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3), otherwise don't include AO3. If the source or figure contains specific data, AO4 marks are available for geographical skills, interpreting the data and using it relevantly in the answer. If the question includes the command word 'explain', answers should provide a reasoned explanation of how or why something occurs, it requires a justification/exemplification of a point. If the question includes the command word 'assess' this means use evidence from the source or own knowledge to determine the relative significance of something, giving consideration to factors and identifying which are the most important. If a source is provided, information from this must be used to score high marks. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question, mark scheme in ascending order of levels. Within each level there is a short overview of the skills and content needed, followed by a bullet point list of the indicative content (titled 'Indicative content guidance ') that could be applicable to each assessment objective, the AO's are indicated in brackets after each bullet point. After the level 3 description include a note that says: To get level three, students do not need detailed examples or evidence, one example that is correct and relevant to the question is enough, unless it is a physical geography question, in which case examples are only needed if it is explicit in the question). Any short example points are bullet pointed and there's no need to write 'e.g' next to it. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        elif question['number_of_marks'] == 8:
            prompt = [8, question['question'], '''The following is a Geography GCSE Edexcel iGCSE example exam question, which is worth 8 mark(s): {}. Now, create a mark scheme for this question. It should outline what an answer would need to demonstrate for a range of possible marks, in 3 bands of mark levels called 'levels'. It should include maximum marks and only give whole marks, do not give marks for identifying countries alone, and do not write those two conditions into the mark scheme. Use your knowledge of previous Geography GCSE Edexcel iGCSE mark schemes when creating this mark scheme, it is important to include the assessment objectives that would be relevant to this question. If a source or figure is explicitly mentioned in the question, information from this must be used to score high marks (AO3), AO3 marks can also be received for using real world examples or case studies relevant to the question. If the source or figure contains specific data, AO4 marks are available for geographical skills, interpreting the data and using it relevantly in the answer. There are no marks for AO1 in any 8 mark question, and there are only AO2 marks available if there is no source or figure directly included in the question, if there is a source/figure, no AO2 marks or AO1 marks are available. If the question includes the command word 'analyse', top level marks must include evidence-based connections about the causes and effects or interrelationships between the components. If the question includes the command word 'evaluate', answers should measure the value or success of something and ultimately provide a substantiated judgement/conclusion, drawing on evidence such as strengths, weaknesses, alternatives and relevant data. If the question includes the command word 'examine', it must break the topic down into individual components/processes and say how each one individually contributes to the question’s theme/topic and how the components/processes work together and interrelate. The person using this mark scheme may not be familiar with the subject matter, so be very specific when describing what an answer would need to include to get the marks. For example, avoid something like "gives a detailed description of X", as the person using this mark scheme might not know the subject so you will really need to spell it out for them. You do not need to provide full example responses or multiple sentence examples, just key ideas within the levels. Leave a new line between each mark explanation. Give the answer in the format: Title (Mark scheme), specific assessment objectives assessed for this question, mark scheme in ascending order of levels. Within each level there is a short overview of the skills and content needed, followed by a bullet point list of the indicative content (titled 'Indicative content guidance ') that could be applicable to each assessment objective, the AO's are indicated in brackets after each bullet point). Any short example points are bullet pointed and there's no need to write 'e.g' next to it. Do not repeat content in multiple level descriptors.'''.format(question['question'])]
        marks_scheme_prompts.append(prompt)
    return marks_scheme_prompts

questions = get_questions()
marks_scheme_prompts = get_marks_prompts(questions)




file_name = ''

if use_gpt_4 == True:
    file_name = 'csvs/feedbackMarkschemes4.csv'
else:
    file_name = 'csvs/feedbackMarkschemes3.csv'


with open(file_name, 'w') as file:
    pass

questions_markschemes = []


with open(file_name, mode='a', newline='') as file:
    writer = csv.writer(file)
    print("number of prompts")
    print(len(marks_scheme_prompts))
    i = 0
    for prompt in marks_scheme_prompts:
        try:
            print('''generating mark scheme {}'''.format(str(i)))
            i = i+1
            start_time = time.time()
            mark_scheme = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(prompt[2]))['choices'][0]['message']["content"].strip().split('\n')
            end_time = time.time()
            elapsed_time_mark_scheme = end_time - start_time
            print(f"Markscheme OpenAI call took {elapsed_time_mark_scheme:.2f} seconds")
        except Exception as e:
            print(f"Problem generating markscheme: {e}")

        try:
            print('generating feedback')
            feedback_prompt = get_feedback_prompt(int(prompt[0]), prompt[1], prompt[2], mark_scheme)
            start_time = time.time()
            feedback = openai.ChatCompletion.create(**get_chat_gpt_options_string_single_message(feedback_prompt))['choices'][0]['message']["content"].strip().split('\n')
            end_time = time.time()
            elapsed_time_feedback = end_time - start_time
            print(f"Feedback OpenAI call took {elapsed_time_feedback:.2f} seconds")
            new_row = [int(prompt[0]), prompt[1], mark_scheme, prompt[2], feedback, elapsed_time_mark_scheme, elapsed_time_feedback]
            writer.writerow(new_row)
        except Exception as e:
            print(f"Problem with: {e}")        
