import json


def get_attachment_regex_dict(format_file):

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
    "confidentiality_footers": (
        """*******************Internet Email Confidentiality Footer*******************


Privileged/Confidential Information may be contained in this message.  If you
are not the addressee indicated in this message (or responsible for delivery 
of
the message to such person), you may not copy or deliver this message to 
anyone.
In such case, you should destroy this message and kindly notify the sender by
reply email. Please advise immediately if you or your employer do not consent 
to
Internet email for messages of this kind.  Opinions, conclusions and other
information in this message that do not relate to the official business of my
firm shall be understood as neither given nor endorsed by it.
""",
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
        """**********************************************************************
This e-mail is the property of Enron Corp. and/or its relevant affiliate and may contain confidential and privileged material for the sole use of the intended recipient (s). Any review, use, distribution or disclosure by others is strictly prohibited. If you are not the intended recipient (or authorized to receive for the recipient), please contact the sender or reply to Enron Corp. at enron.messaging.administration@enron.com and delete all copies of the message. This e-mail (and any attachments hereto) are not intended to be an offer (or an acceptance) and do not create or evidence a binding and enforceable contract between Enron Corp. (or any of its affiliates) and the intended recipient or any other party, and may not be relied on by anyone as the basis of a contract by estoppel or otherwise. Thank you.
**********************************************************************""",
        """******************************************************************
This email and any files transmitted with it from the ElPaso 
Corporation are confidential and intended solely for the 
use of the individual or entity to whom they are addressed. 
If you have received this email in error please notify the 
sender.
******************************************************************""",
        """******************************************************
Notice Regarding Entry of Orders and Instructions:
Please do not transmit orders and/or instructions
regarding your UBSPaineWebber account(s) by e-mail.
Orders and/or instructions transmitted by e-mail will
not be accepted by UBSPaineWebber and UBSPaineWebber
will not be responsible for carrying out such orders
and/or instructions.

Notice Regarding Privacy and Confidentiality:
UBSPaineWebber reserves the right to monitor and
review the content of all e-mail communications sent
and/or received by its employees.""",
        """------------------------------------------------------------------------------
This e-mail transmission may contain confidential or legally privileged information that is intended only for the individual or entity named in the e-mail address. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or reliance upon the contents of this e-mail is strictly prohibited. If you have received this e-mail transmission in error, please reply to the sender, so that ICON Clinical Research can arrange for proper delivery, and then please delete the message.  Thank You.

=============================================================================""",
        """+-------------------------------------------------------------+
| This message may contain confidential and/or privileged     |
| information.  If you are not the addressee or authorized to |
| receive this for the addressee, you must not use, copy,     |
| disclose or take any action based on this message or any    |
| information herein.  If you have received this message in   |
| error, please advise the sender immediately by reply e-mail |
| and delete this message.  Thank you for your cooperation.   |
+-------------------------------------------------------------+""",
        """This message may contain confidential information that is protected by the 
attorney-client and/or work product privileges.""",
        """------------------------------------------------------------------------------
This message is intended only for the personal and confidential use of the designated recipient(s) named above.  If you are not the intended recipient of this message you are hereby notified that any review, dissemination, distribution or copying of this message is strictly prohibited.  This communication is for information purposes only and should not be regarded as an offer to sell or as a solicitation of an offer to buy any financial product, an official confirmation of any transaction, or as an official statement of Lehman Brothers Inc.  Email transmission cannot be guaranteed to be secure or error-free.  Therefore, we do not represent that this information is complete or accurate and it should not be relied upon as such.  All information is subject to change without notice.""",
        """***********************************************************************
Bear Stearns is not responsible for any recommendation, solicitation,
offer or agreement or any information about any transaction, customer
account or account activity contained in this communication.
***********************************************************************""",
        """THE INFORMATION CONTAINED IN THIS E-MAIL IS LEGALLY PRIVILEGED AND CONFIDENTIAL INFORMATION INTENDED ONLY FOR THE USE OF THE INDIVIDUAL OR
ENTITY NAMED ABOVE.  YOU ARE HEREBY NOTIFIED THAT ANY DISSEMINATION, DISTRIBUTION, OR COPY OF THIS E-MAIL TO UNAUTHORIZED ENTITIES IS STRICTLY
PROHIBITED. IF YOU HAVE RECEIVED THIS
E-MAIL IN ERROR, PLEASE DELETE IT.""",
        """**********************************************************************
CAUTION: Electronic mail sent through the Internet is not secure and could
be intercepted by a third party. 

This email and any files transmitted with it are confidential and 
intended solely for the use of the individual or entity to whom they   
are addressed. If you have received this email in error please notify 
the system manager.

This footnote also confirms that this email message has been swept by 
MIMEsweeper for the presence of computer viruses.

**********************************************************************""",
    ),
    "auto_footers": (
        """_________________________________________________________________
    Get your FREE download of MSN Explorer at http://explorer.msn.com/intl.asp/""",
        """--------------------------
Sent from my BlackBerry Wireless Handheld (www.BlackBerry.net)""",
        """______________________________________________________
Get Your Private, Free Email at http://www.hotmail.com""",
        """__________________________________________________
Do You Yahoo!?
Send your FREE holiday greetings online!
http://greetings.yahoo.com""",
        """____________________________________________________________
Do You Yahoo!?
Get your free @yahoo.co.uk address at http://mail.yahoo.co.uk
or your free @yahoo.ie address at http://mail.yahoo.ie""",
        """__________________________________________________
Do You Yahoo!?
Great stuff seeking new owners in Yahoo! Auctions!
http://auctions.yahoo.com""",
        """__________________________________________________
Do You Yahoo!?
Yahoo! GeoCities - quick and easy web site hosting, just $8.95/month.
http://geocities.yahoo.com/ps/info1""",
        """__________________________________________________
Do You Yahoo!?
Send your FREE holiday greetings online!
http://greetings.yahoo.com""",
        """__________________________________________________
Do You Yahoo!?
Get personalized email addresses from Yahoo! Mail
http://personal.mail.yahoo.com/""",
        """__________________________________________________
Do You Yahoo!?
Make a great connection at Yahoo! Personals.
http://personals.yahoo.com""",
        """__________________________________________________
Do You Yahoo!?
Make a great connection at Yahoo! Personals.
http://personals.yahoo.com""",
        """  _____  

Do You Yahoo!?
Find the one for you at Yahoo! Personals <http://rd.yahoo.com/mktg/mail/txt/tagline/?http://personals.yahoo.com>.""",
        """__________________________________________________
Do You Yahoo!?
Find a job, post your resume.
http://careers.yahoo.com""",
        """Do You Yahoo!?
Send your FREE holiday greetings online at Yahoo! Greetings .
""",
        """Do You Yahoo!?
Make international calls for as low as $.04/minute with Yahoo! Messenger http://phonecard.yahoo.com/""",
        """__________________________________________________
Do You Yahoo!?
Buy the perfect holiday gifts at Yahoo! Shopping.
http://shopping.yahoo.com""",
        """__________________________________________________
Do You Yahoo!?
Get email at your own domain with Yahoo! Mail. 
http://personal.mail.yahoo.com/""",
        """---------------------------------
Do You Yahoo!?
Get email alerts & NEW webcam video instant messaging with Yahoo! Messenger.""",
        """_________________________________________________________
Do You Yahoo!?
Get your free @yahoo.com address at http://mail.yahoo.com""",
    ),
}


# TO DO: attempt to generalise regexes
