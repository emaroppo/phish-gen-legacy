import os
from tqdm import tqdm
from pymongo import MongoClient
from email import policy
from email.parser import BytesParser

# generate file paths
def generate_paths_from_folder(folder):
    paths = []
    for root, dirs, files in tqdm(os.walk(folder)):
        for file in files:
            if file[0] != ".":
                paths.append(os.path.join(root, file))
    return paths

def load_file(path):
    with open(path, "rb") as file:
            email_thread = BytesParser(policy=policy.default).parse(file)
    return email_thread

def generate_paths_from_db(db, max_count=None):
    paths = []
    for i in tqdm(db.enron_dataset.find(limit=max_count)):
        paths.append(i["path"])
    return paths

def create_raw_db():
    paths = generate_paths_from_folder("datasets/maildir")
    entries=list()
    errored_paths=list()

    for i in tqdm(paths):
        try:
            with open(i, "r") as f:
                entries.append({"path": i, "content": f.read()})
        except:
            errored_paths.append(i)
            if len(errored_paths) % 1000 == 0:
                print(f"Errored paths: {len(errored_paths)}")
        
    #create phish_gen_data_raw db in mongo
    client = MongoClient()
    db = client.phish_gen_data_raw

    #create enron_dataset collection in phish_gen_data_raw db
    collection = db.enron_dataset

    #insert entries into enron_dataset collection
    collection.insert_many(entries)

    #check that entries were inserted
    print(collection.count_documents({}))
    print(len(errored_paths))