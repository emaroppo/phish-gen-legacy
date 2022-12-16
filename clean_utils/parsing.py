import re

from iteration_utilities import deepflatten

from clean_utils.regex_dict import regex_dict


def extract_headers(message):

    headers = dict()

    pattern_dict = regex_dict["headers"]

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


def extract_headers(message):
    message = "\n" + (message.strip())

    if re.search(regex_dict["headers2"]["find2"], message, flags=re.IGNORECASE):
        headers = re.findall(
            regex_dict["headers2"]["capture2"],
            re.search(
                regex_dict["headers2"]["find2"], message, flags=re.IGNORECASE
            ).group(0)
            + "\n",
            flags=re.IGNORECASE,
        )

        try:
            headers = [tuple(i for i in j if i) for j in headers]
            headers = {k.strip().lower(): v.strip() for k, v in headers}
            message = re.sub(
                regex_dict["headers2"]["find2"], "", message, flags=re.IGNORECASE
            )

        except ValueError:

            message = "\n" + (message.strip())
            results = re.match(
                regex_dict["headers2"]["no_lookbehind"], message, re.IGNORECASE
            )

            if not results:
                if message[1] == "<":
                    message = "\n " + message
                else:
                    message = [i.strip() for i in message.split("\n")]
                    message = "\n".join(message)
                results = re.match(
                    regex_dict["headers2"]["no_lookbehind"], message, re.IGNORECASE
                )

            headers = results.groupdict()
            while results:
                # print(headers)
                headers = {k: v for k, v in headers.items() if v is not None}
                if "header" in headers.keys():
                    headers[headers["header"].lower()] = headers["header_value"]
                    del headers["header"]
                    del headers["header_value"]

                message = re.sub(
                    regex_dict["headers2"]["no_lookbehind"],
                    "\n",
                    message.strip(),
                    count=1,
                    flags=re.IGNORECASE,
                ).strip()

                results = re.match(
                    regex_dict["headers2"]["no_lookbehind"], message, re.IGNORECASE
                )

        return headers, message

    else:
        return None, message


def split_on_headers(message):
    message = "\n" + (message.strip())
    if re.search(regex_dict["headers2"]["find2"], message, flags=re.IGNORECASE):
        headers = re.findall(
            regex_dict["headers2"]["capture2"], message, flags=re.IGNORECASE
        )

        headers_obj = []
        header = dict()
        for i in headers:

            if i[0]:
                header["from"] = i[0]
            if i[1]:
                header["date"] = i[1]
            if i[2]:
                header["time"] = i[2]
            if i[3]:
                header["from"] = i[3]
            if i[4]:
                header["date"] = i[4]
            if i[5]:
                header["time"] = i[5]

            if i[-2].lower() not in header.keys():
                header[i[-2].lower()] = i[-1]
            else:
                headers_obj.append(header)
                header = dict()
                header[i[-2].lower()] = i[-1]

        messages = re.split(
            regex_dict["headers2"]["find2"], message, flags=re.IGNORECASE
        )
        bodies = [i.strip() for i in messages[1:] if i.strip()]

        # NB! Chance of mismatched incorrectly assigned headers; information not used at this stage so not a problem
        # To fix if going to use subject

        secondary_messages = [
            {"headers": i, "body": j} for i, j in zip(headers_obj, bodies)
        ]
        message = [messages[0].strip()] + secondary_messages

        return message

    else:
        return message


def extract_head_headers(header_str):
    header_pattern = re.compile(regex_dict["head_headers"])
    results = header_pattern.findall(header_str)
    headers = dict()

    for i, j in results:
        headers[i] = j

    return headers


def extract_forwarded(message):

    forward_pattern = regex_dict["forwarded"]["ncapturing"]

    if re.search(forward_pattern, message):

        results = re.split(forward_pattern, message)
        fw_headers = re.findall(regex_dict["forwarded"]["capturing"], message)

        forwarded_messages = list()

        for i, j in zip(fw_headers, results[1:]):
            forwarded_message = dict()
            forwarded_message["headers"], forwarded_message["body"] = extract_headers(j)
            if not forwarded_message["headers"]:
                forwarded_message["headers"] = dict()
            forwarded_message["headers"]["fw_by"] = i[0]
            forwarded_message["headers"]["fw_date"] = i[1].replace("\n", "\s")
            forwarded_message["headers"]["fw_time"] = i[2].replace("\n", "\s")
            forwarded_messages.append(forwarded_message)

        message = results[0]

        return message, forwarded_messages

    else:
        return message, None


def separate_thread(email, email_header):

    email = re.split(r"-{2,6}\s{0,2}Original Message\s{0,3}-{2,6}", email)

    json_thread = dict()
    json_thread["messages"] = list()
    json_thread["head_message"] = dict()
    json_thread["head_message"]["headers"] = extract_head_headers(email_header)
    json_thread["head_message"]["body"], forwarded_messages = extract_forwarded(
        email.pop(0)
    )

    if forwarded_messages:
        json_thread["messages"] += forwarded_messages

    if email:
        for j in email:

            original_message = dict()

            message, forwarded_message = extract_forwarded(j)

            if forwarded_message:
                json_thread["messages"].append(forwarded_message)

            original_message["headers"], original_message["body"] = extract_headers(
                message
            )
            json_thread["messages"].append(original_message)

    new_messages = list()
    json_thread["messages"] = list(
        deepflatten(json_thread["messages"], ignore=(str, dict))
    )
    for i in json_thread["messages"]:
        i["body"] = split_on_headers(i["body"])
        if type(i["body"]) is list:
            new_messages += i["body"][1:]
            i["body"] = i["body"][0]

    """
    if len(new_messages) != 0:
        print(f"{len(new_messages)} extra messages found")
    """

    json_thread["messages"] += new_messages

    json_thread["head_message"]["body"] = split_on_headers(
        json_thread["head_message"]["body"]
    )

    if type(json_thread["head_message"]["body"]) is list:
        new_messages += json_thread["head_message"]["body"][1:]
        json_thread["head_message"]["body"] = json_thread["head_message"]["body"][0]
    json_thread["messages"] += new_messages

    return json_thread
