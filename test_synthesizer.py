import boto3
import io
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import numpy as np
import wave


boto3.setup_default_session(profile_name='Ahmad_personal_projects')
# Initialize the Amazon Polly client
polly_client = boto3.client('polly', region_name='us-east-2')

# Text to be converted to speech
text = "Hello, World! This is Ahmad."

# Call Amazon Polly to convert the text to speech
response = polly_client.synthesize_speech(
    Text=text,
    OutputFormat='pcm',
    VoiceId='Joanna'
)

# Read the audio stream from the response
audio_stream = response['AudioStream'].read()


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
try:
    # Use a loop to wait indefinitely until you decide to stop the script.
    print("Playing audio... Press Ctrl+C to stop.")
    while True:
        sd.sleep(1000)  # Sleeps for 1000 milliseconds (1 second) at a time
except KeyboardInterrupt:
    print("Playback interrupted by user.")
finally:
    sd.stop()  # Stop any playback

print("Playback has been stopped.")


# # Pydub
# # Convert the audio stream to an AudioSegment
# audio_segment = AudioSegment.from_file(io.BytesIO(audio_stream), format="mp3")
# # Play the audio
# play(audio_segment)

# print("Speech synthesis complete. Audio played through speakers.")
