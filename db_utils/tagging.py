from pymongo import MongoClient
from tqdm import tqdm
import json

with open("db_utils/format2tag_mapping.json") as f:
    mapping = json.load(f)


def post_attachment_tags_to_message(
    db, doc, tag, head_message=True, message_index=None
):

    if head_message:
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
    else:
        tag = [tag]
        if "tags" in doc["messages"][message_index]:
            if "[ATTACHMENT]" not in doc["messages"][message_index]["tags"]:
                tag += ["[ATTACHMENT]"]

            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$push": {
                        "messages." + str(message_index) + ".tags": {"$each": tag}
                    },
                },
            )
        else:
            tag += ["[ATTACHMENT]"]
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {"messages." + str(message_index) + ".tags": tag},
                },
            )


def tags_from_attachments(db, format_mapping=mapping, scope="all"):

    if scope == "head_message" or scope == "all":
        cursor = db.enron_dataset.find({"head_message.attachments": {"$exists": True}})
        for i in tqdm(cursor):
            for j in i["head_message"]["attachments"]:
                for k, v in format_mapping.items():
                    if j["file_format"] == k:
                        post_attachment_tags_to_message(db, i, v)

    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"attachments": {"$exists": True}}}}
        )

        for i in tqdm(cursor):
            for j, k in enumerate(i["messages"]):
                if "attachments" in k:
                    for l in k["attachments"]:
                        for m, n in format_mapping.items():
                            if l["file_format"] == m:
                                post_attachment_tags_to_message(
                                    db, i, n, head_message=False, message_index=j
                                )


def post_url_tag_to_message(db, doc, head_message=True, message_index=None):

    if head_message:
        if "tags" in doc["head_message"]:

            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$push": {"head_message.tags": {"$each": ["[URL]"]}},
                },
            )
        else:
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {"head_message.tags": ["LINK"]},
                },
            )
    else:
        if "tags" in doc["messages"][message_index]:

            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$push": {
                        "messages." + str(message_index) + ".tags": {"$each": ["[URL]"]}
                    },
                },
            )
        else:
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {"messages." + str(message_index) + ".tags": ["[URL]"]},
                },
            )


def tags_from_urls(db, scope="all"):

    if scope == "head_message" or scope == "all":
        cursor = db.enron_dataset.find({"head_message.urls": {"$exists": True}})

        for i in tqdm(cursor):
            post_url_tag_to_message(db, i)
    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"urls": {"$exists": True}}}}
        )
        for i in tqdm(cursor):
            for j, k in enumerate(i["messages"]):
                if "urls" in k:
                    post_url_tag_to_message(db, i, head_message=False, message_index=j)


def add_word_count(db, scope="all"):

    if scope == "head_message" or scope == "all":
        cursor = db.enron_dataset.find({"head_message.body": {"$exists": True}})

        for i in tqdm(cursor):
            db.enron_dataset.update_one(
                {"_id": i["_id"]},
                {
                    "$set": {
                        "head_message.word_count": len(
                            i["head_message"]["body"].split()
                        )
                    }
                },
            )

    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"body": {"$exists": True}}}}
        )
        for i in tqdm(cursor):
            for j, k in enumerate(i["messages"]):
                if "body" in k:
                    db.enron_dataset.update_one(
                        {"_id": i["_id"]},
                        {
                            "$set": {
                                "messages."
                                + str(j)
                                + ".word_count": len(k["body"].split())
                            }
                        },
                    )


def tag_html_documents(db, scope="all"):

    if scope == "head_message" or scope == "all":
        print(
            f'Found {db.enron_dataset.count_documents({"head_message.body": {"$regex": "<html>"}})} html documents in head_message'
        )
        cursor = db.enron_dataset.find({"head_message.body": {"$regex": "<html>"}})
        for i in tqdm(cursor):
            db.enron_dataset.update_one(
                {"_id": i["_id"]},
                {
                    "$set": {"head_message.is_html": True},
                },
            )
    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"body": {"$regex": "<html>"}}}}
        )
        for i in tqdm(cursor):
            for j, k in enumerate(i["messages"]):
                if "body" in k:
                    db.enron_dataset.update_one(
                        {"_id": i["_id"]},
                        {
                            "$set": {"messages." + str(j) + ".is_html": True},
                        },
                    )


client = MongoClient("localhost", 27017)
db = client.email

client.close()
