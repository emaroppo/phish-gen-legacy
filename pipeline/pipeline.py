from load import load_file, generate_paths_from_db
from cleaning import remove_corrupted_characters, remove_gt, remove_img_token
from parsing import extract_main_body, extract_main_headers, parse_string_multi
from pymongo import MongoClient
from tqdm import tqdm

import re

def parse_email_thread(txt_file):
    # Load file
    email = load_file(txt_file)

    # Parse main headers
    headers = extract_main_headers(email)
    body = extract_main_body(email)

    # Clean body
    body = remove_corrupted_characters(body)
    body = remove_gt(body)
    body = remove_img_token(body)

    # Parse body
    thread = parse_string_multi(body, headers)
    # Identify forwarded emails and who forwarded them
    thread = identify_forwarded_emails(thread)
    
    # Construct the relationships between emails
    for i in range(len(thread) - 1):  # stop at the second-to-last message
        # The 'reply_to' field indicates which email this one is a reply to,
        # based on the order in the list
        thread[i]['reply_to'] = i + 1  # using the index of the following message as identifier

    return thread

def identify_forwarded_emails(thread):
    forwarded_pattern = re.compile('[-\s]{3,}Forwarded\s+by\s+(?P<sender>.*)\s+on\s+(?P<datetime>(?P<date>[\d\/]{8,})\s+(?P<time>[\d:]{5,}\s+[AP]M))\s+-{2,}')

    for email in thread:
        match = forwarded_pattern.search(email['body'])
        if match:
            email['forwarded'] = True
            email['forwarded_by'] = match.group('sender')
        else:
            email['forwarded'] = False

    return thread

db= MongoClient("localhost", 27017).phish_gen_data_raw
email_paths = generate_paths_from_db(db,1000)
email_threads = []
for path in tqdm(email_paths):
    db.enron_dataset_test.insert_one({'thread':parse_email_thread(path)})

#save email threads to db in a new collection

