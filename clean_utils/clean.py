import os
import re

from pymongo import MongoClient

from clean_utils.regex_dict import regex_dict

client = MongoClient("localhost", 27017)
db = client.email


def remove_corrupted_characters(body):
    body = re.sub(r"(=09|=20|=01|=\n)", r"", body)
    return body


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


def remove_img_token(body):
    return body.replace("[IMAGE]", "").strip()


def retrieve_subject(body):
    subj_match = re.match(r"Subject:(.*)\n", body, re.IGNORECASE)

    if subj_match:
        subject = subj_match.group(1).strip()
        body = re.sub(r"Subject:(.*)\n", "", body)

        return body, subject

    else:
        return body, None


# remove signature functions are useless duplicates now, reminder to self to remove one (or both?) :0
