from collections import deque
import pyaudio

def is_silent(data):
    SILENCE_THRESHOLD = 500
    """Returns 'True' if below the 'silent' threshold"""
    return max(data) < SILENCE_THRESHOLD

def test_mic():
    # Parameters for pyaudio stream
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    SILENCE_DURATION = 5  # How many seconds of silence before we consider the conversation over

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, output=True, frames_per_buffer=CHUNK)

    print("Testing microphone... Press Ctrl+C to stop.")
    # Initialize the buffer and silence tracking
    audio_buffer = deque(maxlen=int(RATE / CHUNK * SILENCE_DURATION))
    silent_time = 0

    while True:
        # Read a chunk of data
        data = stream.read(CHUNK, exception_on_overflow=False)
        stream.write(data)

        if not data:
            print("No data read from the microphone.")
        else:
            # Check for silence
            if is_silent(data):
                silent_time += (CHUNK / RATE)
                if silent_time > 5:  # 5 seconds of silence
                    print("Silence detected. Stopping listening.")
                    audio_buffer.append(data)
                    break
            else:
                silent_time = 0  # Reset the silence timer

        # Append data to the buffer
        audio_buffer.append(data)

    print("Recording stopped, playing back...")

    for data in audio_buffer:
        stream.write(data)

    # Stop and close the playback stream
    stream.stop_stream()
    stream.close()

    print("Playback finished.")

    # try:
    #     while True:
    #         data = stream.read(CHUNK)
    #         stream.write(data)  # Playback the captured audio in real-time
    # except KeyboardInterrupt:
    #     print("\nStopping microphone test...")
    #     stream.stop_stream()
    #     stream.close()
    #     audio.terminate()

if __name__ == "__main__":
    test_mic()
