import time
import json
from pprint import pprint
import random

from slackclient import SlackClient


BOT_TOKEN = ""
GROUP_TOKEN = ""


def main():




    sc = SlackClient(BOT_TOKEN)

    if not sc.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    while True:


        for slack_event in sc.rtm_read():



            if not slack_event.get('type') == "message":
               continue

            message = slack_event.get("text")
            user = slack_event.get("user")
            channel = slack_event.get("channel")


            if not message or not user:
               continue


            if "hello" in message.lower():
                sc.rtm_send_message(channel, "hi")

            if "bye" in message.lower():
                sc.rtm_send_message(channel, "Goodbye")


            if "jokes" in message.lower():
                with open('jokes.json', encoding='utf-8') as data_file:
                    data = json.loads(data_file.read())

                values = [v for d in data['jokes'] for k, v in d.items() if k == 'id']
                try:
                    x = random.choice(values)
                    category = data['jokes'][x]['type']
                    sc.rtm_send_message(channel, "*Category:*   %s." % (category))
                    time.sleep(3)
                    sc.rtm_send_message(channel,data['jokes'][x]['setup'])
                    time.sleep(10)
                    sc.rtm_send_message(channel, data['jokes'][x]['punchline'])

                except IndexError:
                    print("nothing found")

            if "help" in message.lower:
                sc.rtm_send_message("try: jokes")


        time.sleep(0.5)


if __name__ == '__main__':
    main()