import os
from slack import RTMClient
from slack import WebClient
from dotenv import load_dotenv

load_dotenv()
flag = False
members = {}

def send_websocket():
    global flag
    if not flag:
        flag = True
        global members
        web_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        users = web_client.users_list()
        for user in users['members']:
            members[user['id']] = user['profile']['display_name']
        ids = [u['id'] for u in users['members']]
        rtm_client.send_over_websocket(payload={
            "type": "presence_sub",
            "ids": ids
        })

@RTMClient.run_on(event="message")
def enable_presence_subscription(**payload):
    send_websocket()
    global members
    username = members[payload['data']['user']] if members[payload['data']['user']] != "" else payload['data']['user']
    print(f"{username} sent message: {payload['data']['text']}")
    web_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    response = web_client.chat_postEphemeral(
        channel=payload['data']['channel'],
        text="Hello",
        user=payload['data']['user']
    )

try:
    rtm_client = RTMClient(token=os.getenv("SLACK_BOT_TOKEN"))
    print("Bot is up and running!")
    rtm_client.start()

except Exception as err:
    print(err)
