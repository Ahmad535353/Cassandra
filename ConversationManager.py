from deepgram import Deepgram
from API_KEYS import DEEPGRAM_API_KEY
import pyaudio
import logging
import asyncio


class ConversationManager():
    def __init__(self) -> None:
        self.transcriber = Transcriber()
        self.llm = LLM()
        self.synthesizer = Synthesizer()
    async def start_conv(self):
        try:
            print("Listening... Press Ctrl+C to stop.")
            transcripts = await self.transcriber.transcribe()
            for transcript in transcripts:
                response = self.llm.process(transcript)
                self.synthesizer.speak(response)
        except Exception as e:
            print(f"An error occurred: {e}")


class Transcriber:
    def __init__(self):
        self.api_key = DEEPGRAM_API_KEY
        self.deepgram = Deepgram(self.api_key)
        self.CHUNK = 20000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
    
    async def transcribe(self):
        transcripts = []
        
        stream = self.audio.open(
            format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
            input=True, output=True, frames_per_buffer=self.CHUNK
        )

        try:
            deepgramLive = await self.deepgram.transcription.live(
                {
                    "smart_format": True,
                    "interim_results": False,
                    "language": "en-US",
                    "model": "nova",
                    "encoding": "linear16",
                    "sample_rate": self.RATE
                }
            )

            deepgramLive.registerHandler(
                deepgramLive.event.CLOSE, lambda c: print(f"Connection closed with code {c}.")
            )

            def handle_transcript(t):
                logging.info(f"Transcript received: {t}")
                transcripts.append(t)

            deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, handle_transcript)

            while True:
                data = stream.read(self.CHUNK)
                if not data:
                    logging.warning("No data read from the microphone.")
                else:
                    logging.debug("Captured audio data from microphone.")
                    deepgramLive.send(data)
                logging.debug("Sent audio data to Deepgram.")
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            await deepgramLive.finish()
            stream.stop_stream()
            stream.close()
            self.audio.terminate()

        await deepgramLive.finish()
        print (transcripts)
        return transcripts

class LLM:
    def __init__(self):
        # Initialize LLM SDK or API connection here if needed
        pass

    def process(self, text):
        # Process the text with LLM and return the response
        response = "AI Response for " + text  # Mock response
        return response

class Synthesizer:
    def __init__(self):
        # Initialize voice synthesizer SDK or API connection here if needed
        pass

    def speak(self, text):
        # Convert text to speech and play it
        print(f"[AI Voice]: {text}")