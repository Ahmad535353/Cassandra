from deepgram import Deepgram
from API_KEYS import DEEPGRAM_API_KEY, CHATGPT_API_KEY
import pyaudio
import logging
import asyncio
import openai

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
        self.CHUNK = 80000
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
                # logging.info(f"Transcript received: {t}")
                if 'channel' in t:
                    transcripts.append(t['channel']['alternatives'][0]['transcript'])
                    # logging.info(f"handled this transcription: {t['channel']['alternatives'][0]['transcript']}")


            deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, handle_transcript)

            silent_time = 0  # Time duration for which silence has been detected
            while True:
                data = stream.read(self.CHUNK)
                if not data:
                    logging.warning("No data read from the microphone.")
                else:
                    # Check for silence
                    if self.is_silent(data):
                        silent_time += (self.CHUNK / self.RATE)
                        if silent_time > 5:  # 5 seconds of silence
                            logging.info("Silence detected. Stopping listening.")
                            break
                    else:
                        silent_time = 0  # Reset the silence timer

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
        print (transcripts[:-1])
        return transcripts[:-1]
    
    def is_silent(self, data):
        SILENCE_THRESHOLD = 500
        """Returns 'True' if below the 'silent' threshold"""
        return max(data) < SILENCE_THRESHOLD

class LLM:
    def __init__(self):
        # Initialize LLM SDK or API connection here if needed
        openai.api_key = CHATGPT_API_KEY

    def process(self, text):
        # Process the text with LLM and return the response
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a conversational assistant. You should asnwer every question like a real human, like a conversation. Keep the answers short."},
            {"role": "user", "content": text}
        ]
        )
        answer = completion.choices[0].message
        print (answer)
        # response = "AI Response:" + answer  # Mock response
        return answer

class Synthesizer:
    def __init__(self):
        # Initialize voice synthesizer SDK or API connection here if needed
        pass

    def speak(self, text):
        # Convert text to speech and play it
        print(f"[AI Voice]: {text}")