import re
import os
from clean_utils.regex_dict import regex_dict
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.email


def strip_body(thread_dict):
    thread_dict["head_message"]["body"] = thread_dict["head_message"]["body"].strip()
    for i in thread_dict["messages"]:
        i["body"] = i["body"].strip()
    return thread_dict


def remove_general_signature(body, signature):
    body = re.sub(signature, r"[SIGNATURE]", body)
    return body


def remove_legal_signature(body, signature):
    body = re.sub(signature, r"[SIGNATURE]", body)
    return body


def remove_gt(body):
    body = body.split("\n")
    new_body = []
    for i in body:
        new_body.append(i.lstrip("> "))
    new_body = "\n".join(new_body)
    return new_body


x = db.enron_dataset.find_one({"head_message.body": {"$regex": "\n>"}})
print(x["head_message"]["body"])

x["head_message"]["body"] = remove_gt(x["head_message"]["body"])
print(strip_body(x))

print(x["head_message"]["body"])

# remove signature functions are useless duplicates now, reminder to self to remove one (or both?) :0
