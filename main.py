#!/usr/bin/env python

import asyncio
import aioconsole
from BingChatAPI import BingChatAPI

API = BingChatAPI()
API.initialConnection()


async def callChat():
    await API.wsConnect()
    for i in range(0, 20):
        prompt = await aioconsole.ainput("\033[1m\033[0;31m" + 'User: ' + "\033[0;37m")
        for response in await API.update(prompt):
            print("\033[1m\033[0;32m" + "BingChat: " +
                  "\033[0;37m" + response["bot"])

    await API.close()

    return None

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(callChat())
    loop.close()
