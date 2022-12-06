import re
import os
from clean_utils.regex_dict import regex_dict


def strip_body(thread_dict):
    thread_dict["head_message"]["body"] = thread_dict["head_message"]["body"].strip()
    for i in thread_dict["messages"]:
        i["body"] = i["body"].strip()
    return thread_dict


def remove_general_signature(body):
    signature = regex_dict["signatures"]["general"]
    body = re.sub(signature, r"[SIGNATURE]", body)
    return body


def remove_legal_signature(body):
    signature = regex_dict["signatures"]["legal"]
    body = re.sub(signature, r"[SIGNATURE]", body)
    return body
