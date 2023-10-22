import pyaudio

def test_mic():
    # Parameters for pyaudio stream
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, output=True, frames_per_buffer=CHUNK)

    print("Testing microphone... Press Ctrl+C to stop.")

    try:
        while True:
            data = stream.read(CHUNK)
            stream.write(data)  # Playback the captured audio in real-time
    except KeyboardInterrupt:
        print("\nStopping microphone test...")
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    test_mic()
