#!/usr/bin/env python

import json
import time
import asyncio
from websockets.sync.client import connect
from dotenv.main import load_dotenv
import sys
import os
import requests
import logging


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()
cookie = os.environ['U_COOKIE']

DELIMITER = "\x1e"

logging.info(f"UserCookie: {cookie}")

CONVERSATION_URL = "https://www.bing.com/turing/conversation/create"
cookies = {"_U": cookie}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"
}

res = requests.get(
    CONVERSATION_URL,
    cookies=cookies,
    headers=headers
)

if res.status_code == 200:
    ResposeBody = res.json()
    res = {
        "conversationId": ResposeBody["conversationId"],
        "clientId": ResposeBody["clientId"],
        "conversationSignature": ResposeBody["conversationSignature"],
        "invocationId": 0
    }

logging.info(res)

input_ = "what is lorem ipsum"

SYDNEY_URL = "wss://sydney.bing.com/sydney/ChatHub"

connection = connect(SYDNEY_URL)

connection.send("""{"protocol":"json","version":1}""" + DELIMITER)
message = connection.recv()
logging.info(f"Received: {message}")

connection.send("""{"type":6}""" + DELIMITER)

text_struct = {
    "arguments": [
        {
            "source": "cib",
            "optionsSets": [
                "nlu_direct_response_filter",
                "deepleo",
                "disable_emoji_spoken_text",
                "responsible_ai_policy_235",
                "enablemm",
                "galileo",
                "visualcreative",
                "alllanguages",
                "jb095",
                "jbfv1",
                "nojbfedge",
                "weasgv2",
                "dv3sugg"
            ],
            "allowedMessageTypes": [
                "Chat",
                "InternalSearchQuery",
                "InternalSearchResult",
                "Disengaged",
                "InternalLoaderMessage",
                "RenderCardRequest",
                "AdsQuery",
                "SemanticSerp",
                "GenerateContentQuery",
                "SearchQuery"
            ],
            "sliceIds": [
                "rankwritec",
                "winmuid3tf",
                "forallv2",
                "allnopvt",
                "ttstmout",
                "sbsvgoptcf",
                "rrsuppfinal-c",
                "anssupdmar",
                "winlongmsg2tf",
                "sydnoinputt",
                "creatgoglc",
                "creatorv2t",
                "convcssclick",
                "0427visual_b",
                "418glpv6ps0",
                "420langdsat",
                "420bic",
                "0329resps0",
                "427rchlths0",
                "0417rediss0",
                "425bicp2",
                "424jbfv1",
                "426weasgv2"
            ],
            "verbosity": "verbose",
            "isStartOfSession": res["invocationId"] == 0,
            "message": {
                "locale": "en-GB",
                "market": "en-GB",
                "author": "user",
                "inputMethod": "Keyboard",
                "text": input_,
                "messageType": "Chat"
            },
            "conversationSignature": res["conversationSignature"],
            "participant": {
                "id": res["clientId"],
            },
            "conversationId": res["conversationId"],
        },
    ],
    "invocationId": str(res["invocationId"]),
    "target": "chat",
    "type": 4,
}

connection.send(json.dumps(text_struct) + DELIMITER)

finalresponse = False
while not finalresponse:
    message = str(connection.recv()).split(DELIMITER)[0]
    message = json.loads(message)
    if message["type"] == 2:
        finalresponse = True
        logging.info(message["item"]["messages"][1]["text"])
    elif "messages" in message["arguments"][0].keys():
        if "text" in message["arguments"][0]["messages"][0].keys():
            logging.info(message["arguments"][0]["messages"][0]["text"])


time.sleep(10)
connection.close()
