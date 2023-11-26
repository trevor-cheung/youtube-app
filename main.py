import taipy as tp
import makequestions
import textToSpeech

from taipy import Config

input_name_data_node_cfg = Config.configure_data_node(id="input_name")
message_data_node_cfg = Config.configure_data_node(id="message")
questions_array_data_node_cfg = Config.configure_data_node(id="questions_array")
answers_array_data_node_cfg = Config.configure_data_node(id="answers_array")
qnum_data_node_cfg = Config.configure_data_node(id="qnum")


page = """
<|container|
# **linquiztics**{: .color-secondary}
<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|

<link|
## **Video**{: .color-primary} Link

<|{input_name}|input|label=Paste link here first!|>
<|submit|button|on_action=submit_scenario|>
|link>


<language|
## **Language**{: .color-primary}

<|{language}|selector|lov={[("en", "English"), ("sp", "Spanish"), ("ko", "Korean")]}|dropdown=True|>
|language>

<difficulty|
## Difficulty

<|{difficulty}|selector|lov={[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]}|dropdown=True|>
|difficulty>
|>

<br/> 

<|layout|columns=1|gap=30px|class_name=card|
### Question: 
<|{message}|text|>
<br/>
<|Play Text|button|on_action=play_speech|>
<br/>
<br/>
### Your Answer: 
<|{answer}|input|class_name=fullwidth|>
<br/>
<|{feedback}|text|>
<br/>
<|submit|button|on_action=submit_answer|>

<br/>
<|next|button|on_action=change_text|>
|>

|>

<style>
button {text-align: center;}
</style>
"""

input_name = None
message = None
language = 'en'
difficulty = None
answer = None
feedback = None

questions_array = []
answers_array = []

qnum = 0

stylekit = {
    # "color_primary": "#5C4230",
    # "color_secondary": "#8F2D24",
    # "color_background_light": "#7A6B62",
    # "color_background_dark": "#15130F",
    # "color_paper_light": "#F6F7F4",
    # "color_paper_dark": "#ABBFA9",
}

def submit_scenario(state):
    state.qnum = 0
    state.questions_array, state.answers_array = makequestions.linkToQs(state.input_name, state.language[1])
    state.message = state.questions_array[0]

def submit_answer(state):
    evaluation, feedback = makequestions.confidence(state.answer, state.answers_array[state.qnum])
    evaluation = int(evaluation)
    print(evaluation)
    print(feedback)
    if evaluation == 0:
        state.feedback = "Incorrect.\n"+feedback
    elif evaluation == 1:
        state.feedback = "Mostly correct.\n"+feedback
    elif evaluation == 2:
        state.feedback = "Correct!\n"+feedback
    
def change_text(state):
    state.qnum += 1
    if state.qnum >= len(state.questions_array):
        state.message = "No more questions!"
        return
    state.message = state.questions_array[state.qnum]
    state.answer = ""
    state.feedback = ""
    
def play_speech(state):
    state.message = state.questions_array[state.qnum]
    textToSpeech.playSpeech(state.message, state.language[0])


if __name__ == "__main__":
    tp.Core().run()
    tp.Gui(page).run(stylekit=stylekit)



