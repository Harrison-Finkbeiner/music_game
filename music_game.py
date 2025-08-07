# Music listening party game. PLayers submit links to music videos and try to 
# guess which players submitted the videos
#
# Author: Harrison Finkbeiner
# Date: August 06 2025

import json
import imaplib, email
import browser


class MusicGame():
    def __init__(self):
        user_email = "EMAIL_ADDRESS"
        password = "PASSWORD"
        imap_url = "imap.gmail.com"

        self.con = imaplib.IMAP4_SSL(imap_url)

        self.con.login(user_email, password)
        