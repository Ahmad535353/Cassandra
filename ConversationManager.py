from deepgram import Deepgram
from API_KEYS import DEEPGRAM_API_KEY, CHATGPT_API_KEY
import pyaudio
import logging
import asyncio
import openai
import boto3
import sounddevice as sd
import numpy as np
import wave

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
        print (answer['content'])
        # response = "AI Response:" + answer  # Mock response
        return answer['content']

class Synthesizer:
    def __init__(self):
        # Initialize voice synthesizer SDK or API connection here if needed
        boto3.setup_default_session(profile_name='Ahmad_personal_projects')
        # Initialize the Amazon Polly client
        self.polly_client = boto3.client('polly', region_name='us-east-2')

    def speak(self, text, save_to_file=False):
        # Convert text to speech and play it
        response = self.polly_client.synthesize_speech(
            Text=text,
            OutputFormat='pcm',
            VoiceId='Joanna'
        )

        # Read the audio stream from the response
        audio_stream = response['AudioStream'].read()


        if save_to_file:
            # Save the audio to a file
            num_channels = 1  # Mono
            sample_width = 2  # Polly's PCM output is 16-bit
            frame_rate = 16000  # Sample rate of 16000 Hz
            num_frames = len(audio_stream) // (sample_width * num_channels)
            # Write the PCM data to a WAV file
            with wave.open('output.wav', 'wb') as wav_file:
                wav_file.setnchannels(num_channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(frame_rate)
                wav_file.setnframes(num_frames)
                wav_file.writeframes(audio_stream)
                print("Speech synthesis complete. Audio saved as 'hello_world.mp3'.")

        # Assuming the sample width is 2 bytes and sample rate is 16000 Hz
        sample_rate = 16000
        # The PCM data from Polly is in 16-bit little-endian, so we'll use 'int16'
        samples = np.frombuffer(audio_stream, dtype=np.int16)
        # Play the audio
        sd.play(samples, sample_rate)
        sd.wait()
        # try:
        #     # Use a loop to wait indefinitely until you decide to stop the script.
        #     print("Playing audio... Press Ctrl+C to stop.")
        #     while True:
        #         sd.sleep(1000)  # Sleeps for 1000 milliseconds (1 second) at a time
        # except KeyboardInterrupt:
        #     print("Playback interrupted by user.")
        # finally:
        #     sd.stop()  # Stop any playback

        print("Playback has been stopped.")
