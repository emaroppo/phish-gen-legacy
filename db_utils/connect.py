from pymongo import MongoClient
import re
from clean_utils.clean import remove_general_signature, remove_legal_signature
from clean_utils.regex_dict import regex_dict, get_attachment_regex_dict
from tqdm import tqdm
import os
import json

# create a connection to the local Mongo database

client = MongoClient("localhost", 27017)
db = client.email

# count matching the filter criteria
def clean_general_signature_db(db):

    for i in regex_dict["signatures"]["general"]:
        count = db.enron_dataset.count_documents({"head_message.body": {"$regex": i}})
        for _ in tqdm(range(count)):
            # find the first matching document
            doc = db.enron_dataset.find_one({"head_message.body": {"$regex": i}})
            # update the document
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "head_message.body": remove_general_signature(
                            doc["head_message"]["body"], i
                        )
                    }
                },
            )


def clean_legal_signature_db(db):

    for i in regex_dict["signatures"]["legal"]:
        count = db.enron_dataset.count_documents({"head_message.body": {"$regex": i}})
        for _ in tqdm(range(count)):
            # find the first matching document
            doc = db.enron_dataset.find_one({"head_message.body": {"$regex": i}})

            # update the document
            if "tags" in doc["head_message"]:
                db.enron_dataset.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "head_message.body": remove_legal_signature(
                                doc["head_message"]["body"], i
                            )
                        },
                        "$push": {"head_message.tags": r"[LEGAL]"},
                    },
                )
            else:
                db.enron_dataset.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "head_message.body": remove_legal_signature(
                                doc["head_message"]["body"], i
                            ),
                            "head_message.tags": [r"[LEGAL]"],
                        }
                    },
                )


# write a function to export all the "body" fields from the "head_message" fields and the "messages" field to a folder
def export_body(db, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for k, doc in enumerate(tqdm(db.enron_dataset.find())):
        with open(folder + str(k) + ".txt", "w") as f:
            f.write(doc["head_message"]["body"])
        for i, j in enumerate(doc["messages"]):
            with open(folder + str(k) + "_" + str(i) + ".txt", "w") as f:
                f.write(j["body"])


def add_attachment(db, doc_, attachment, scope="all", array_index=None):
    if scope == "head_message" or scope == "all":
        if "attachments" in doc_["head_message"]:
            db.enron_dataset.update_one(
                {"_id": doc_["_id"]},
                {
                    "$set": {"head_message.body": doc_["head_message"]["body"]},
                    "$push": {"head_message.attachments": {"$each": attachment}},
                },
            )
        else:
            db.enron_dataset.update_one(
                {"_id": doc_["_id"]},
                {
                    "$set": {
                        "head_message.body": doc_["head_message"]["body"],
                        "head_message.attachments": attachment,
                    }
                },
            )
    if scope == "messages" or scope == "all":

        db_entry = db.enron_dataset.find_one({"_id": doc_["_id"]})
        for i, j in enumerate(doc_["messages"]):

            if "attachments" in db_entry["messages"][i]:
                db.enron_dataset.update_one(
                    {"_id": doc_["_id"]},
                    {
                        "$set": {f"messages.{i}.body": j["body"]},
                        "$push": {f"messages.{i}.attachments": {"$each": attachment}},
                    },
                )
            else:
                db.enron_dataset.update_one(
                    {"_id": doc_["_id"], "messages": j},
                    {
                        "$set": {
                            f"messages.{i}.body": j["body"],
                            f"messages.{i}.attachments": attachment,
                        },
                    },
                )


def extract_attachments(
    db, format_list=get_attachment_regex_dict("file_formats2.json"), scope="all"
):

    if scope == "head_message" or scope == "all":
        for i in format_list:
            for j in i:
                try:
                    cursor = db.enron_dataset.find({"head_message.body": {"$regex": j}})
                    for k in tqdm(cursor):
                        body = k["head_message"]["body"]
                        match = re.findall(j, body)
                        attachments = [
                            {"file": k[0], "file_name": k[1], "file_format": k[2]}
                            for k in match
                        ]
                        k["head_message"]["body"] = re.sub(j, r"[FILE]", body)
                        add_attachment(db, k, attachments)

                except TypeError:
                    pass

    if scope == "messages" or scope == "all":
        for i in format_list:
            for j in i:
                try:
                    cursor = db.enron_dataset.find(
                        {"messages": {"$elemMatch": {"body": {"$regex": j}}}}
                    )
                    for k in tqdm(cursor):
                        for l in k["messages"]:
                            body = l["body"]
                            match = re.findall(j, body, re.IGNORECASE)
                            if match:
                                attachments = [
                                    {
                                        "file": k[0],
                                        "file_name": k[1],
                                        "file_format": k[2],
                                    }
                                    for k in match
                                ]
                                l["body"] = re.sub(j, r"[FILE]", body)
                                add_attachment(db, k, attachments, scope="messages")

                except TypeError as e:
                    print(e)
                    pass


def add_url(db, doc_, urls=[], scope="all"):
    if scope == "head_message" or scope == "all":
        if "urls" in doc_["head_message"]:
            db.enron_dataset.update_one(
                {"_id": doc_["_id"]},
                {
                    "$set": {"head_message.body": doc_["head_message"]["body"]},
                    "$push": {"head_message.urls": {"$each": urls}},
                },
            )
        else:
            db.enron_dataset.update_one(
                {"_id": doc_["_id"]},
                {
                    "$set": {
                        "head_message.body": doc_["head_message"]["body"],
                        "head_message.urls": urls,
                    }
                },
            )
    if scope == "messages" or scope == "all":
        db.enron_dataset.update_one(
            {"_id": doc_["_id"]},
            {
                "$set": {
                    "messages": doc_["messages"],
                }
            },
        )


def extract_urls(db, scope="all"):

    if scope == "head_message" or scope == "all":

        cursor = db.enron_dataset.find(
            {"head_message.body": {"$regex": regex_dict["url"]}}
        )

        for i in tqdm(cursor):
            body = i["head_message"]["body"]
            match = re.findall(regex_dict["url"], body)
            urls = [k for k in match]
            i["head_message"]["body"] = re.sub(regex_dict["url"], r"[URL]", body)
            add_url(db, i, urls)

    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"body": {"$regex": regex_dict["url"]}}}}
        )
        for i in tqdm(cursor):
            for j in i["messages"]:
                body = j["body"]
                match = re.findall(regex_dict["url"], body)
                if match:
                    j["urls"] = [k for k in match]
                    j["body"] = re.sub(regex_dict["url"], r"[URL]", body)
                    add_url(db, i, scope="messages")


def add_attachment_tags_to_head_message(db, doc, tag):
    tag = [tag]

    if "tags" in doc["head_message"]:
        if "[ATTACHMENT]" not in doc["head_message"]["tags"]:
            tag += ["[ATTACHMENT]"]

        db.enron_dataset.update_one(
            {"_id": doc["_id"]},
            {
                "$push": {"head_message.tags": {"$each": tag}},
            },
        )
    else:
        tag += ["[ATTACHMENT]"]
        db.enron_dataset.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {"head_message.tags": tag},
            },
        )


def add_url_tag_to_head_message(db, doc, tag):
    tag = [tag]

    if "tags" in doc["head_message"]:

        db.enron_dataset.update_one(
            {"_id": doc["_id"]},
            {
                "$push": {"head_message.tags": {"$each": tag}},
            },
        )
    else:
        db.enron_dataset.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {"head_message.tags": tag},
            },
        )


extract_attachments(db, scope="head_message")

cursor = db.enron_dataset.find({"head_message.attachments": {"$exists": True}})

for i in tqdm(cursor):
    for j in i["head_message"]["attachments"]:
        if j["file_format"] == "xls":
            add_attachment_tags_to_head_message(db, i, "[EXCEL]")
        if j["file_format"] == "doc":
            add_attachment_tags_to_head_message(db, i, "[WORD]")
        if j["file_format"] == "pps":
            add_attachment_tags_to_head_message(db, i, "[POWERPOINT]")
        if j["file_format"] == "ppt":
            add_attachment_tags_to_head_message(db, i, "[POWERPOINT]")
        if j["file_format"] == "pdf":
            add_attachment_tags_to_head_message(db, i, "[PDF]")
"""
cursor = db.enron_dataset.find(
 {"messages": {"$elemMatch": {"urls": {"$exists": True}}}}
)

for i in tqdm(cursor):
    for j, k in enumerate(i["messages"]):
        if "urls" in k:
            if "tags" not in k:
                k["tags"] = list()
            k["tags"].append("[URL]")
            db.enron_dataset.update_one(
                {"_id": i["_id"]}, {"$set": {f"messages.{j}": k}}
            )
"""

extract_attachments(db, scope="messages")

cursor = db.enron_dataset.find(
    {"messages": {"$elemMatch": {"attachments": {"$exists": True}}}}
)

for i in tqdm(cursor):
    for j, k in enumerate(i["messages"]):
        k["tags"] = set()

        if "attachments" in k:
            for l in k["attachments"]:
                if l["file_format"] == "xls":
                    k["tags"].add("[ATTACHMENT]")
                    k["tags"].add("[EXCEL]")
                if l["file_format"] == "doc":
                    k["tags"].add("[ATTACHMENT]")
                    k["tags"].add("[WORD]")
                if l["file_format"] == "pps":
                    k["tags"].add("[ATTACHMENT]")
                    k["tags"].add("[POWERPOINT]")
                if l["file_format"] == "ppt":
                    k["tags"].add("[ATTACHMENT]")
                    k["tags"].add("[POWERPOINT]")
                if l["file_format"] == "pdf":
                    k["tags"].add("[ATTACHMENT]")
                    k["tags"].add("[PDF]")
            k["tags"] = list(k["tags"])
            db.enron_dataset.update_one(
                {"_id": i["_id"]}, {"$set": {f"messages.{j}": k}}
            )
