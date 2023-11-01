import boto3

# Initialize the Amazon Polly client
polly_client = boto3.client('polly')

# Text to be converted to speech
text = "Hello, World!"

# Call Amazon Polly to convert the text to speech
response = polly_client.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna'
)

# Save the audio to a file
with open('hello_world.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())

print("Speech synthesis complete. Audio saved as 'hello_world.mp3'.")