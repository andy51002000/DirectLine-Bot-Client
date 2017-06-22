"""Receive message from bot."""
# importing the requests library
import json
import requests

# defining the api-endpoint
API_ENDPOINT = "https://directline.botframework.com/v3/directline/conversations"
# your API key here
API_KEY = ""
# your bot id
BOT_ID = ""

def stat_conversation():
    """Start a conversation with bot and get conversation id."""

    headers = {'Authorization': 'Bearer '+API_KEY}

# sending post request and saving response as response object
    responds = requests.post(url=API_ENDPOINT, headers=headers)
    print "The status code is:%s"%responds.status_code

# extracting response text
    response_text = responds.text
    print "The respons text is:%s"%response_text

# Parse JSON and get value
    conversation_id = responds.json()['conversationId']
    print "conversationId is:%s"%conversation_id
    return conversation_id

def send_message(conversation_id, message):
    """Send message to bot."""


# defining the api-endpoint
    send_api_endpoint = API_ENDPOINT +'/'+ conversation_id + "/activities"


    headers = {'Authorization': 'Bearer '+API_KEY, 'Content-Type': 'application/json'}
    data = {
        "type": "message",
        "from": {
            "id": "user1"
        },
        "text": message
    }

# sending post request and saving response as response object
    responds = requests.post(url=send_api_endpoint, data=json.dumps(data), headers=headers)
    print "The status code is:%s"%responds.status_code

# extracting response text
    response_text = responds.text
    print "The respons text is:%s"%response_text

def receive_message(conversation_id, watermark):
    """Receive message from bot."""


# defining the api-endpoint
    receive_api_endpoint = API_ENDPOINT +'/' + conversation_id + "/activities?watermark="+watermark

# your source code here

    headers = {'Authorization':'Bearer '+API_KEY}

# sending get request and saving response as response object
    responds = requests.get(url=receive_api_endpoint, headers=headers)
    print "The status code is:%s"%responds.status_code

    return responds.json()


if __name__ == "__main__":

    CONVERSASION_ID = stat_conversation()
    WATERMARK = ''
    while 1:
        USRR_INPUT = raw_input('please input message: ')
        if USRR_INPUT == 'exit':
            break
        send_message(CONVERSASION_ID, USRR_INPUT)
        JSON_MESSAGE = receive_message(CONVERSASION_ID, WATERMARK)
        WATERMARK = JSON_MESSAGE["watermark"]
        print 'watermark is', WATERMARK
        ACTIVITIES = JSON_MESSAGE["activities"]
        BOT_MESSAGES = list()
        for active in ACTIVITIES:
            if active["from"]["id"] == BOT_ID:
                BOT_MESSAGES.append(active)
        for bot_message in BOT_MESSAGES:
            print bot_message["text"]

