import json
import time
import asyncio
from websockets.client import connect
from dotenv.main import load_dotenv
import sys
import os
import requests
import logging


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()
cookie = os.environ['U_COOKIE']
logging.info(f"UserCookie: {cookie}")

DELIMITER = "\x1e"
CONVERSATION_URL = "https://www.bing.com/turing/conversation/create"
SYDNEY_URL = "wss://sydney.bing.com/sydney/ChatHub"


class BingChatAPI:
    def __init__(self):
        self.res = {
            "conversationId": "",
            "clientId": "",
            "conversationSignature": "",
            "invocationId": 0
        }
        self.connection = None

    def initialConnection(self) -> None:
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
            self.res = {
                "conversationId": ResposeBody["conversationId"],
                "clientId": ResposeBody["clientId"],
                "conversationSignature": ResposeBody["conversationSignature"],
                "invocationId": 0
            }
        logging.info(self.res)

    async def wsConnect(self) -> None:
        self.connection = await connect(SYDNEY_URL)

        try:
            await self.connection.send("""{"protocol":"json","version":1}""" + DELIMITER)
            message = await self.connection.recv()
            logging.info(f"Received: {message}")

            await self.connection.send("""{"type":6}""" + DELIMITER)

        except Exception as e:
            logging.error(e)

    async def update(self, input_text: str) -> str:
        if self.connection and self.res["clientId"] != "":
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
                        "isStartOfSession": self.res["invocationId"] == 0,
                        "message": {
                            "locale": "en-GB",
                            "market": "en-GB",
                            "author": "user",
                            "inputMethod": "Keyboard",
                            "text": input_text,
                            "messageType": "Chat"
                        },
                        "conversationSignature": self.res["conversationSignature"],
                        "participant": {
                            "id": self.res["clientId"],
                        },
                        "conversationId": self.res["conversationId"],
                    },
                ],
                "invocationId": str(self.res["invocationId"]),
                "target": "chat",
                "type": 4,
            }

            await self.connection.send(json.dumps(text_struct) + DELIMITER)

            finalresponse = False
            while not finalresponse:
                message = str(await self.connection.recv()).split(DELIMITER)[0]
                message = json.loads(message)

                if message["type"] == 2:
                    finalresponse = True
                    self.res["invocationId"] += 1
                    return message["item"]["messages"][1]["text"]
                elif message["type"] == 6:
                    logging.info("Done Answering")
                elif "messages" in message["arguments"][0].keys():
                    if "text" in message["arguments"][0]["messages"][0].keys():
                        logging.info(message["arguments"]
                                     [0]["messages"][0]["text"])

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
