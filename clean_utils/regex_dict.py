import json

regex_dict = {
    "signatures": {
        "general": (
            r"Enron\s*North\s*America\s*Corp\.\s*([0-9]*\s[A-z\s]*,\s[A-z0-9\s]*\s)([A-z]*,\s[A-z]*\s+)[0-9]*\s([0-9]*-[0-9]*-[0-9]*\s)\(phone\)\s([0-9]*-[0-9]*-[0-9]*\s)\(fax\)\s([A-z.]*@enron.com)",
            r"Enron North America Corp\.\s*1400\s*Smith\s*Street\s*EB\s*824\s*Houston,\s*Texas\s*77002\s*Phone:\s*\(713\)\s*853-1575\s*Fax:\s*\(713\)\s*646-3490\s*",
        ),
        "legal": (
            r"Enron North America Corp\.\s*Legal\s*Department\s*1400\s*Smith\s*Street,\s*EB\s*3885\s*Houston,\s*Texas\s*77002",
            r"Enron North America Corp\.\s*1400\s*Smith,\s*38th Floor,\s*Legal\s*Houston,\s*Texas\s*77002-7361\s*\(713\)\s*345-7732\s*\(713\)\s*646-3393\s*\(fax\)",
        ),
    },
    "head_headers": r"[A-z-]*:((.*)(\n\t.*)*)",
    "headers": {
        "from": r"From:\s*(.*)",
        "sent_datetime": (
            r"Sent:\s*(([A-z0-9,\s]+,\s*[0-9]{2,4})\s*([0-9]{1,2}:[0-9]{1,2} (AM|PM)))",
            r"Date:\s*([A-z0-9, \/:]*)",
        ),
        "to": r"To:\s*((.*)(\n +.*)*)",
        "subject": r"Subject:\s*(.*\s*)",
        "importance": r"Importance:\s*([A-z0-9]*)",
        "cc": r"[Cc]{2}:(.*)",
    },
    "forwarded": r"-{3,}\s*Forwarded[\s\n]by\s*([A-z0-9\/\.\s_]+)[\s\n]on\s*(([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})\s*([0-9]{1,2}:[0-9]{1,2}\s*(PM|AM)))\s*-{3,}",
    "url": r"((?:http|https|ftp|ftps):\/\/[A-z0-9\.\/\?=&_\-]+)",
}


def get_attachment_regex_dict(format_file):

    with open(format_file, "r") as f:
        file_list = json.load(f)

    format_list = []

    for i in file_list.keys():
        format_list += file_list[i]

    attachment_regex_dict = [
        (
            r"\(See attached file: (([\-\w\s!&.()#]*)\.({})\))".format(i),
            r"<<(([\-\w\s!.&'()#]*)\.({}))>>".format(i),
            r" - (([\-\w\s!&'.()#]*)\.({}))".format(i),
        )
        for i in format_list
    ]
    return attachment_regex_dict


# TO DO: attempt to generalise regexes
# TO DO: add regexes for forwarded messages
# TO DO: add regexes for messages in threads mot yet captured
