# Music listening party game. PLayers submit links to music videos and try to 
# guess which players submitted the videos
#
# Author: Harrison Finkbeiner
# Date: August 06 2025

import json
import imaplib, email
import webbrowser
import random

class MusicGame():
    def __init__(self):
        user_email = "EMAIL_ADDRESS"
        password = "PASSWORD"
        imap_url = "imap.gmail.com"
        IMAP_PORT = 993

        self.playerDict = {}
        self.playerVideoDict = {}

        self.con = imaplib.IMAP4_SSL(imap_url,IMAP_PORT)

        self.con.login(user_email, password)

        try:
            with open('players.json', 'r') as file:
                data = json.load(file)
            

        except FileNotFoundError:
            print("Error: 'players.json' not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in 'players.json'.")

        self.game_code = data.get("game_code", None)

        for players in data["players"]:
            self.playerDict[players['Email']] = players['Name']

        for emails in self.playerDict.keys():
            self.playerVideoDict[emails] = []

        self.submittedVideos = []
        self.videosIndex = []


    # Get messages for the given game code and create a list
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

                        sender = msg['from']
                        senderEmail = sender.split("<")[1].strip(">")
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain':
                                try:
                                    charset = part.get_content_charset()
                                    if charset:
                                        plain_text_body = part.get_payload(decode=True).decode(charset)
                                    else:
                                        plain_text_body = part.get_payload(decode=True).decode('utf-8') # Default to utf-8
                                    self.submittedVideos.append(plain_text_body)
                                    lastIndex = len(self.submittedVideos) - 1

                                    if senderEmail in self.playerVideoDict:
                                        self.playerVideoDict[senderEmail].append(lastIndex)

                                    break # Found and printed plain text, exit loop
                                except Exception as e:
                                    print(f"Error decoding plain text part: {e}")
                                    # Fallback or error handling
            else:
                print(f"No messages found with subject {self.game_code}")
        else:
            print(f"Failed to search with status {status}")

    # Shows players and submitted video. Players through all videos and displays 
    # who submitted the videos
    def gameLoop(self):
        # print players: submitted video count: 
        for email, submittedVideoList in self.playerVideoDict.items():
            player = self.playerDict[email]
            print(f"Player: {player} submitted {len(submittedVideoList)}")
        self.randomizeVideos()

        input("Press a button to start the game.")
        for i in self.videosIndex:
            input("Press enter to play the next video")
            webbrowser.open(self.submittedVideos[i])
            input("Press to reveal player")
            for email, submittedVideoList in self.playerVideoDict.items():
                if i in submittedVideoList:
                    player = self.playerDict[email]

            print(f"Video submitted by: {player}")
    
    # Randomize video order to play the videos
    def randomizeVideos(self):
        self.videosIndex = list(range(0, len(self.submittedVideos)))
        random.shuffle(self.videosIndex)


def main():
    mg = MusicGame()
    mg.getMessages()
    mg.gameLoop()

if __name__ == "__main__":
    main()