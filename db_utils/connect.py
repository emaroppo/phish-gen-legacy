from pymongo import MongoClient
import re
from clean_utils.clean import remove_signature

# create a connection to the local Mongo database

client = MongoClient("localhost", 27017)
db = client.email

# count matching the filter criteria
def clean_signature_db():
    count = db.enron_dataset.count_documents(
        {
            "head_message.body": {
                "$regex": r"Enron North America Corp\.\s([0-9]*\s[A-z\s]*,\s[A-z0-9\s]*\s)([A-z]*,\s[A-z]*\s+)[0-9]*\s([0-9]*-[0-9]*-[0-9]*\s)\(phone\)\s([0-9]*-[0-9]*-[0-9]*\s)\(fax\)\s([A-z.]*@enron.com)"
            }
        }
    )
    while count:
        # find the first matching document
        doc = db.enron_dataset.find_one(
            {
                "head_message.body": {
                    "$regex": r"Enron North America Corp\.\s([0-9]*\s[A-z\s]*,\s[A-z0-9\s]*\s)([A-z]*,\s[A-z]*\s+)[0-9]*\s([0-9]*-[0-9]*-[0-9]*\s)\(phone\)\s([0-9]*-[0-9]*-[0-9]*\s)\(fax\)\s([A-z.]*@enron.com)"
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
        # print the count of remaining documents

        count -= 1
        print(count)


matches = db.enron_dataset.count_documents(
    {
        "head_message.body": {
            "$regex": r"Enron North America Corp.\nLegal Department\n1400 Smith Street, EB 3885\nHouston, Texas 77002"
        }
    }
)

print(matches)
