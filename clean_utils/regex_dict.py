import json


def generate_regex(string):
    string = string.replace("\n", " ")
    string = string.replace(" ", "\s*")
    string = string.replace(".", "\.")
    string = string.replace("(", "\(")
    string = string.replace(")", "\)")
    string = string.replace("/", "\/")
    return string


def get_attachment_regex_dict(format_file="clean_utils/file_formats.json"):

    with open(format_file, "r") as f:
        file_list = json.load(f)

    format_list = []

    for i in file_list.keys():
        format_list += file_list[i]

    attachment_regex_dict = [
        (
            r"\(See\sattached\sfile:\s(([%,\-\w\s!&.()_#]*?)\.({}))\)".format(i),
            r"<<(([%,\-\w\s!.&'()#_]*?)\.({}))>>".format(i),
            r" ?- (([%,\-\w\s!&'.()#_]*?)\.({}))".format(i),
        )
        for i in format_list
    ]
    return attachment_regex_dict


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
    "head_headers": r"([A-z-]*):((?:.*)(?:\n\t.*)*)",
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
    "headers2": {
        "capture": r"(?:(?P<from>(?<=\n)[\"\w\s\/,.]*?\s+?<[\w\s\-.@]*?>)\s+?on\s+?(?P<send_date>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?|(?:(?P<from_1>(?<=\n)[\"\w\s\/,.]*?\s+?)(?P<send_date_1>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time_1>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?)*?)(?:(?:[> ]{0,3}(?P<header>(?<!mail)(?:to)|from|cc|subject|sent|date|importance):(?P<header_value>(?:.*?\n)+?))(?=>* ?(?:to|from|cc|subject|sent|date|importance):|(?:\n+)|(?:>+\n)))",
        "capture2": r"(?:\n)(?:(?P<from>(?<=\n)[\\\'\[\]()\"\w\s\/,.]*?\s+?<[\w\s\-.@]*?>)\s+?on\s+?(?P<send_date>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?|(?:(?P<from_1>(?<=\n)[()@\"\w\s\/,.]*?\s+?)(?P<send_date_1>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time_1>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?)*?)(?:(?:[> ]{0,6}(?P<header>(?<!mail)(?:to)|from|cc|sent|subj|bcc|subject|sent|date|importance):(?P<header_value>(?:.*?\n)+?))+(?=[> ]*?(?:to|from|cc|sent|subj|bcc|subject|sent|date|importance):|(?:\n+)|(?:\s*?>+\n)))",
        "find": r"(?:(?:(?<=\n)[\"\w\s\/,.]*?\s+?<[\w\s\-.@]*?>)\s+?on\s+?(?:(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?:[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?|(?:(?:(?<=\n)[\"\w\s\/,.]*?\s+?)(?:(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?:[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?)*?)(?:(?:[> ]{0,3}(?:(?<!mail)(?:to)|from|cc|subject|sent|date|importance):(?:(?:.*?\n)+?))(?=>* ?(?:to|from|cc|subject|sent|date|importance):|(?:\n+)|(?:>+\n)))",
        "find2": r"(?:(?:(?<=\n)[\\\'\[\]()\"\w\s\/,.]*?\s+?<[\w\s\-.@]*?>)\s+?on\s+?(?:(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?:[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?|(?:(?:(?<=\n)[()@\"\w\s\/,.]*?\s+?)(?:(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?:[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?)*?)(?:(?:[> ]{0,6}(?:(?<!mail)(?:to)|from|cc|sent|subj|bcc|subject|sent|date|importance):(?:(?:.*?\n)+?))+(?=[> ]*?(?:to|from|cc|sent|subj|bcc|subject|sent|date|importance):|(?:\n+)|(?:\s*?>+\n)))",
        "no_lookbehind": r"(?:\n)(?:(?P<from>[()\"\w\s\/,.]*?\s+?<[\w\s\-.@]*?>)\s+?on\s+?(?P<send_date>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?|(?:(?P<from_1>[()@\"\w\s\/,.]*?\s+?)(?P<send_date_1>(?:[0-9]{1,2}\/){2}[0-9]{2,4})\s+?(?P<send_time_1>[0-9]{1,2}:[0-9]{1,2}[:0-9]{0,3}\s+?(?:AM|PM))\s+?)*?)(?:(?:[> ]{0,6}(?P<header>(?<!mail)(?:to)|from|cc|sent|subj|bcc|subject|sent|date|importance):(?P<header_value>(?:.*?\n)+?))+(?=[> ]*?(?:to|from|cc|sent|subj|bcc|subject|sent|date|importance):|(?:\n+)|(?:\s*?>+\n)))",
    },
    "forwarded": {
        "ncapturing": r"-{3,}[\s>]*Forwarded[\s\n>]*by[\s>]*(?:[A-z0-9\/\.$&@\s_\-]+)[\s\n>]on[\s>]*(?:(?:[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})[\s>]*(?:[0-9]{1,2}:[0-9]{1,2}[\s>]*(?:PM|AM)))[\s>]*-{3,}",
        "capturing": r"-{3,}[\s>]*Forwarded[\s\n>]*by[\s>]*([A-z0-9\/\.@&$\s_\-]+)[\s\n>]on[\s>]*((?:[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})[\s>]*([0-9]{1,2}:[0-9]{1,2}[\s>]*(?:PM|AM)))[\s>]*-{3,}",
    },
    "thread": r"-{3,}\s*Original Message\s*-{3,}",
    "url": r"((?:http|https|ftp|ftps):\/\/[A-z0-9\.\/\?=&_\-\+]+)",
}

garbage_dict = {
    "replacement_strings": {
        "confidentiality_footers": (
            """**********************************************************************************************
This E-mail and any of its attachments may contain Exelon Generation Company
proprietary information, which is privileged, confidential, or subject to copyright
belonging to the Exelon family of Companies.  This E-mail is intended solely for
the use of the individual or entity to which it is addressed.  If you are not the
intended recipient of this E-mail, you are hereby notified that any dissemination,
distribution, copying, or action taken in relation to the contents of and
attachments to this E-mail is strictly prohibited and may be unlawful.  If you have
received this E-mail in error, please notify the sender immediately and
permanently delete the original and any copy of this E-mail and any printout.

Thank You.
*********************************************************************************************""",
            """+-------------------------------------------------------------+
| This message may contain confidential and/or privileged     |
| information.  If you are not the addressee or authorized to |
| receive this for the addressee, you must not use, copy,     |
| disclose or take any action based on this message or any    |
| information herein.  If you have received this message in   |
| error, please advise the sender immediately by reply e-mail |
| and delete this message.  Thank you for your cooperation.   |
+-------------------------------------------------------------+""",
            """This e-mail is privileged and confidential and is intended only for the
recipient(s) named above.  If you are not the intended recipient, please
(i) do not read, copy, use or disclose the contents hereof to others
(any of the foregoing being strictly prohibited), (ii) notify the sender
immediately of your receipt hereof, and (iii) delete this e-mail and all
copies of it.""",
        ),
        "auto_footers": (
            """--------------------------
Sent from my BlackBerry Wireless Handheld (www.BlackBerry.net)""",
            """______________________________________________________
Get Your Private, Free Email at http://www.hotmail.com""",
            """At Homecoming 2000, the BETA TENT had the biggest crowd by far.  Stay connected and consider a future homecoming BETA reunion.  It's incredible...forget the 20 years in between...everyone just seems to pick it up right where they left off years ago."""
            """-------------------------
Yahoo! Greetings is a free service. If you'd like to send someone a
Yahoo! Greeting, you can do so at http://greetings.yahoo.com/""",
            """Find the one for you at Yahoo! Personals
http://rd.yahoo.com/mktg/greetings/txt/confirmation/tagline/?http://personals.yahoo.com""",
            """____________________________________________________________
Do You Yahoo!?
Get your free @yahoo.co.uk address at http://mail.yahoo.co.uk
or your free @yahoo.ie address at http://mail.yahoo.ie""",
            """__________________________________________________
Do You Yahoo!?
Check out Yahoo! Shopping and Yahoo! Auctions for all of
your unique holiday gifts! Buy at http://shopping.yahoo.com
or bid at http://auctions.yahoo.com""",
            """_____  

Do You Yahoo!?
Find the one for you at Yahoo! Personals <http://rd.yahoo.com/mktg/mail/txt/tagline/?http://personals.yahoo.com>.""",
        ),
    },
    "regex": {
        "auto_footers": (
            r"""(_{3,})?\s*Get\s*your\s*FREE\s*download\s*of\s*MSN\s*Explorer\s*at\s*((?:http|https|ftp|ftps):\/\/[A-z0-9\.\/\?=&_"\-\+]+)""",
            r"""(_{3,})?\s*Do\s*You\s*Yahoo\!\?\s*[\s\w!@.\-$,\/>&]*([((?:http|https|ftp|ftps):\/\/[A-z0-9\.\/\?=&_\-\+]+)""",
            r"""(?:\-{3,}\s*)?Yahoo\!\s*Groups\s*Sponsor\s*[-~]*>\s*[\s\w!@.\-$,\/>&]*([((?:http|https|ftp|ftps):\/\/[A-z0-9\.\/\?=&_\-\+]+)\s*[-~]*>""",
        ),
        "confidentiality_footers": (
            r"""-*\s*This\s*message\s*is\s*intended\s*only\s*for\s*the\s*personal\s*and\s*confidential\s*use\s*of\s*the\s*designated\s*recipient\(s\)\s*named\s*above\.\s*\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient\s*of\s*this\s*message\s*you\s*are\s*hereby\s*notified\s*that\s*any\s*review,\s*dissemination,\s*distribution\s*or\s*copying\s*of\s*this\s*message\s*is\s*strictly\s*prohibited\.\s*\s*This\s*communication\s*is\s*for\s*information\s*purposes\s*only\s*and\s*should\s*not\s*be\s*regarded\s*as\s*an\s*offer\s*to\s*sell\s*or\s*as\s*a\s*solicitation\s*of\s*an\s*offer\s*to\s*buy\s*any\s*financial\s*product,\s*an\s*official\s*confirmation\s*of\s*any\s*transaction,\s*or\s*as\s*an\s*official\s*statement\s*of\s*Lehman\s*Brothers\s*Inc\.\s*\s*Email\s*transmission\s*cannot\s*be\s*guaranteed\s*to\s*be\s*secure\s*or\s*error-free\.\s*\s*Therefore,\s*we\s*do\s*not\s*represent\s*that\s*this\s*information\s*is\s*complete\s*or\s*accurate\s*and\s*it\s*should\s*not\s*be\s*relied\s*upon\s*as\s*such\.\s*\s*All\s*information\s*is\s*subject\s*to\s*change\s*without\s*notice\.""",
            r"-*\s*This\s*e-mail\s*transmission\s*may\s*contain\s*confidential\s*or\s*legally\s*privileged\s*information\s*that\s*is\s*intended\s*only\s*for\s*the\s*individual\s*or\s*entity\s*named\s*in\s*the\s*e-mail\s*address\.\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient,\s*you\s*are\s*hereby\s*notified\s*that\s*any\s*disclosure,\s*copying,\s*distribution,\s*or\s*reliance\s*upon\s*the\s*contents\s*of\s*this\s*e-mail\s*is\s*strictly\s*prohibited\.\s*If\s*you\s*have\s*received\s*this\s*e-mail\s*transmission\s*in\s*error,\s*please\s*reply\s*to\s*the\s*sender,\s*so\s*that\s*ICON\s*Clinical\s*Research\s*can\s*arrange\s*for\s*proper\s*delivery,\s*and\s*then\s*please\s*delete\s*the\s*message\.\s*\s*Thank\s*You\.\s*\s*=*",
            r"""\**\s*CAUTION:\s*Electronic\s*mail\s*sent\s*through\s*the\s*Internet\s*is\s*not\s*secure\s*and\s*could\s*be\s*intercepted\s*by\s*a\s*third\s*party\.\s*\s*\s*This\s*email\s*and\s*any\s*files\s*transmitted\s*with\s*it\s*are\s*confidential\s*and\s*\s*intended\s*solely\s*for\s*the\s*use\s*of\s*the\s*individual\s*or\s*entity\s*to\s*whom\s*they\s*\s*\s*\s*are\s*addressed\.\s*If\s*you\s*have\s*received\s*this\s*email\s*in\s*error\s*please\s*notify\s*\s*the\s*system\s*manager\.\s*\s*This\s*footnote\s*also\s*confirms\s*that\s*this\s*email\s*message\s*has\s*been\s*swept\s*by\s*\s*MIMEsweeper\s*for\s*the\s*presence\s*of\s*computer\s*viruses\.\s*\s*\**""",
            r"""=*This\s*email\s*message\s*is\s*for\s*the\s*sole\s*use\s*of\s*the\s*intended\s*recipient\(s\)\s*and\s*may\s*contain\s*confidential\s*and\s*privileged\s*information\.\s*Any\s*unauthorized\s*review,\s*use,\s*disclosure\s*or\s*distribution\s*is\s*prohibited\.\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient,\s*please\s*contact\s*the\s*sender\s*by\s*reply\s*email\s*and\s*destroy\s*all\s*copies\s*of\s*the\s*original\s*message\.""",
            r"""-*\s*The\s*information\s*transmitted\s*is\s*intended\s*only\s*for\s*the\s*person\s*or\s*entity\s*to\s*which\s*it\s*is\s*addressed\s*and\s*may\s*contain\s*confidential\s*and\/or\s*privileged\s*material\.\s*Any\s*review,\s*retransmission,\s*dissemination\s*or\s*other\s*use\s*of,\s*or\s*taking\s*of\s*any\s*action\s*in\s*reliance\s*upon,\s*this\s*information\s*by\s*persons\s*or\s*entities\s*other\s*than\s*the\s*intended\s*recipient\s*is\s*prohibited\.\s*\s*\s*If\s*you\s*received\s*this\s*in\s*error,\s*please\s*contact\s*the\s*sender\s*and\s*delete\s*the\s*material\s*from\s*any\s*computer\.""",
            r"""\**\s*Notice\s*Regarding\s*Entry\s*of\s*Orders\s*and\s*Instructions:\s*Please\s*do\s*not\s*transmit\s*orders\s*and\/or\s*instructions\s*regarding\s*your\s*UBSPaineWebber\s*account\(s\)\s*by\s*e-mail\.\s*Orders\s*and\/or\s*instructions\s*transmitted\s*by\s*e-mail\s*will\s*not\s*be\s*accepted\s*by\s*UBSPaineWebber\s*and\s*UBSPaineWebber\s*will\s*not\s*be\s*responsible\s*for\s*carrying\s*out\s*such\s*orders\s*and\/or\s*instructions\.\s*\s*Notice\s*Regarding\s*Privacy\s*and\s*Confidentiality:\s*UBSPaineWebber\s*reserves\s*the\s*right\s*to\s*monitor\s*and\s*review\s*the\s*content\s*of\s*all\s*e-mail\s*communications\s*sent\s*and\/or\s*received\s*by\s*its\s*employees\.""",
            r"""-*\s*This\s*message\s*is\s*intended\s*only\s*for\s*the\s*personal\s*and\s*confidential\s*use\s*of\s*the\s*designated\s*recipient\(s\)\s*named\s*above\.\s*\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient\s*of\s*this\s*message\s*you\s*are\s*hereby\s*notified\s*that\s*any\s*review,\s*dissemination,\s*distribution\s*or\s*copying\s*of\s*this\s*message\s*is\s*strictly\s*prohibited\.\s*\s*This\s*communication\s*is\s*for\s*information\s*purposes\s*only\s*and\s*should\s*not\s*be\s*regarded\s*as\s*an\s*offer\s*to\s*sell\s*or\s*as\s*a\s*solicitation\s*of\s*an\s*offer\s*to\s*buy\s*any\s*financial\s*product,\s*an\s*official\s*confirmation\s*of\s*any\s*transaction,\s*or\s*as\s*an\s*official\s*statement\s*of\s*Lehman\s*Brothers\s*Inc\.\s*\s*Email\s*transmission\s*cannot\s*be\s*guaranteed\s*to\s*be\s*secure\s*or\s*error-free\.\s*\s*Therefore,\s*we\s*do\s*not\s*represent\s*that\s*this\s*information\s*is\s*complete\s*or\s*accurate\s*and\s*it\s*should\s*not\s*be\s*relied\s*upon\s*as\s*such\.\s*\s*All\s*information\s*is\s*subject\s*to\s*change\s*without\s*notice\.\s*=*""",
            r"""-*\s*This\s*message\s*is\s*intended\s*only\s*for\s*the\s*personal\s*and\s*confidential\s*use\s*of\s*the\s*designated\s*recipient\(s\)\s*named\s*above\.\s*\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient\s*of\s*this\s*message\s*you\s*are\s*hereby\s*notified\s*that\s*any\s*review,\s*dissemination,\s*distribution\s*or\s*copying\s*of\s*this\s*message\s*is\s*strictly\s*prohibited\.\s*\s*This\s*communication\s*is\s*for\s*information\s*purposes\s*only\s*and\s*should\s*not\s*be\s*regarded\s*as\s*an\s*offer\s*to\s*sell\s*or\s*as\s*a\s*solicitation\s*of\s*an\s*offer\s*to\s*buy\s*any\s*financial\s*product,\s*an\s*official\s*confirmation\s*of\s*any\s*transaction,\s*or\s*as\s*an\s*official\s*statement\s*of\s*Lehman\s*Brothers\s*Inc\.\s*\s*Email\s*transmission\s*cannot\s*be\s*guaranteed\s*to\s*be\s*secure\s*or\s*error-free\.\s*\s*Therefore,\s*we\s*do\s*not\s*represent\s*that\s*this\s*information\s*is\s*complete\s*or\s*accurate\s*and\s*it\s*should\s*not\s*be\s*relied\s*upon\s*as\s*such\.\s*\s*All\s*information\s*is\s*subject\s*to\s*change\s*without\s*notice\.""",
            r"""\++CONFIDENTIALITY\s*NOTICE\++\s*The\s*information\s*in\s*this\s*email\s*may\s*be\s*confidential\s*and\/or\s*privileged\.\s*\s*This\s*email\s*is\s*intended\s*to\s*be\s*reviewed\s*by\s*only\s*the\s*individual\s*or\s*organization\s*named\s*above\.\s*\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient\s*or\s*an\s*authorized\s*representative\s*of\s*the\s*intended\s*recipient,\s*you\s*are\s*hereby\s*notified\s*that\s*any\s*review,\s*dissemination\s*or\s*copying\s*of\s*this\s*email\s*and\s*its\s*attachments,\s*if\s*any,\s*or\s*the\s*information\s*contained\s*herein\s*is\s*prohibited\.\s*\s*If\s*you\s*have\s*received\s*this\s*email\s*in\s*error,\s*please\s*immediately\s*notify\s*the\s*sender\s*by\s*return\s*email\s*and\s*delete\s*this\s*email\s*from\s*your\s*system\.\s*\s*Thank\s*You""",
            r"""THE\s*INFORMATION\s*CONTAINED\s*IN\s*THIS\s*E-MAIL\s*IS\s*LEGALLY\s*PRIVILEGED\s*AND\s*CONFIDENTIAL\s*INFORMATION\s*INTENDED\s*ONLY\s*FOR\s*THE\s*USE\s*OF\s*THE\s*INDIVIDUAL\s*OR\s*ENTITY\s*NAMED\s*ABOVE\.\s*\s*YOU\s*ARE\s*HEREBY\s*NOTIFIED\s*THAT\s*ANY\s*DISSEMINATION,\s*DISTRIBUTION,\s*OR\s*COPY\s*OF\s*THIS\s*E-MAIL\s*TO\s*UNAUTHORIZED\s*ENTITIES\s*IS\s*STRICTLY\s*PROHIBITED\.\s*IF\s*YOU\s*HAVE\s*RECEIVED\s*THIS\s*E-MAIL\s*IN\s*ERROR,\s*PLEASE\s*DELETE\s*IT\.""",
            r"""__+\s*\s*Ce\s*message\s*et\s*toutes\s*les\s*pieces\s*jointes\s*\(ci-apres\s*le\s*"message"\)\s*sont\s*etablis\s*a\s*l'intention\s*exclusive\s*de\s*ses\s*destinataires\s*et\s*sont\s*confidentiels\.\s*Si\s*vous\s*recevez\s*ce\s*message\s*par\s*erreur,\s*merci\s*de\s*le\s*detruire\s*et\s*d'en\s*avertir\s*immediatement\s*l'expediteur\.\s*Toute\s*utilisation\s*de\s*ce\s*message\s*non\s*conforme\s*a\s*sa\s*destination,\s*toute\s*diffusion\s*ou\s*toute\s*publication,\s*totale\s*ou\s*partielle,\s*est\s*interdite,\s*sauf\s*autorisation\s*expresse\.\s*\s*L'internet\s*ne\s*permettant\s*pas\s*d'assurer\s*l'integrite\s*de\s*ce\s*message,\s*BNP\s*PARIBAS\s*\(et\s*ses\s*filiales\)\s*decline\(nt\)\s*toute\s*responsabilite\s*au\s*titre\s*de\s*ce\s*message,\s*dans\s*l'hypothese\s*ou\s*il\s*aurait\s*ete\s*modifie\.\s*--+\s*This\s*message\s*and\s*any\s*attachments\s*\(the\s*"message"\)\s*are\s*intended\s*solely\s*for\s*the\s*addressees\s*and\s*are\s*confidential\.\s*If\s*you\s*receive\s*this\s*message\s*in\s*error,\s*please\s*delete\s*it\s*and\s*immediately\s*notify\s*the\s*sender\.""",
            r"""\**\s*This\s*e-mail\s*is\s*the\s*property\s*of\s*Enron\s*Corp\.\s*and\/or\s*its\s*relevant\s*affiliate\s*\s*and\s*may\s*contain\s*confidential\s*and\s*privileged\s*material\s*for\s*the\s*sole\s*use\s*of\s*the\s*\s*intended\s*\s*recipient\s*\(s\)\.\s*Any\s*review,\s*use,\s*distribution\s*or\s*disclosure\s*by\s*others\s*is\s*\s*strictly\s*prohibited\.\s*If\s*you\s*are\s*not\s*the\s*intended\s*recipient\s*\(or\s*authorized\s*to\s*\s*receive\s*for\s*\s*the\s*recipient\),\s*please\s*contact\s*the\s*sender\s*or\s*reply\s*to\s*Enron\s*Corp\.\s*at\s*\s*enron\.messaging\.administration@enron\.com\s*and\s*delete\s*all\s*copies\s*of\s*the\s*\s*message\.\s*\s*This\s*e-mail\s*\(and\s*any\s*attachments\s*hereto\)\s*are\s*not\s*intended\s*to\s*be\s*an\s*offer\s*\s*\(or\s*an\s*\s*acceptance\)\s*and\s*do\s*not\s*create\s*or\s*evidence\s*a\s*binding\s*and\s*enforceable\s*\s*contract\s*\s*between\s*Enron\s*Corp\.\s*\(or\s*any\s*of\s*its\s*affiliates\)\s*and\s*the\s*intended\s*\s*recipient\s*or\s*any\s*other\s*party,\s*and\s*may\s*not\s*be\s*relied\s*on\s*by\s*anyone\s*as\s*the\s*basis\s*of\s*a\s*\s*contract\s*by\s*\s*estoppel\s*or\s*otherwise\.\s*Thank\s*you\.\s*\**""",
            r"""\**\s*This\s*email\s*and\s*any\s*files\s*transmitted\s*with\s*it\s*from\s*the\s*ElPaso\s*\s*Corporation\s*are\s*confidential\s*and\s*intended\s*solely\s*for\s*the\s*\s*use\s*of\s*the\s*individual\s*or\s*entity\s*to\s*whom\s*they\s*are\s*addressed\.\s*\s*If\s*you\s*have\s*received\s*this\s*email\s*in\s*error\s*please\s*notify\s*the\s*\s*sender\.\s*\**""",
            r"""\**\s*Bear\s*Stearns\s*is\s*not\s*responsible\s*for\s*any\s*recommendation,\s*solicitation,\s*offer\s*or\s*agreement\s*or\s*any\s*information\s*about\s*any\s*transaction,\s*customer\*account\s*or\s*account\s*activity\s*contained\s*in\s*this\s*communication\.\**""",
            r"""\**Internet\s*Email\s*Confidentiality\s*Footer\**\s*\s*\s*Privileged\/Confidential\s*Information\s*may\s*be\s*contained\s*in\s*this\s*message\.\s*\s*If\s*you\s*are\s*not\s*the\s*addressee\s*indicated\s*in\s*this\s*message\s*\(or\s*responsible\s*for\s*delivery\s*\s*of\s*the\s*message\s*to\s*such\s*person\),\s*you\s*may\s*not\s*copy\s*or\s*deliver\s*this\s*message\s*to\s*\s*anyone\.\s*In\s*such\s*case,\s*you\s*should\s*destroy\s*this\s*message\s*and\s*kindly\s*notify\s*the\s*sender\s*by\s*reply\s*email\.\s*Please\s*advise\s*immediately\s*if\s*you\s*or\s*your\s*employer\s*do\s*not\s*consent\s*\s*to\s*Internet\s*email\s*for\s*messages\s*of\s*this\s*kind\.\s*\s*Opinions,\s*conclusions\s*and\s*other\s*information\s*in\s*this\s*message\s*that\s*do\s*not\s*relate\s*to\s*the\s*official\s*business\s*of\s*my\s*firm\s*shall\s*be\s*understood\s*as\s*neither\s*given\s*nor\s*endorsed\s*by\s*it\.""",
        ),
    },
}

# TO DO: attempt to generalise regexes
# TO DO: add regexes for signatures
