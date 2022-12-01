def strip_body(thread_dict):
    thread_dict["head_message"]["body"] = thread_dict["head_message"]["body"].strip()
    for i in thread_dict["messages"]:
        i["body"] = i["body"].strip()
    return thread_dict
