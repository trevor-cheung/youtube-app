import json
import requests
import config
import re
from youtube_transcript_api import YouTubeTranscriptApi


def link_to_transcript(link): # takes link, returns transcript
    video_id = link.replace('https://www.youtube.com/watch?v=', '')
    script = YouTubeTranscriptApi.get_transcript(video_id)
    return script


def generate_questions(transcript): # takes transcript, returns q/a as str
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+config.openai_key,
    }

    json_data = {
        'model': 'gpt-3.5-turbo-1106',
        'messages': [
            {
                'role': 'user',
                'content': f'Write a set of questions in English based on the script to test a reader\'s comprehension of the script. Include answers to the question. Preceed each question with \'Q:\' and each answer with \'A:\'\nTranscript: \n{transcript}',
            },
        ],
        'temperature': 0.5,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    response_dict = json.loads(response.text)
    
    # print(response_dict)  

    return(response_dict['choices'][0]['message']['content'])


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

def linkToQs(link): # takes link, returns q/a arrays
    return Q_and_A_arrays(generate_questions(link_to_transcript(link)))

# link = "https://www.youtube.com/watch?v=sbIQLzieUq8"

# qs, ans = linkToQs(link)





