from API_KEYS import DEEPGRAM_API_KEY
import pyaudio
import logging

from deepgram import Deepgram
import asyncio

# Your Deepgram API Key
# DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'

# URL for the realtime streaming audio you would like to transcribe
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'


logging.basicConfig(level=logging.INFO)

async def main():
    logging.info("Initializing the Deepgram SDK...")
    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # Parameters for pyaudio stream
    CHUNK = 8000
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK
    )
    print("Listening... Press Ctrl+C to stop.")

    # Create a websocket connection to Deepgram
    # In this example, punctuation is turned on, interim results are turned off, and language is set to UK English.
    try:
        logging.info("Attempting to open a socket connection to Deepgram...")
        deepgramLive = await deepgram.transcription.live(
            {
                "smart_format": True,
                "interim_results": False,
                "language": "en-US",
                "model": "nova",
                "encoding": "linear16",  # Specify the encoding
                "sample_rate": RATE  # Specify the sample rate
            }
        )
        logging.info("Socket connection to Deepgram opened successfully!")
    except Exception as e:
        print(f"Could not open socket: {e}")
        return

    # Listen for the connection to close
    deepgramLive.registerHandler(
        deepgramLive.event.CLOSE, lambda c: print(f"Connection closed with code {c}.")
    )

    # Listen for any transcripts received from Deepgram and write them to the console
    deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, lambda t: logging.info(f"Transcript received: {t}"))

    try:
        while True:
            data = stream.read(CHUNK)
            if not data:
                logging.warning("No data read from the microphone.")
            else:
                logging.debug("Captured audio data from microphone.")
                deepgramLive.send(data)
            logging.debug("Sent audio data to Deepgram.")
            await asyncio.sleep(0.1)  # Give some buffer time
    except KeyboardInterrupt:
        # Indicate that we've finished sending data
        await deepgramLive.finish()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("\nStopping...")

    # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
    await deepgramLive.finish()


if __name__ == "__main__":
    # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
    # await main()
    asyncio.run(main())
