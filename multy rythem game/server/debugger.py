from PyInquirer import prompt


def ask_action():
    action_dict = {
        "type" : "list",
        "name" : "action",
        "message" : "What action do yo want to do?",
        "choices" : [
            "stop server",
            "get all of the server info",
            "get one key of the server info",
            "get_server_config",
            "set_server_config"
                    ]
    }
    answers = prompt(action_dict)
    return answers["action"]


def get_key_of_server_info(serverinfo : dict):
    action_dict = {
        "type" : "list",
        "name" : "action",
        "message" : "What key do you want to get?",
        "choices" : serverinfo.keys()
    }
    answers = prompt(action_dict)
    print(serverinfo.get(answers["action"]))



