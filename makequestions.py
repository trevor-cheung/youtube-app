import json
import requests
import config as config
import re
from youtube_transcript_api import YouTubeTranscriptApi

def chatgpt(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+config.openai_key,
    }

    json_data = {
        'model': 'gpt-3.5-turbo-1106',
        'messages': [
            {
                'role': 'user',
                'content': f'{prompt}',
            },
        ],
        'temperature': 0.5,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    response_dict = json.loads(response.text)
    
    # print(response_dict)  

    return(response_dict['choices'][0]['message']['content'])

def link_to_transcript(link): # takes link, returns transcript
    video_id = link.replace('https://www.youtube.com/watch?v=', '')
    script = YouTubeTranscriptApi.get_transcript(video_id)
    return script


def generate_questions(transcript, lang): # takes transcript and language, returns q/a as str
    if(lang == 'English'):
        prompt = f"Write a set of questions in English based on the following transcript to test a reader\'s comprehension of the script. Include answers to the question. Preceed each question with \'Q:\' and each answer with \'A:\'\nTranscript: \n{transcript}"
    else:
        prompt = f"Write a set of questions in {lang} based on the transcript to test a reader\'s comprehension of the script. Include answers to the question. Preceed each question with \'Q:\' and each answer with \'A:\'\nTranscript: \n{transcript}"

    return chatgpt(prompt)


def Q_and_A_arrays(str): # takes str, return q/a arrays
    QandA = re.split("Q: |A: ", str)
    # instead of using re library, we can replace all "Q: " with "A: ", leaving only "A: "s and splitting it normally with "A: " as the transactor. i think that is slower though.
    qs = []
    ans = []
    QandA.pop(0) # remove blank one

    for i in range(len(QandA)):
        if (i%2==0):
            qs.append(QandA[i])
        else:
            ans.append(QandA[i])
    
    for i in range(len(qs)):
        print("Question: "+qs[i]+"\n")
        print("Answer: "+ans[i]+"\n")
    
    return qs, ans

def linkToQs(link, lang): # takes link, returns q/a arrays
    return Q_and_A_arrays(generate_questions(link_to_transcript(link), lang))

def confidence(string, ans): # gives two values: evaluation number as int and feedback as string.
    prompt = f"Compare how accurate the following response is to the actual answer. Evaluate leniently with regard to specific specific wording - it is more important that the individual understands the general idea. \nIf the response is mostly accurate with few errors, say \'2\'. If the response is somewhat accurate with some errors and/or some missing ideas, say \'1\'. If the response is mostly or completely incorrect, say \'0\'. \n Begin by saying the evaluation number (e.g 0,1,2) followed by an explanation for why you gave that evaluation. Speak as if you are speaking directly to the respondent. \nResponse: {string}\nActual answer: {ans}\n"
    output = chatgpt(prompt)
    evaluation = output[0]
    feedback = output.replace(str(evaluation), "", 1)
    return evaluation, feedback.strip()
        

# link = "https://www.youtube.com/watch?v=sbIQLzieUq8"

# qs, ans = linkToQs(link, False)

# conf, feedback = confidence("theshy said he should have been more reckless in the beginning and that he could have possibly won in that first gank if he had been more aggressive", "TheShy regrets not being more reckless during the first phase when the enemy team went for a top gank. He feels he could have been more aggressive and potentially won that attempt.")
# print(conf+"\n"+feedback)