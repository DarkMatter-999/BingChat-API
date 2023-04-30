#!/usr/bin/env python

import asyncio

from BingChatAPI import BingChatAPI

API = BingChatAPI()
API.initialConnection()


async def callChat():
    await API.wsConnect()

    print(await API.update("What is 1 + 1 answer me without searching on the internet"))

    print(await API.update("ok then what is 1 + 10"))

    print(await API.update("what was my first question?"))

    await API.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(callChat())
    loop.run_forever()
    loop.close()
