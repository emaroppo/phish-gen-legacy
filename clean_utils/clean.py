import re
import os


def strip_body(thread_dict):
    thread_dict["head_message"]["body"] = thread_dict["head_message"]["body"].strip()
    for i in thread_dict["messages"]:
        i["body"] = i["body"].strip()
    return thread_dict


def remove_signature(body):
    signature = r"Enron North America Corp\.\s([0-9]*\s[A-z\s]*,\s[A-z0-9\s]*\s)([A-z]*,\s[A-z]*\s+)[0-9]*\s([0-9]*-[0-9]*-[0-9]*\s)\(phone\)\s([0-9]*-[0-9]*-[0-9]*\s)\(fax\)\s([A-z.]*@enron.com)"
    body = re.sub(signature, r"[SIGNATURE]", body)
    return body


print(os.getcwd())
