import json
from clean_utils.parsing import separate_thread
from clean_utils.clean import strip_body


def txt_to_json(thread_id, thread, thread_header, to_file=True, json_path=None):
    json_thread = dict()
    json_thread["thread_id"] = thread_id
    json_thread["messages"] = list()
    json_thread = separate_thread(json_thread, thread, thread_header)

    if to_file:
        with open(json_path, "w") as file:
            json.dump(json_thread, file, indent=4)

    return json_thread


def bodies_to_txts(thread_dict, to_file=True, txt_path=None, clean=True):

    if clean:
        thread_dict = strip_body(thread_dict)

    head_message = thread_dict["head_message"]["body"]
    message_bodies = [i["body"] for i in thread_dict["messages"]]

    if to_file and head_message:
        with open(txt_path + "_head.txt", "w") as file:
            file.write(head_message)

    if message_bodies:
        for i, j in enumerate(message_bodies):
            if j:
                with open(txt_path + str(i) + ".txt", "w") as file:
                    file.write(j)

    return head_message, message_bodies
