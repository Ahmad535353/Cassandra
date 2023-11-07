from API_KEYS import DEEPGRAM_API_KEY
import pyaudio
import logging

from deepgram import Deepgram
import asyncio

from ConversationManager import ConversationManager

logging.basicConfig(level=logging.INFO)

async def main():

    conversation_manager = ConversationManager()
    await conversation_manager.start_conv()


if __name__ == "__main__":
    # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
    # await main()
    asyncio.run(main())
