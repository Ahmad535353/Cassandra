import boto3
import io
from pydub import AudioSegment
from pydub.playback import play

boto3.setup_default_session(profile_name='Ahmad_personal_projects')
# Initialize the Amazon Polly client
polly_client = boto3.client('polly', region_name='us-east-2')

# Text to be converted to speech
text = "Hello, World!"

# Call Amazon Polly to convert the text to speech
response = polly_client.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna'
)

# # Save the audio to a file
# with open('hello_world.mp3', 'wb') as file:
#     file.write(response['AudioStream'].read())
# print("Speech synthesis complete. Audio saved as 'hello_world.mp3'.")


# Read the audio stream from the response
audio_stream = response['AudioStream'].read()


# Convert the audio stream to an AudioSegment
audio_segment = AudioSegment.from_file(io.BytesIO(audio_stream), format="mp3")

# Play the audio
play(audio_segment)

print("Speech synthesis complete. Audio played through speakers.")
