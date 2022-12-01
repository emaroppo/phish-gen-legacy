import re


def extract_headers(message):

    headers = dict()

    pattern_dict = dict()
    pattern_dict["from"] = r"From:\s*(.*)"
    pattern_dict["sent_datetime"] = (
        r"Sent:\s*(([A-z0-9,\s]+,\s*[0-9]{2,4})\s*([0-9]{1,2}:[0-9]{1,2} (AM|PM)))",
        r"Date:\s*([A-z0-9, \/:]*)",
    )
    pattern_dict["to"] = r"To:\s*((.*)(\n +.*)*)"
    pattern_dict["subject"] = r"Subject:\s*(.*\s*)"
    pattern_dict["importance"] = r"Importance:\s*([A-z0-9]*)"
    pattern_dict["cc"] = r"[Cc]{2}:(.*)"

    for i in pattern_dict.keys():
        if type(pattern_dict[i]) is str:
            if re.search(pattern_dict[i], message):
                headers[i] = re.search(pattern_dict[i], message).group(1)
                message = re.sub(pattern_dict[i], "", message)
        else:
            for j in pattern_dict[i]:
                if re.search(j, message):
                    headers[i] = re.search(j, message).group(1)
                    message = re.sub(j, "", message)

    return headers, message


def extract_head_headers(header_str):
    header_pattern = re.compile(r"[A-z-]*:((.*)(\n\t.*)*)")
    # extract all group 1 matches from header_str to a list
    results = header_pattern.findall(header_str)

    # attributes
    attributes = [
        "Message-ID",
        "Date",
        "From",
        "To",
        "Subject",
        "Mime-Version",
        "Content-Type",
        "Content-Transfer-Encoding",
        "X-From",
        "X-To",
        "X-cc",
        "X-bcc",
        "X-Folder",
        "X-Origin",
    ]

    # convert list of tuples to list of lists
    headers = dict()
    for i, j in zip(attributes, results):
        headers[i] = j[0]
    return headers


def extract_forwarded(message):
    """Extract forwarded message from a message."""

    forward_pattern = "-{3,}\s*Forwarded[\s\n]by\s*([A-z0-9\/\.\s_]+)[\s\n]on\s*(([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})\s*([0-9]{1,2}:[0-9]{1,2}\s*(PM|AM)))\s*-{3,}"

    if re.search(forward_pattern, message):

        results = re.split(forward_pattern, message)

        forwarded_message = dict()
        forwarded_message["headers"] = dict()
        forwarded_message["headers"], forwarded_message["body"] = extract_headers(
            results[-1]
        )
        forwarded_message["headers"]["fw_by"] = results[1]
        forwarded_message["headers"]["fw_date"] = results[3]
        forwarded_message["headers"]["fw_time"] = results[4].replace("\n", "\s")

        message = results[0]

        return message, forwarded_message

    else:
        return message, None


def separate_thread(json_thread, email, email_header):
    email = email.split("-----Original Message-----")

    json_thread["head_message"] = dict()
    json_thread["head_message"]["headers"] = extract_head_headers(email_header)
    json_thread["head_message"]["body"], forwarded_message = extract_forwarded(
        email.pop(0)
    )

    if forwarded_message:
        json_thread["messages"].append(forwarded_message)

    if email:
        for j in range(len(email)):
            original_message = dict()

            message, forwarded_message = extract_forwarded(email[j])

            if forwarded_message:
                json_thread["messages"].append(forwarded_message)

            original_message["headers"], original_message["body"] = extract_headers(
                message
            )
            json_thread["messages"].append(original_message)

    return json_thread
