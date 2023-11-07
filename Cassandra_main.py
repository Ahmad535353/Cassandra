from API_KEYS import DEEPGRAM_API_KEY
import logging
import asyncio

from ConversationManager import ConversationManager

logging.basicConfig(level=logging.INFO)


async def main():
    conversation_manager = ConversationManager(llm_type="gpt")
    await conversation_manager.start_conv()


if __name__ == "__main__":
    # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
    # await main()
    asyncio.run(main())
