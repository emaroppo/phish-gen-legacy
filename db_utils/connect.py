from pymongo import MongoClient
import re
from clean_utils.clean import remove_general_signature, remove_legal_signature
from clean_utils.regex_dict import regex_dict, get_attachment_regex_dict
from tqdm import tqdm


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


def post_attachments(db, doc_, attachment, scope="all", array_index=None):
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


def extract_attachments_obj(
    db,
    format_list=get_attachment_regex_dict("file_formats.json"),
    scope="all",
    replacement_token=False,
):

    if scope == "head_message" or scope == "all":
        for i in tqdm(format_list):
            for j in i:

                print(f"Looking for .{j} attachments...")

                try:
                    cursor = db.enron_dataset.find(
                        {"head_message.body": {"$regex": j, "$options": "i"}}
                    )
                    if cursor:
                        for k in tqdm(cursor):
                            body = k["head_message"]["body"]
                            match = re.findall(j, body, flags=re.IGNORECASE)
                            if replacement_token:
                                new_body = re.sub(
                                    j, r"[FILE]", body, flags=re.IGNORECASE
                                )
                            else:
                                new_body = body

                            attachments = [
                                {"file": k[0], "file_name": k[1], "file_format": k[2]}
                                for k in match
                            ]
                            k["head_message"]["body"] = new_body

                            post_attachments(db, k, attachments)

                except TypeError:
                    pass

    if scope == "messages" or scope == "all":
        for i in format_list:

            for j in i:

                print(f"Looking for .{j} attachments...")
                try:

                    cursor = db.enron_dataset.find(
                        {
                            "messages": {
                                "$elemMatch": {"body": {"$regex": j, "$options": "i"}}
                            }
                        }
                    )
                    if cursor:
                        for k in tqdm(cursor):
                            for l in k["messages"]:
                                body = l["body"]
                                match = re.findall(j, body, flags=re.IGNORECASE)
                                if replacement_token:
                                    new_body = re.sub(
                                        j, r"[FILE]", body, flags=re.IGNORECASE
                                    )
                                else:
                                    new_body = body
                                if match:
                                    attachments = [
                                        {
                                            "file": k[0],
                                            "file_name": k[1],
                                            "file_format": k[2],
                                        }
                                        for k in match
                                    ]
                                    l["body"] = new_body
                                    post_attachments(
                                        db, k, attachments, scope="messages"
                                    )

                except TypeError as e:
                    print(e)
                    pass


def post_urls(db, doc_, urls=[], scope="all"):
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


def extract_urls_obj(db, scope="all", replacement_token=True):

    if scope == "head_message" or scope == "all":

        cursor = db.enron_dataset.find(
            {"head_message.body": {"$regex": regex_dict["url"]}}
        )

        for i in tqdm(cursor):
            body = i["head_message"]["body"]
            match = re.findall(regex_dict["url"], body)
            urls = [k for k in match]
            if replacement_token:
                new_body = re.sub(
                    regex_dict["url"], r"[URL]", body, flags=re.IGNORECASE
                )
            else:
                new_body = body
            i["head_message"]["body"] = new_body
            post_urls(db, i, urls, scope="head_message")

    if scope == "messages" or scope == "all":
        cursor = db.enron_dataset.find(
            {"messages": {"$elemMatch": {"body": {"$regex": regex_dict["url"]}}}}
        )

        for i in tqdm(cursor):
            for j in i["messages"]:
                body = j["body"]
                match = re.findall(regex_dict["url"], body)

                if replacement_token:
                    new_body = re.sub(
                        regex_dict["url"], r"[URL]", body, flags=re.IGNORECASE
                    )
                else:
                    new_body = body

                if match:
                    j["urls"] = [k for k in match]
                    j["body"] = new_body
                    post_urls(db, i, scope="messages")
