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

        try:
            with open('players.json', 'r') as file:
                data = json.load(file)
            

        except FileNotFoundError:
            print("Error: 'players.json' not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in 'players.json'.")

        self.game_code = data.get("game_code", None)



    def getMessages(self):
        self.con.select('INBOX')
        status, data = self.con.search(None, "SUBJECT", str(self.game_code))

        if status == 'OK':
            message_ids = data[0].split()

            if message_ids:
                for msg_id in message_ids:
                    status, msg_data = self.con.fetch(msg_id, '(RFC822)')
                    if (status == 'OK'):
                        raw_email = msg_data[0][1]
                        msg = email.message_from_bytes(raw_email)

                        print(msg)
            else:
                print(f"No messages found with subject {self.game_code}")
        else:
            print(f"Failed to search with status {status}"


def main():

    mg = MusicGame()
    mg.getMessages()

if __name__ == "__main__":
    main()