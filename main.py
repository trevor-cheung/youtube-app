import taipy as tp
import makequestions

from taipy import Config

def build_message(input: str):
    string = ''
    q, a = makequestions.linkToQs(input)
    for i in q:
        string += i + "\n"
    return string

input_name_data_node_cfg = Config.configure_data_node(id="input_name")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_name_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])


page = """
Name: <|{input_name}|input|>
<|submit|button|on_action=submit_scenario|>
Questions: <|{message}|text|>
"""

input_name = "Taipy"
message = None

def submit_scenario(state):
    state.scenario.input_name.write(state.input_name)
    state.scenario.submit(wait=True)
    state.message = scenario.message.read()

if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    tp.Gui(page).run()



