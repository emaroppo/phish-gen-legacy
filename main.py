from emails.email_obj import EMail
from pipeline.load import generate_paths_from_folder
from tqdm import tqdm
from pymongo import MongoClient

# connect to database
client = MongoClient("localhost", 27017)
db = client.email1


# generate file paths
paths = generate_paths_from_folder("datasets/maildir")
error_counter = dict()
error_counter["unicodedecodeerror"] = 0
for i in tqdm(paths):
    try:
        email = EMail.from_txt(i)
    except UnicodeDecodeError:
        error_counter["unicodedecodeerror"] += 1
        continue
    email.save(db)




print(error_counter)
