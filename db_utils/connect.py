from pymongo import MongoClient
import re
from clean_utils.clean import remove_signature
from clean_utils.regex_dict import regex_dict
from tqdm import tqdm

# create a connection to the local Mongo database

client = MongoClient("localhost", 27017)
db = client.email

# count matching the filter criteria
def clean_general_signature_db(db):
    count = db.enron_dataset.count_documents(
        {
            "head_message.body": {
                "$regex": regex_dict["signatures"]["general"]
            }
        }
    )
    for i in tqdm(range(count)):
        # find the first matching document
        doc = db.enron_dataset.find_one(
            {
                "head_message.body": {
                    "$regex": regex_dict["signatures"]["general"]
                }
            }
        )
        # update the document
        db.enron_dataset.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "head_message.body": remove_signature(doc["head_message"]["body"])
                }
            },
        )


def clean_legal_signature_db(db):
    count = db.enron_dataset.count_documents(
        {
            "head_message.body": {
                "$regex": regex_dict["signatures"]["legal"]
            }
        }
    )
    for _ in tqdm(range(count)):
        # find the first matching document
        doc = db.enron_dataset.find_one(
            {
                "head_message.body": {
                    "$regex": regex_dict["signatures"]["legal"]
                }
            }
        )
        # update the document
        if "tags" in doc["head_message"]:
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "head_message.body": remove_signature(doc["head_message"]["body"]),
                    }
                    "$push": {"head_message.tags": r"[LEGAL]"}
                },
            )
        else:
            db.enron_dataset.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "head_message.body": remove_signature(doc["head_message"]["body"]),
                        "head_message.tags":[r"[LEGAL]"]
                    }
                },
            )

print(matches)
