import audioop
from collections import deque
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
        self.listener = Listener()
        self.transcriber = Transcriber()
        self.llm = LLM()
        self.synthesizer = Synthesizer()
        self.converstaion = ''
    async def start_conv(self):
        try:
            while True:
                audio = await self.listener.listen()
                print("Listening... Press Ctrl+C to stop.")
                transcripts = await self.transcriber.transcribe(audio)
                transcript = ' '.join(transcripts)
                self.converstaion += transcript
                response = self.llm.process(self.converstaion)
                self.converstaion += response
                self.synthesizer.speak(response)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.listener.close_stream()


class Listener:
    def __init__(self):
        # Parameters for pyaudio stream
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.SILENCE_DURATION = 5  # How many seconds of silence before we consider the conversation over
        self.silence_threshold = 200

        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                            input=True, output=True, frames_per_buffer=self.CHUNK)

        # Initialize the buffer and silence tracking
        # self.audio_buffer = deque(maxlen=int(self.RATE / self.CHUNK * self.SILENCE_DURATION))
        self.audio_buffer = deque()
    async def listen(self):
        self.audio_buffer = deque()
        self.silent_time = 0
        started_speaking = False
        print("Testing microphone...")
        data = self.stream.read(self.CHUNK, exception_on_overflow=True)
        self.silence_threshold = self.get_base_room_noise(data) * 5
        print("Silence threshold: " + str(self.silence_threshold * 3))
        print("Listening until silence, or Ctrl+C is pressed...")
        while True:
            # Read a chunk of data
            data = self.stream.read(self.CHUNK, exception_on_overflow=True)
            if not started_speaking:
                if not self.is_silent(data):
                    started_speaking = True
                else:
                    continue
            # self.stream.write(data)
            # if not data:
            #     print("No data read from the microphone.")
            else:
                # Check for silence
                if self.is_silent(data):
                    self.silent_time += (self.CHUNK / self.RATE)
                    # print (self.silent_time)
                    if self.silent_time > 2:  # 5 seconds of silence
                        print("Silence detected. Stopping listening.")
                        self.audio_buffer.append(data)
                        break
                else:
                    self.silent_time = 0  # Reset the silence timer

            # Append data to the buffer
            self.audio_buffer.append(data)
        print("Recording stopped, playing back...")

        for data in self.audio_buffer:
            self.stream.write(data)

        # Stop and close the playback stream
        print("Playback finished.")
        return b''.join(self.audio_buffer)
    def is_silent(self, snd_data):
        """Returns 'True' if below the 'silent' threshold"""
        # print (audioop.rms(snd_data, 2))
        return audioop.rms(snd_data, 2) < self.silence_threshold
    def get_base_room_noise(self, snd_data):
        """Returns 'True' if below the 'silent' threshold"""
        return audioop.rms(snd_data, 2)
    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        
class Transcriber:
    def __init__(self):
        self.api_key = DEEPGRAM_API_KEY
        self.deepgram = Deepgram(self.api_key)
        self.RATE = 44100
    
    async def transcribe(self, data):
        transcripts = []
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

            deepgramLive.send(data)
            logging.debug("Sent audio data to Deepgram.")
            await asyncio.sleep(0.1)
            await deepgramLive.finish()
        except KeyboardInterrupt:
            await deepgramLive.finish()
        
        print (transcripts[:-1])
        return transcripts[:-1]

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

        ssml_text = f"<speak><prosody rate='200%'>{text}</prosody></speak>"  # 2x speed

        # Convert text to speech and play it
        response = self.polly_client.synthesize_speech(
            TextType='ssml',
            Text=ssml_text,
            OutputFormat='pcm',
            VoiceId='Joanna'
        )

        # Read the audio stream from the response
        audio_stream = response['AudioStream'].read()

        # Assuming the sample width is 2 bytes and sample rate is 16000 Hz
        sample_rate = 16000
        # The PCM data from Polly is in 16-bit little-endian, so we'll use 'int16'
        samples = np.frombuffer(audio_stream, dtype=np.int16)
        
        # Add silence at the end by appending zeros
        silence_duration = 2  # 2 seconds of silence
        silence_samples = np.zeros(int(sample_rate * silence_duration), dtype=np.int16)
        samples_with_silence = np.concatenate((samples, silence_samples))


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


        # Play the audio
        sd.play(samples_with_silence, sample_rate)
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
